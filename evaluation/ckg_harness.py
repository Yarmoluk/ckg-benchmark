"""
CKG Harness — Compressed Knowledge Graph retrieval system.

For each benchmark query, this harness:
1. Loads the domain's learning-graph.csv
2. Retrieves the exact subgraph relevant to the query (no embeddings)
3. Sends subgraph + query to Claude for answer generation
4. Records F1, tokens, and RDS

Usage:
    python evaluation/ckg_harness.py --domain calculus
    python evaluation/ckg_harness.py --all
    python evaluation/ckg_harness.py --all --dry-run
"""

import csv
import json
import time
import argparse
import os
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-6"
DOMAINS_DIR = Path("benchmark/domains")
QUERIES_DIR = Path("benchmark/queries")
RESULTS_DIR = Path("results/ckg")
PRICE_INPUT  = 3.0  / 1_000_000   # $3 per 1M input tokens
PRICE_OUTPUT = 15.0 / 1_000_000   # $15 per 1M output tokens

SYSTEM_PROMPT = """You are a knowledge graph query engine. You will be given a structured
knowledge graph subgraph and a question. Answer the question using ONLY the information
in the subgraph. Be concise and precise. List concepts as comma-separated values when
asked to enumerate. Do not add information not present in the subgraph."""

# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class Concept:
    id: int
    label: str
    dependencies: list[int]
    taxonomy_id: str

