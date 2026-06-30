"""
Small-Model CKG Benchmark Harness

Measures how much CKG retrieval closes the quality gap when using small open-source
models vs frontier models — the core claim for the dev-tools/OSS community.

Gap-Closed % = (small+CKG_F1 - small_baseline_F1) / (frontier+CKG_F1 - small_baseline_F1)

  - small_baseline: small model with NO context (raw parametric knowledge)
  - small+CKG: small model grounded on deterministic subgraph from CKG harness
  - frontier+CKG: locked numbers from the main benchmark (F1=0.4926)

Backends:
  ollama     — Ollama local server at localhost:11434 (OpenAI-compatible)
  anthropic  — Anthropic API (Claude; for frontier ceiling run)

Modes:
  ckg        — CKG subgraph retrieval + model answer
  baseline   — No context; model answers from parametric memory only

Usage:
  # Run CKG mode with qwen3:8b (Ollama must be running)
  python evaluation/small_model_harness.py --model qwen3:8b --mode ckg

  # Run baseline (no context) with the same model
  python evaluation/small_model_harness.py --model qwen3:8b --mode baseline

  # Run both modes back-to-back
  python evaluation/small_model_harness.py --model qwen3:8b --mode both

  # Frontier ceiling comparison (Anthropic)
  python evaluation/small_model_harness.py \\
    --model claude-haiku-4-5-20251001 --backend anthropic --mode ckg

  # Print gap-closed report after runs
  python evaluation/small_model_harness.py --gap-report

  # Dry run to test retrieval without API calls
  python evaluation/small_model_harness.py --model qwen3:8b --mode ckg --dry-run
"""

import csv
import json
import os
import random
import re
import sys
import time
import argparse
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────────────────

DOMAINS_DIR  = Path("benchmark/domains")
QUERIES_DIR  = Path("benchmark/queries")
RESULTS_DIR  = Path("results/small_model")

# ── Sample config ──────────────────────────────────────────────────────────────

DEFAULT_DOMAINS = [
    "calculus",
    "biology",
    "blockchain",
    "chemistry",
    "computer-science",
    "economics-course",
    "bioinformatics",
    "circuits",
]
QUERIES_PER_DOMAIN = 60   # ~480 total — manageable for a single GPU/ollama run

# Frontier CKG locked numbers from main benchmark (ckg_summary.json, v0.6.2)
FRONTIER_CKG_F1  = 0.4926
FRONTIER_RAG_F1  = 0.1231
FRONTIER_TOKENS  = 263.5

# ── System prompts ─────────────────────────────────────────────────────────────

CKG_SYSTEM = (
    "You are a knowledge graph query engine. You will be given a structured "
    "knowledge graph subgraph and a question. Answer the question using ONLY "
    "the information in the subgraph. Be concise and precise. List concepts as "
    "comma-separated values when asked to enumerate. Do not add information not "
    "present in the subgraph."
)

BASELINE_SYSTEM = (
    "You are a precise question-answering assistant. Answer the question concisely "
    "and accurately using your knowledge. List concepts as comma-separated values "
    "when asked to enumerate."
)

# ── Graph data structures ──────────────────────────────────────────────────────

class Concept:
    __slots__ = ("id", "label", "dependencies", "taxonomy_id")
    def __init__(self, cid, label, deps, tax):
        self.id           = cid
        self.label        = label
        self.dependencies = deps
        self.taxonomy_id  = tax


def load_graph(csv_path: Path) -> dict:
    concepts = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            cid  = int(row["ConceptID"])
            deps = [int(d) for d in row.get("Dependencies","").split("|") if d.strip().isdigit()]
            concepts[cid] = Concept(cid, row["ConceptLabel"].strip(), deps,
                                    row.get("TaxonomyID","GEN").strip())
    return concepts


def find_concept_by_label(concepts: dict, label: str) -> Optional[Concept]:
    ll = label.lower()
    for c in concepts.values():
        if c.label.lower() == ll:
            return c
    for c in concepts.values():
        if ll in c.label.lower():
            return c
    return None


