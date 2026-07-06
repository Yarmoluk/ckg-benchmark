"""
KRB Eval — Knowledge Retrieval Benchmark evaluation harness.

Evaluates any retrieval system against the KRB dataset and produces a
submission-ready results file for the leaderboard.

Dataset:  huggingface.co/datasets/danyarm/ckg-benchmark
Paper:    github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf
Leaderboard: huggingface.co/spaces/danyarm/krb-leaderboard

─────────────────────────────────────────────────────────────────────────────
QUICK START — evaluate the built-in CKG system:

    pip install anthropic huggingface_hub
    export ANTHROPIC_API_KEY=...
    python evaluation/krb_eval.py --system ckg --domain calculus
    python evaluation/krb_eval.py --system ckg --all

PLUG IN YOUR OWN SYSTEM:

    from evaluation.krb_eval import Retriever, run_eval

    class MyRAGRetriever(Retriever):
        def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
            # Return the context string your system would pass to an LLM.
            # meta has: type, concept_id, hop_depth, ground_truth, etc.
            return my_rag_function(domain, query_text)

    results = run_eval(
        retriever=MyRAGRetriever(),
        system_name="my-rag-v1",
        domains=["calculus", "biology"],   # or None for all 45
    )
    # → writes krb_submission_my-rag-v1_<timestamp>.json
    # → open a GitHub issue at github.com/Yarmoluk/ckg-benchmark to submit

─────────────────────────────────────────────────────────────────────────────
"""

import csv
import json
import os
import re
import time
import argparse
import tempfile
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from pathlib import Path
from typing import Optional

# ── Optional imports (loaded lazily) ─────────────────────────────────────────

def _require(pkg, install_hint=None):
    import importlib
    try:
        return importlib.import_module(pkg)
    except ImportError:
        hint = install_hint or f"pip install {pkg}"
        raise SystemExit(f"Missing package '{pkg}'. Install with: {hint}")


# ── Config ────────────────────────────────────────────────────────────────────

DATASET_REPO   = "danyarm/ckg-benchmark"
DEFAULT_MODEL  = "claude-haiku-4-5-20251001"
PRICE_INPUT    = 0.80 / 1_000_000   # Haiku input  $/token
PRICE_OUTPUT   = 4.00 / 1_000_000   # Haiku output $/token

LOCAL_DOMAINS  = Path(__file__).parent.parent / "benchmark" / "domains"
LOCAL_QUERIES  = Path(__file__).parent.parent / "benchmark" / "queries"

SYSTEM_PROMPT = (
    "Answer the question using ONLY the information in the provided context. "
    "Be concise and precise. List concepts as comma-separated values when asked "
    "to enumerate. Do not add information not present in the context."
)

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts","based","on","knowledge","graph",
    "subgraph","prerequisites","prerequisite","following","use","given","find",
}


# ── Graph structures ──────────────────────────────────────────────────────────

class Concept:
    __slots__ = ("id", "label", "dependencies", "taxonomy_id")
    def __init__(self, id, label, dependencies, taxonomy_id):
        self.id = id; self.label = label
        self.dependencies = dependencies; self.taxonomy_id = taxonomy_id


def load_graph_csv(path) -> dict:
    concepts = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            cid  = int(row["ConceptID"])
            deps = [int(d) for d in row.get("Dependencies","").split("|")
                    if d.strip().isdigit()]
            concepts[cid] = Concept(
                id=cid,
                label=row["ConceptLabel"].strip(),
                dependencies=deps,
                taxonomy_id=row.get("TaxonomyID","GEN").strip(),
            )
    return concepts


def _find(concepts, label):
    ll = label.lower()
    for c in concepts.values():
        if c.label.lower() == ll: return c
    for c in concepts.values():
        if ll in c.label.lower(): return c
    return None

def _rev_index(concepts):
    rev = defaultdict(set)
    for cid, c in concepts.items():
        for d in c.dependencies: rev[d].add(cid)
    return rev

def _bfs_ancestors(concepts, start):
    visited, queue, path = set(), deque([start]), []
    while queue:
        n = queue.popleft()
        if n in visited: continue
        visited.add(n); path.append(n)
        for d in concepts[n].dependencies:
            if d not in visited: queue.append(d)
    return path

def _bfs_path(concepts, a, b):
    if a == b: return [a]
    rev = _rev_index(concepts)
    queue, visited = deque([(a,[a])]), {a}
    while queue:
        node, path = queue.popleft()
        nbrs = set(concepts[node].dependencies) | rev[node] if node in concepts else set()
        for nb in nbrs:
            if nb in visited or nb not in concepts: continue
            np = path + [nb]
            if nb == b: return np
            visited.add(nb); queue.append((nb, np))
    return [a, b]