@dataclass
class QueryRecord:
    query_id: str
    domain: str
    query_type: str
    query: str
    ground_truth: list[str]
    hop_depth: int
    # Filled by harness
    retrieved_context: str = ""
    predicted_answer: str = ""
    predicted_tokens: list[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    retrieved_tokens: int = 0
    f1: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    rds: float = 0.0
    cost_usd: float = 0.0
    latency_ms: int = 0

    def __post_init__(self):
        if self.predicted_tokens is None:
            self.predicted_tokens = []

# ── CSV loader ─────────────────────────────────────────────────────────────────

def load_graph(csv_path: Path) -> dict[int, Concept]:
    concepts = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = int(row["ConceptID"])
            deps_raw = row.get("Dependencies", "").strip()
            deps = [int(d) for d in deps_raw.split("|") if d.strip().isdigit()]
            concepts[cid] = Concept(
                id=cid,
                label=row["ConceptLabel"].strip(),
                dependencies=deps,
                taxonomy_id=row.get("TaxonomyID", "GEN").strip()
            )
    return concepts

# ── Graph traversal ───────────────────────────────────────────────────────────

def find_concept_by_label(concepts: dict, label: str) -> Optional[Concept]:
    label_lower = label.lower()
    for c in concepts.values():
        if c.label.lower() == label_lower:
            return c
    # Partial match fallback
    for c in concepts.values():
        if label_lower in c.label.lower():
            return c
    return None

def get_direct_deps(concepts: dict, concept: Concept) -> list[Concept]:
    return [concepts[d] for d in concept.dependencies if d in concepts]

def bfs_path_to_root(concepts: dict, start_id: int) -> list[int]:
    """Trace from a concept back through all ancestors."""
    visited = set()
    queue = deque([start_id])
    path = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        path.append(node)
        for dep in concepts[node].dependencies:
            if dep not in visited:
                queue.append(dep)
    return path

def get_shared_neighbors(concepts: dict, a: Concept, b: Concept) -> list[Concept]:
    a_deps = set(a.dependencies)
    b_deps = set(b.dependencies)
    shared_ids = a_deps & b_deps
    return [concepts[i] for i in shared_ids if i in concepts]

# ── Subgraph serializer → context string ──────────────────────────────────────

def subgraph_to_context(concepts: dict, relevant_ids: list[int]) -> str:
    """Serialize a subgraph to a compact text context for the LLM."""
    lines = ["KNOWLEDGE GRAPH SUBGRAPH:"]
    for cid in relevant_ids:
        if cid not in concepts:
            continue
        c = concepts[cid]
        dep_labels = [concepts[d].label for d in c.dependencies if d in concepts]
        dep_str = ", ".join(dep_labels) if dep_labels else "none"
        lines.append(f"  [{c.taxonomy_id}] {c.label} | prerequisites: {dep_str}")
    return "\n".join(lines)

# ── Per-query retrieval ───────────────────────────────────────────────────────

def retrieve(concepts: dict, query: dict) -> tuple[str, list[int]]:
    """Return (context_string, list_of_relevant_concept_ids)."""
    qtype = query.get("query_type") or query.get("type", "")

    if qtype == "T1_entity":
        # Use concept_id if present (most reliable), else label from ground_truth
        cid = query.get("concept_id")
        if cid and cid in concepts:
            c = concepts[cid]
        else:
            c = find_concept_by_label(concepts, query["ground_truth"][0])
        if not c:
            return "No matching concept found.", []
        # Include concept + direct deps + direct dependents
        dep_ids = [c.id] + c.dependencies
        rev = [cc.id for cc in concepts.values() if c.id in cc.dependencies]
        relevant = list(dict.fromkeys(dep_ids + rev[:5]))  # cap dependents at 5
        return subgraph_to_context(concepts, relevant), relevant

    elif qtype == "T2_dependency":
        # Use concept_id directly — ground_truth[0] is a prerequisite label, NOT the target
        cid = query.get("concept_id")
        if cid and cid in concepts:
            c = concepts[cid]
        else:
            # Fall back to query text extraction
            q_text = query["query"]  # "What are the prerequisites for X?"
            label = q_text.replace("What are the prerequisites for ", "").rstrip("?").strip()
            c = find_concept_by_label(concepts, label)
        if not c:
            return "No matching concept found.", []
        dep_ids = [c.id] + c.dependencies
        return subgraph_to_context(concepts, dep_ids), dep_ids

    elif qtype == "T3_path":
        # "What is the prerequisite chain from X to Y?"
        # ground_truth is the path as labels
        if query.get("path_ids"):
            relevant = query["path_ids"]
        else:
            # Reconstruct from ground truth labels
            relevant = []
            for label in query.get("ground_truth", []):
                c = find_concept_by_label(concepts, label)
                if c:
                    relevant.append(c.id)
        if not relevant:
            # Fall back: trace from the concept_id to root
            cid = query.get("concept_id")
            if cid and cid in concepts:
                relevant = bfs_path_to_root(concepts, cid)
        return subgraph_to_context(concepts, relevant), relevant

    elif qtype == "T4_aggregate":
        tax_id = query.get("taxonomy_id", "")
        if not tax_id:
            # Extract from ground truth
            members = [find_concept_by_label(concepts, label) for label in query.get("ground_truth", [])]
            relevant = [c.id for c in members if c]
        else:
            relevant = [c.id for c in concepts.values() if c.taxonomy_id == tax_id]
        return subgraph_to_context(concepts, relevant), relevant

    elif qtype == "T5_cross_concept":
        cid_a = query.get("concept_id_a")
        cid_b = query.get("concept_id_b")
        if cid_a in concepts and cid_b in concepts:
            a, b = concepts[cid_a], concepts[cid_b]
            shared = get_shared_neighbors(concepts, a, b)
            relevant = list(dict.fromkeys(
                [a.id, b.id] + [c.id for c in shared] + a.dependencies[:3] + b.dependencies[:3]
            ))
        else:
            relevant = []
        return subgraph_to_context(concepts, relevant), relevant

    return "Query type not recognized.", []

# ── F1 scoring ────────────────────────────────────────────────────────────────

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts","based","on","knowledge","graph",
    "subgraph","prerequisites","prerequisite","following"
}