def bfs_ancestors(concepts: dict, start_id: int) -> list:
    visited, queue, path = set(), deque([start_id]), []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node); path.append(node)
        for d in concepts.get(node, Concept(0,"",[],"")).dependencies:
            if d not in visited:
                queue.append(d)
    return path


def bfs_path(concepts: dict, a: int, b: int) -> list:
    if a == b:
        return [a]
    rev = defaultdict(set)
    for cid, c in concepts.items():
        for d in c.dependencies:
            rev[d].add(cid)
    queue, visited = deque([(a, [a])]), {a}
    while queue:
        node, path = queue.popleft()
        nbs = set(concepts[node].dependencies if node in concepts else []) | rev[node]
        for nb in nbs:
            if nb in visited or nb not in concepts:
                continue
            np = path + [nb]
            if nb == b:
                return np
            visited.add(nb); queue.append((nb, np))
    return [a, b]


def subgraph_to_context(concepts: dict, ids: list) -> str:
    lines = ["KNOWLEDGE GRAPH SUBGRAPH:"]
    for cid in ids:
        if cid not in concepts:
            continue
        c = concepts[cid]
        deps = ", ".join(concepts[d].label for d in c.dependencies if d in concepts) or "none"
        lines.append(f"  [{c.taxonomy_id}] {c.label} | prerequisites: {deps}")
    return "\n".join(lines)


def retrieve(concepts: dict, q: dict) -> tuple:
    qtype = q.get("query_type") or q.get("type", "")
    if qtype == "T1_entity":
        cid = q.get("concept_id")
        c   = concepts.get(cid) if cid else None
        if not c:
            c = find_concept_by_label(concepts, q["ground_truth"][0])
        if not c:
            return "No matching concept found.", []
        rev  = [cc.id for cc in concepts.values() if c.id in cc.dependencies]
        ids  = list(dict.fromkeys([c.id] + c.dependencies + rev[:5]))
        return subgraph_to_context(concepts, ids), ids

    elif qtype == "T2_dependency":
        cid = q.get("concept_id")
        c   = concepts.get(cid) if cid else None
        if not c:
            txt = q["query"].replace("What are the prerequisites for ","").rstrip("?").strip()
            c   = find_concept_by_label(concepts, txt)
        if not c:
            return "No matching concept found.", []
        ids = [c.id] + c.dependencies
        return subgraph_to_context(concepts, ids), ids

    elif qtype == "T3_path":
        if q.get("path_ids"):
            ids = q["path_ids"]
        else:
            ids = [c.id for lbl in q.get("ground_truth",[])
                   if (c := find_concept_by_label(concepts, lbl))]
        if not ids:
            cid = q.get("concept_id")
            ids = bfs_ancestors(concepts, cid) if cid and cid in concepts else []
        return subgraph_to_context(concepts, ids), ids

    elif qtype == "T4_aggregate":
        tax = q.get("taxonomy_id","")
        ids = ([c.id for c in concepts.values() if c.taxonomy_id == tax] if tax
               else [c.id for lbl in q.get("ground_truth",[])
                     if (c := find_concept_by_label(concepts, lbl))])
        return subgraph_to_context(concepts, ids), ids

    elif qtype == "T5_cross_concept":
        a, b = q.get("concept_id_a"), q.get("concept_id_b")
        if a in concepts and b in concepts:
            path = bfs_path(concepts, a, b)
            shared = [cc.id for cc in concepts.values()
                      if concepts[a].id in cc.dependencies and concepts[b].id in cc.dependencies]
            ids = list(dict.fromkeys(
                path + shared + concepts[a].dependencies[:3] + concepts[b].dependencies[:3]
            ))
        else:
            ids = []
        return subgraph_to_context(concepts, ids), ids

    return "Query type not recognized.", []

# ── Scoring ────────────────────────────────────────────────────────────────────

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts","based","on","knowledge","graph",
    "subgraph","prerequisites","prerequisite","following",
}