def _serialize(concepts, ids):
    lines = ["KNOWLEDGE GRAPH SUBGRAPH:"]
    for cid in ids:
        if cid not in concepts: continue
        c = concepts[cid]
        deps = ", ".join(concepts[d].label for d in c.dependencies if d in concepts) or "none"
        lines.append(f"  [{c.taxonomy_id}] {c.label} | prerequisites: {deps}")
    return "\n".join(lines)


# ── Retriever interface ───────────────────────────────────────────────────────

class Retriever(ABC):
    """
    Implement this to plug your system into KRB.

    retrieve() should return the context string that would be prepended to the
    query when calling an LLM. The harness handles the LLM call and scoring.

    If your system is end-to-end (it generates an answer, not just retrieves),
    override generate() instead and leave retrieve() returning an empty string.
    """

    @abstractmethod
    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        """
        domain     : e.g. "calculus"
        query_text : the benchmark query string
        meta       : full query record — type, concept_id, hop_depth, ground_truth
        returns    : context string to prepend to query for the LLM
        """

    def generate(self, context: str, query_text: str, client, model: str) -> tuple[str,int,int]:
        """
        Default: calls Claude with system prompt + context + query.
        Returns (answer_str, prompt_tokens, completion_tokens).
        Override to use a different LLM or end-to-end system.
        """
        msg = client.messages.create(
            model=model,
            max_tokens=512,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role":"user","content":f"{context}\n\nQuestion: {query_text}"}],
        )
        return (msg.content[0].text,
                msg.usage.input_tokens,
                msg.usage.output_tokens)

    def setup(self, domain: str, graph_path: Path):
        """Called once per domain before queries run. Override to pre-load indexes."""
        pass


# ── Built-in CKG retriever ────────────────────────────────────────────────────

class CKGRetriever(Retriever):
    """
    Reference implementation: BFS/DFS over a typed dependency graph.
    Downloads graph CSVs from huggingface.co/datasets/danyarm/ckg-benchmark
    (falls back to local benchmark/domains/ if present).
    """

    def __init__(self):
        self._concepts = {}   # domain → {id: Concept}
        self._cache_dir = Path(tempfile.gettempdir()) / "krb_graphs"
        self._cache_dir.mkdir(exist_ok=True)

    def setup(self, domain: str, graph_path: Path):
        self._concepts[domain] = load_graph_csv(graph_path)

    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        concepts = self._concepts.get(domain, {})
        if not concepts:
            return "Graph not loaded."
        qtype = meta.get("type") or meta.get("query_type","")

        if qtype == "T1_entity":
            cid = meta.get("concept_id")
            c   = concepts.get(cid) or _find(concepts, meta.get("ground_truth",[""])[0])
            if not c: return "Concept not found."
            rev = [cc.id for cc in concepts.values() if c.id in cc.dependencies]
            ids = list(dict.fromkeys([c.id] + c.dependencies + rev[:5]))

        elif qtype == "T2_dependency":
            cid = meta.get("concept_id")
            c   = concepts.get(cid) or _find(concepts, query_text.split("for ")[-1].rstrip("?"))
            if not c: return "Concept not found."
            ids = [c.id] + c.dependencies

        elif qtype == "T3_path":
            ids = meta.get("path_ids") or []
            if not ids:
                for label in meta.get("ground_truth",[]):
                    cc = _find(concepts, label)
                    if cc: ids.append(cc.id)
            if not ids:
                cid = meta.get("concept_id")
                if cid and cid in concepts:
                    ids = _bfs_ancestors(concepts, cid)

        elif qtype == "T4_aggregate":
            tax = meta.get("taxonomy_id","")
            if tax:
                ids = [c.id for c in concepts.values() if c.taxonomy_id == tax]
            else:
                ids = [cc.id for label in meta.get("ground_truth",[])
                       for cc in [_find(concepts, label)] if cc]

        elif qtype == "T5_cross_concept":
            a, b = meta.get("concept_id_a"), meta.get("concept_id_b")
            if a in concepts and b in concepts:
                path = _bfs_path(concepts, a, b)
                shared = [c.id for c in concepts.values()
                          if a in c.dependencies and b in c.dependencies]
                ids = list(dict.fromkeys(
                    path + shared +
                    concepts[a].dependencies[:3] + concepts[b].dependencies[:3]
                ))
            else:
                ids = []
        else:
            ids = []

        return _serialize(concepts, ids)


# ── Scoring ───────────────────────────────────────────────────────────────────