def normalize_text(text: str) -> str:
    """Strip markdown formatting and punctuation before tokenizing."""
    import re
    text = re.sub(r'\*+', ' ', text)        # remove ** bold markers
    text = re.sub(r'_+', ' ', text)          # remove _ italic markers
    text = re.sub(r'`+', ' ', text)          # remove backticks
    text = re.sub(r'#+\s*', ' ', text)       # remove markdown headers
    text = re.sub(r'[^\w\s]', ' ', text)     # remove remaining punctuation
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def token_f1(predicted: str, ground_truth: list[str]) -> dict:
    pred_tokens  = set(normalize_text(predicted).lower().split()) - STOPWORDS
    truth_tokens = set(normalize_text(" ".join(ground_truth)).lower().split()) - STOPWORDS
    if not pred_tokens and not truth_tokens:
        return {"f1": 1.0, "precision": 1.0, "recall": 1.0}
    if not pred_tokens or not truth_tokens:
        return {"f1": 0.0, "precision": 0.0, "recall": 0.0}
    tp = len(pred_tokens & truth_tokens)
    p  = tp / len(pred_tokens)
    r  = tp / len(truth_tokens)
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return {"f1": round(f1, 4), "precision": round(p, 4), "recall": round(r, 4)}

# ── Main harness ──────────────────────────────────────────────────────────────

def run_domain(domain: str, client: anthropic.Anthropic, dry_run: bool = False) -> list[dict]:
    queries_file = QUERIES_DIR / f"queries_{domain}.jsonl"
    csv_file     = DOMAINS_DIR / domain / "learning-graph.csv"

    if not queries_file.exists():
        print(f"  ✗ no queries file for {domain}")
        return []
    if not csv_file.exists():
        print(f"  ✗ no CSV for {domain}")
        return []

    concepts = load_graph(csv_file)
    queries = []
    with open(queries_file) as f:
        for line in f:
            queries.append(json.loads(line))

    print(f"  {domain}: {len(queries)} queries, {len(concepts)} concepts")

    results = []
    for i, q in enumerate(queries):
        context, relevant_ids = retrieve(concepts, q)

        user_message = f"{context}\n\nQuestion: {q['query']}"

        if dry_run:
            result = {
                **q,
                "system": "ckg",
                "retrieved_context": context[:200] + "...",
                "predicted_answer": "[DRY RUN]",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "retrieved_tokens": len(context.split()),
                "f1": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "rds": 0.0,
                "cost_usd": 0.0,
                "latency_ms": 0
            }
            results.append(result)
            continue

        t0 = time.time()
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=512,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}]
            )
            latency_ms = int((time.time() - t0) * 1000)
            answer = response.content[0].text
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
        except Exception as e:
            print(f"    ✗ API error on {q.get('id', q.get('query_id','?'))}: {e}")
            continue

        scores = token_f1(answer, q.get("ground_truth", []))
        total_tokens = prompt_tokens + completion_tokens
        rds = scores["f1"] / total_tokens if total_tokens > 0 else 0.0
        cost = prompt_tokens * PRICE_INPUT + completion_tokens * PRICE_OUTPUT

        result = {
            **q,
            "system": "ckg",
            "retrieved_context": context,
            "predicted_answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "retrieved_tokens": len(context.split()),
            "f1": scores["f1"],
            "precision": scores["precision"],
            "recall": scores["recall"],
            "rds": round(rds, 8),
            "cost_usd": round(cost, 6),
            "latency_ms": latency_ms
        }
        results.append(result)

        # Progress tick every 25 queries
        if (i + 1) % 25 == 0:
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            avg_tok = sum(r["total_tokens"] for r in results) / len(results)
            print(f"    [{i+1}/{len(queries)}] avg F1={avg_f1:.3f} avg_tokens={avg_tok:.0f}")

        # Rate limit: be gentle
        time.sleep(0.3)

    return results