def normalize(text: str) -> str:
    text = re.sub(r'\*+|_+|`+|#+\s*', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def token_f1(predicted: str, ground_truth: list) -> dict:
    pred  = set(normalize(predicted).lower().split()) - STOPWORDS
    truth = set(normalize(" ".join(ground_truth)).lower().split()) - STOPWORDS
    if not pred and not truth:
        return {"f1": 1.0, "precision": 1.0, "recall": 1.0}
    if not pred or not truth:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}
    tp = len(pred & truth)
    p  = tp / len(pred)
    r  = tp / len(truth)
    f1 = 2*p*r/(p+r) if (p+r) > 0 else 0.0
    return {"f1": round(f1,4), "precision": round(p,4), "recall": round(r,4)}

# ── LLM adapters ──────────────────────────────────────────────────────────────

def make_client(backend: str):
    if backend == "anthropic":
        import anthropic as sdk
        return sdk.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    else:  # ollama
        from openai import OpenAI
        return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def call_model(client, model: str, backend: str,
               system: str, user_msg: str, max_tokens: int = 512) -> tuple:
    """Returns (answer_text, input_tokens, output_tokens, latency_ms)."""
    t0 = time.time()
    if backend == "anthropic":
        resp = client.messages.create(
            model=model, max_tokens=max_tokens, temperature=0,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        answer = resp.content[0].text
        in_tok, out_tok = resp.usage.input_tokens, resp.usage.output_tokens
    else:  # openai-compatible (ollama)
        resp = client.chat.completions.create(
            model=model, temperature=0, max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user_msg},
            ],
        )
        answer  = resp.choices[0].message.content or ""
        # Ollama reports usage in prompt_tokens / completion_tokens
        in_tok  = getattr(resp.usage, "prompt_tokens",     0)
        out_tok = getattr(resp.usage, "completion_tokens", 0)
    latency_ms = int((time.time() - t0) * 1000)
    return answer, in_tok, out_tok, latency_ms

# ── Stratified sampler ─────────────────────────────────────────────────────────

def stratified_sample(domain: str, n: int, rng: random.Random) -> list:
    """Sample n queries from a domain, proportional to type distribution."""
    path = QUERIES_DIR / f"queries_{domain}.jsonl"
    if not path.exists():
        return []
    queries = [json.loads(l) for l in path.open() if l.strip()]
    by_type = defaultdict(list)
    for q in queries:
        by_type[q.get("query_type") or q.get("type","?")].append(q)

    total = len(queries)
    sampled = []
    for qtype, qs in by_type.items():
        k = max(1, round(n * len(qs) / total))
        sampled.extend(rng.sample(qs, min(k, len(qs))))

    rng.shuffle(sampled)
    return sampled[:n]

# ── Domain runner ──────────────────────────────────────────────────────────────

def run_domain(domain: str, queries: list, client, model: str, backend: str,
               mode: str, dry_run: bool) -> list:
    csv_path = DOMAINS_DIR / domain / "learning-graph.csv"
    if not csv_path.exists():
        print(f"  ✗ no CSV for {domain}")
        return []

    concepts = load_graph(csv_path) if mode == "ckg" else {}
    results  = []

    for i, q in enumerate(queries):
        if mode == "ckg":
            context, _ = retrieve(concepts, q)
            system     = CKG_SYSTEM
            user_msg   = f"{context}\n\nQuestion: {q['query']}"
        else:
            system   = BASELINE_SYSTEM
            user_msg = q["query"]

        if dry_run:
            results.append({
                **q,
                "model": model, "backend": backend, "mode": mode,
                "predicted_answer": "[DRY RUN]",
                "f1": 0.0, "precision": 0.0, "recall": 0.0,
                "prompt_tokens": 0, "completion_tokens": 0,
                "total_tokens": 0, "latency_ms": 0, "cost_usd": 0.0,
            })
            continue

        try:
            answer, in_tok, out_tok, lat = call_model(
                client, model, backend, system, user_msg)
        except Exception as e:
            print(f"    ✗ {q.get('id','?')}: {e}")
            continue

        scores = token_f1(answer, q.get("ground_truth",[]))
        total  = in_tok + out_tok

        results.append({
            **q,
            "model": model, "backend": backend, "mode": mode,
            "predicted_answer": answer,
            "f1":        scores["f1"],
            "precision": scores["precision"],
            "recall":    scores["recall"],
            "prompt_tokens":     in_tok,
            "completion_tokens": out_tok,
            "total_tokens":      total,
            "latency_ms":        lat,
            "cost_usd":          0.0,  # ollama = free; anthropic cost added in summary
        })

        if (i+1) % 20 == 0:
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            print(f"    [{i+1}/{len(queries)}] avg_F1={avg_f1:.3f}")

        time.sleep(0.05)  # avoid hammering Ollama

    return results