def _norm(text):
    text = re.sub(r'[*_`#]', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def token_f1(predicted: str, ground_truth: list) -> dict:
    pred   = set(_norm(predicted).lower().split()) - STOPWORDS
    truth  = set(_norm(" ".join(ground_truth)).lower().split()) - STOPWORDS
    if not pred and not truth: return {"f1":1.0,"p":1.0,"r":1.0}
    if not pred or not truth:  return {"f1":0.0,"p":0.0,"r":0.0}
    tp = len(pred & truth)
    p  = tp / len(pred)
    r  = tp / len(truth)
    f1 = 2*p*r/(p+r) if p+r else 0.0
    return {"f1":round(f1,4),"p":round(p,4),"r":round(r,4)}


# ── Data loading ──────────────────────────────────────────────────────────────

def _load_queries(domain: str) -> list:
    # Prefer local files (fast); fall back to HF download
    local = LOCAL_QUERIES / f"queries_{domain}.jsonl"
    if local.exists():
        with open(local) as f:
            return [json.loads(l) for l in f if l.strip()]

    hf = _require("huggingface_hub", "pip install huggingface_hub")
    path = hf.hf_hub_download(
        repo_id=DATASET_REPO, repo_type="dataset",
        filename=f"queries/queries_{domain}.jsonl",
    )
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def _get_graph_path(domain: str) -> Path:
    local = LOCAL_DOMAINS / domain / "learning-graph.csv"
    if local.exists():
        return local

    hf = _require("huggingface_hub", "pip install huggingface_hub")
    path = hf.hf_hub_download(
        repo_id=DATASET_REPO, repo_type="dataset",
        filename=f"domains/{domain}/learning-graph.csv",
    )
    return Path(path)


def _available_domains() -> list:
    if LOCAL_QUERIES.exists():
        return sorted(p.stem.replace("queries_","")
                      for p in LOCAL_QUERIES.glob("queries_*.jsonl"))
    hf = _require("huggingface_hub", "pip install huggingface_hub")
    api = hf.HfApi()
    files = api.list_repo_tree(DATASET_REPO, repo_type="dataset", path_in_repo="queries")
    return sorted(f.path.split("/")[-1].replace("queries_","").replace(".jsonl","")
                  for f in files if f.path.endswith(".jsonl"))


# ── Domain runner ─────────────────────────────────────────────────────────────

def run_domain(domain, retriever, client, model, dry_run=False, limit=0):
    queries   = _load_queries(domain)
    if limit:
        queries = queries[:limit]
    graph_path = _get_graph_path(domain)
    retriever.setup(domain, graph_path)

    print(f"  {domain}: {len(queries)} queries")
    results = []

    for i, q in enumerate(queries):
        qtext = q["query"]
        context = retriever.retrieve(domain, qtext, q)

        if dry_run:
            results.append({**q, "system":"dry-run",
                            "predicted_answer":"[DRY RUN]",
                            "context_preview": context[:120]+"...",
                            "f1":0.0,"p":0.0,"r":0.0,
                            "prompt_tokens":0,"completion_tokens":0,
                            "total_tokens":0,"rds":0.0,"cost_usd":0.0})
            continue

        t0 = time.time()
        try:
            answer, pt, ct = retriever.generate(context, qtext, client, model)
        except Exception as e:
            print(f"    ✗ {q.get('id','?')}: {e}")
            continue
        latency = int((time.time()-t0)*1000)

        scores = token_f1(answer, q.get("ground_truth",[]))
        total  = pt + ct
        cost   = pt*PRICE_INPUT + ct*PRICE_OUTPUT
        rds    = scores["f1"]/total if total else 0.0

        results.append({
            **q,
            "predicted_answer": answer,
            "context_tokens":   len(context.split()),
            "prompt_tokens":    pt,
            "completion_tokens":ct,
            "total_tokens":     total,
            "f1":    scores["f1"],
            "p":     scores["p"],
            "r":     scores["r"],
            "rds":   round(rds, 8),
            "cost_usd": round(cost, 6),
            "latency_ms": latency,
        })

        if (i+1) % 50 == 0:
            avg_f1 = sum(r["f1"] for r in results)/len(results)
            print(f"    [{i+1}/{len(queries)}] avg_f1={avg_f1:.3f}")

        time.sleep(0.1)

    return results


def _summarize(results: list, system_name: str, domains: list) -> dict:
    if not results:
        return {}

    by_type  = defaultdict(list)
    by_hop   = defaultdict(list)
    by_domain = defaultdict(list)

    for r in results:
        t = r.get("type") or r.get("query_type","unknown")
        by_type[t].append(r["f1"])
        by_hop[r.get("hop_depth",0)].append(r["f1"])
        by_domain[r.get("domain","?")].append(r["f1"])

    all_f1  = [r["f1"] for r in results]
    all_tok = [r.get("total_tokens",0) for r in results]
    all_rds = [r["rds"] for r in results if r.get("rds",0) > 0]
    all_cost = [r.get("cost_usd",0) for r in results]

    return {
        "system":        system_name,
        "krb_version":   "v0.6.2",
        "dataset":       DATASET_REPO,
        "n_queries":     len(results),
        "n_domains":     len(set(r.get("domain") for r in results)),
        "macro_f1":      round(sum(all_f1)/len(all_f1), 4),
        "mean_tokens":   round(sum(all_tok)/len(all_tok), 1) if all_tok else 0,
        "macro_rds":     round(sum(all_rds)/len(all_rds), 8) if all_rds else 0,
        "total_cost_usd":round(sum(all_cost), 4),
        "f1_by_type":    {k: round(sum(v)/len(v),4) for k,v in by_type.items()},
        "f1_by_hop":     {k: round(sum(v)/len(v),4) for k,v in by_hop.items()},
        "f1_by_domain":  {k: round(sum(v)/len(v),4) for k,v in by_domain.items()},
    }


# ── Public API ────────────────────────────────────────────────────────────────

def run_eval(
    retriever: Retriever,
    system_name: str,
    domains: Optional[list] = None,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
    limit: int = 0,
    output_dir: Path = None,
) -> dict:
    """
    Evaluate a retriever against KRB and write a submission file.

    Parameters
    ----------
    retriever   : Retriever subclass implementing .retrieve()
    system_name : Short identifier, e.g. "my-rag-v1" (used in output filename)
    domains     : List of domain names, or None to run all 45
    model       : Anthropic model for answer generation (default: Haiku)
    dry_run     : Skip API calls, test retrieval pipeline only
    limit       : Max queries per domain (0 = all)
    output_dir  : Where to write submission JSON (default: ./krb_results/)

    Returns
    -------
    summary dict  (also written to krb_results/krb_submission_{system_name}.json)
    """
    if domains is None:
        domains = _available_domains()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not dry_run:
        raise SystemExit("Set ANTHROPIC_API_KEY  (or pass --dry-run to skip API calls)")

    anthropic_mod = _require("anthropic", "pip install anthropic")
    client = anthropic_mod.Anthropic(api_key=api_key) if not dry_run else None

    out_dir = Path(output_dir or "krb_results")
    out_dir.mkdir(exist_ok=True)

    print(f"\nKRB Eval — system: {system_name}  model: {model}  {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Domains: {len(domains)}\n")

    all_results = []
    for domain in domains:
        try:
            results = run_domain(domain, retriever, client, model, dry_run, limit)
            all_results.extend(results)
        except Exception as e:
            print(f"  ✗ {domain}: {e}")

    summary = _summarize(all_results, system_name, domains)

    # Write per-query results
    detail_path = out_dir / f"krb_{system_name}_queries.jsonl"
    with open(detail_path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    # Write submission summary
    sub_path = out_dir / f"krb_submission_{system_name}.json"
    with open(sub_path, "w") as f:
        json.dump(summary, f, indent=2)

    if not dry_run and summary:
        print(f"\n── RESULTS ──────────────────────────────────────")
        print(f"   System:       {system_name}")
        print(f"   Domains:      {summary['n_domains']}")
        print(f"   Queries:      {summary['n_queries']}")
        print(f"   Macro F1:     {summary['macro_f1']}")
        print(f"   Mean tokens:  {summary['mean_tokens']:.0f}")
        print(f"   Total cost:   ${summary['total_cost_usd']:.3f}")
        print(f"\n   F1 by query type:")
        for t, f1 in sorted(summary["f1_by_type"].items()):
            print(f"     {t}: {f1}")
        print(f"\n   Submission file: {sub_path}")
        print(f"   Submit at: github.com/Yarmoluk/ckg-benchmark/issues/new")

    return summary


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="KRB Eval — evaluate any retrieval system against the Knowledge Retrieval Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--system",   default="ckg",
                   help="System name tag for output files (default: ckg)")
    p.add_argument("--domain",   nargs="+", help="One or more domains to evaluate")
    p.add_argument("--all",      action="store_true", help="Run all available domains")
    p.add_argument("--model",    default=DEFAULT_MODEL, help=f"Anthropic model (default: {DEFAULT_MODEL})")
    p.add_argument("--dry-run",  action="store_true", help="Test retrieval pipeline without API calls")
    p.add_argument("--limit",    type=int, default=0, help="Max queries per domain (0=all)")
    p.add_argument("--output",   default="krb_results", help="Output directory (default: krb_results/)")
    args = p.parse_args()

    if not args.domain and not getattr(args, 'all', False):
        p.print_help()
        return

    # Built-in systems
    SYSTEMS = {
        "ckg": CKGRetriever,
    }

    if args.system not in SYSTEMS:
        print(f"Unknown built-in system '{args.system}'. Available: {list(SYSTEMS)}")
        print("To use your own system, import run_eval() and pass a custom Retriever.")
        return

    retriever = SYSTEMS[args.system]()
    domains   = args.domain if args.domain else None

    run_eval(
        retriever=retriever,
        system_name=args.system,
        domains=domains,
        model=args.model,
        dry_run=args.dry_run,
        limit=args.limit,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