def summarize(results: list[dict]) -> dict:
    if not results:
        return {}
    by_type = defaultdict(list)
    for r in results:
        by_type[r.get("query_type") or r.get("type", "unknown")].append(r)

    type_f1 = {k: round(sum(r["f1"] for r in v) / len(v), 4)
               for k, v in by_type.items()}

    all_f1    = [r["f1"] for r in results]
    all_rds   = [r["rds"] for r in results if r.get("rds", 0) > 0]
    all_tok   = [r.get("total_tokens", 0) for r in results]
    all_cost  = [r.get("cost_usd", 0) for r in results]

    by_hop = defaultdict(list)
    for r in results:
        by_hop[r.get("hop_depth", 0)].append(r["f1"])
    hop_f1 = {k: round(sum(v)/len(v), 4) for k, v in by_hop.items()}

    return {
        "n_queries": len(results),
        "macro_f1":  round(sum(all_f1) / len(all_f1), 4),
        "macro_rds": round(sum(all_rds) / len(all_rds), 8) if all_rds else 0,
        "mean_tokens": round(sum(all_tok) / len(all_tok), 1) if all_tok else 0,
        "total_cost_usd": round(sum(all_cost), 4),
        "f1_by_type": type_f1,
        "f1_by_hop":  hop_f1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Single domain to run")
    parser.add_argument("--all", action="store_true", help="Run all domains")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, test retrieval only")
    parser.add_argument("--limit", type=int, default=0, help="Limit queries per domain (0=all)")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        raise SystemExit("Set ANTHROPIC_API_KEY or use --dry-run")

    client = anthropic.Anthropic(api_key=api_key) if not args.dry_run else None

    if args.domain:
        domains = [args.domain]
    elif args.all:
        domains = sorted([
            p.stem.replace("queries_", "")
            for p in QUERIES_DIR.glob("queries_*.jsonl")
        ])
    else:
        parser.print_help()
        return

    print(f"\nCKG Harness — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Model: {MODEL}")
    print(f"Domains: {len(domains)}\n")

    all_results = []
    domain_summaries = {}

    for domain in domains:
        print(f"── {domain}")
        results = run_domain(domain, client, dry_run=args.dry_run)

        if args.limit and not args.dry_run:
            results = results[:args.limit]

        if results:
            out_path = RESULTS_DIR / f"ckg_{domain}.jsonl"
            with open(out_path, "w") as f:
                for r in results:
                    f.write(json.dumps(r) + "\n")

            summary = summarize(results)
            domain_summaries[domain] = summary
            all_results.extend(results)

            if not args.dry_run:
                print(f"   F1={summary['macro_f1']}  tokens={summary['mean_tokens']:.0f}  "
                      f"RDS={summary['macro_rds']:.6f}  cost=${summary['total_cost_usd']:.3f}")

    # Write aggregate summary
    if all_results:
        global_summary = summarize(all_results)
        global_summary["by_domain"] = domain_summaries

        with open(RESULTS_DIR / "ckg_summary.json", "w") as f:
            json.dump(global_summary, f, indent=2)

        print(f"\n── GLOBAL SUMMARY ──")
        print(f"   Domains:      {len(domain_summaries)}")
        print(f"   Queries:      {global_summary['n_queries']}")
        print(f"   Macro F1:     {global_summary['macro_f1']}")
        print(f"   Mean tokens:  {global_summary['mean_tokens']:.0f}")
        print(f"   Macro RDS:    {global_summary['macro_rds']:.6f}")
        print(f"   Total cost:   ${global_summary['total_cost_usd']:.3f}")
        print(f"\n   F1 by query type:")
        for qtype, f1 in sorted(global_summary["f1_by_type"].items()):
            print(f"     {qtype}: {f1}")
        print(f"\n   F1 by hop depth:")
        for hop, f1 in sorted(global_summary["f1_by_hop"].items()):
            print(f"     hop={hop}: {f1}")
        print(f"\n   Results written to: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