def summarize(results: list) -> dict:
    if not results:
        return {}
    all_f1  = [r["f1"] for r in results]
    all_tok = [r["total_tokens"] for r in results]
    by_type = defaultdict(list)
    by_hop  = defaultdict(list)
    for r in results:
        by_type[r.get("query_type") or r.get("type","?")].append(r["f1"])
        by_hop[r.get("hop_depth",0)].append(r["f1"])
    return {
        "model":      results[0]["model"],
        "backend":    results[0]["backend"],
        "mode":       results[0]["mode"],
        "n_queries":  len(results),
        "macro_f1":   round(sum(all_f1)/len(all_f1), 4),
        "mean_tokens": round(sum(all_tok)/len(all_tok), 1),
        "f1_by_type": {k: round(sum(v)/len(v),4) for k,v in by_type.items()},
        "f1_by_hop":  {k: round(sum(v)/len(v),4) for k,v in by_hop.items()},
    }

# ── Gap-closed report ──────────────────────────────────────────────────────────

def gap_report():
    sm_dir = RESULTS_DIR
    if not sm_dir.exists():
        print("No small_model results found. Run --mode ckg and --mode baseline first.")
        return

    # Load all summaries
    summaries = {}
    for f in sm_dir.glob("*/summary_*.json"):
        with open(f) as fh:
            s = json.load(fh)
        key = f"{s['model']}:{s['mode']}"
        summaries[key] = s

    if not summaries:
        print("No summary files found under", sm_dir)
        return

    print("\n── Small-Model CKG Benchmark — Gap-Closed Report ──\n")
    print(f"  Frontier CKG F1  (locked): {FRONTIER_CKG_F1}")
    print(f"  Frontier RAG F1  (locked): {FRONTIER_RAG_F1}\n")

    models = sorted({k.split(":")[0] for k in summaries})
    for model in models:
        ckg_key  = f"{model}:ckg"
        base_key = f"{model}:baseline"
        ckg_f1   = summaries[ckg_key]["macro_f1"]  if ckg_key  in summaries else None
        base_f1  = summaries[base_key]["macro_f1"] if base_key in summaries else None
        tok      = summaries[ckg_key]["mean_tokens"] if ckg_key in summaries else "—"

        print(f"  {model}")
        if base_f1 is not None:
            print(f"    baseline F1  (no context): {base_f1:.4f}")
        if ckg_f1 is not None:
            print(f"    CKG F1               : {ckg_f1:.4f}")
            print(f"    mean tokens (CKG)    : {tok:.0f}" if isinstance(tok, float) else f"    mean tokens (CKG): {tok}")
        if ckg_f1 is not None and base_f1 is not None:
            denom = FRONTIER_CKG_F1 - base_f1
            gap   = (ckg_f1 - base_f1) / denom if denom else 0.0
            print(f"    gap-closed vs frontier: {gap*100:.1f}%")
        print()

    print("  (Gap-closed = (small+CKG − small_baseline) / (frontier+CKG − small_baseline))")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Small-model CKG benchmark — measures gap-closed vs frontier"
    )
    parser.add_argument("--model",   default="qwen3:8b",
                        help="Model name (e.g. qwen3:8b, llama3.2:8b, claude-haiku-4-5-20251001)")
    parser.add_argument("--backend", choices=["ollama","anthropic"], default="ollama",
                        help="Inference backend")
    parser.add_argument("--mode",    choices=["ckg","baseline","both"], default="ckg",
                        help="ckg = grounded on subgraph; baseline = no context")
    parser.add_argument("--domains", nargs="+", default=DEFAULT_DOMAINS,
                        help="Domains to run (default: 8 diverse domains)")
    parser.add_argument("--n",       type=int, default=QUERIES_PER_DOMAIN,
                        help="Queries per domain (default: 60)")
    parser.add_argument("--seed",    type=int, default=42)
    parser.add_argument("--dry-run", action="store_true",
                        help="Test retrieval without calling the model")
    parser.add_argument("--gap-report", action="store_true",
                        help="Print gap-closed report from saved results and exit")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel domain workers (use 1 for Ollama; higher for Anthropic)")
    args = parser.parse_args()

    if args.gap_report:
        gap_report()
        return

    modes = ["ckg","baseline"] if args.mode == "both" else [args.mode]

    if not args.dry_run:
        if args.backend == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("Set ANTHROPIC_API_KEY for anthropic backend.")

    rng    = random.Random(args.seed)
    client = None if args.dry_run else make_client(args.backend)

    for mode in modes:
        slug     = args.model.replace(":", "-").replace("/", "-")
        out_dir  = RESULTS_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n── Small-Model Harness  mode={mode}  model={args.model}  backend={args.backend} ──")
        print(f"   Domains : {args.domains}")
        print(f"   Queries : {args.n}/domain  ({len(args.domains)*args.n} total)")
        print(f"   Output  : {out_dir}/\n")

        all_results = []
        domain_summaries = {}

        def process(domain):
            queries = stratified_sample(domain, args.n, random.Random(args.seed))
            if not queries:
                return domain, []
            print(f"  {domain}: {len(queries)} queries")
            results = run_domain(domain, queries, client, args.model,
                                 args.backend, mode, args.dry_run)
            if results:
                out_path = out_dir / f"{mode}_{domain}.jsonl"
                with open(out_path, "w") as fh:
                    for r in results:
                        fh.write(json.dumps(r) + "\n")
                s = summarize(results)
                if not args.dry_run:
                    print(f"   {domain}: F1={s['macro_f1']}  tokens={s['mean_tokens']:.0f}")
                return domain, results
            return domain, []

        if args.workers > 1:
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                futs = {pool.submit(process, d): d for d in args.domains}
                for fut in as_completed(futs):
                    domain, results = fut.result()
                    if results:
                        domain_summaries[domain] = summarize(results)
                        all_results.extend(results)
        else:
            for domain in args.domains:
                _, results = process(domain)
                if results:
                    domain_summaries[domain] = summarize(results)
                    all_results.extend(results)

        if all_results:
            global_summary = summarize(all_results)
            global_summary["by_domain"] = domain_summaries
            summary_path = out_dir / f"summary_{mode}.json"
            with open(summary_path, "w") as fh:
                json.dump(global_summary, fh, indent=2)

            print(f"\n── {mode.upper()} SUMMARY ──")
            print(f"   Domains   : {len(domain_summaries)}")
            print(f"   Queries   : {global_summary['n_queries']}")
            print(f"   Macro F1  : {global_summary['macro_f1']}")
            print(f"   Mean tok  : {global_summary['mean_tokens']:.0f}")
            print(f"\n   F1 by query type:")
            for qtype, f1 in sorted(global_summary["f1_by_type"].items()):
                print(f"     {qtype}: {f1}")
            print(f"\n   Results → {out_dir}/")

    if len(modes) == 2 and all_results:
        gap_report()


if __name__ == "__main__":
    main()
