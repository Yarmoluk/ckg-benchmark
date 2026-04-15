"""
Results Analysis — generate paper tables and figures from harness outputs.

Usage:
    python evaluation/analyze_results.py --systems ckg           # CKG only
    python evaluation/analyze_results.py --systems ckg rag        # after RAG run
    python evaluation/analyze_results.py --systems ckg rag graphrag  # all three

Outputs:
    results/tables/table1_macro_f1.csv       -- Table 1: Macro F1, RDS, tokens
    results/tables/table2_by_query_type.csv  -- Table 2: F1 by T1-T5
    results/tables/table3_tokenomics.csv     -- Table 3: Token counts and RDS
    results/tables/table4_hop_degradation.csv -- Table 4: F1 by hop depth
    results/tables/table5_structural.csv     -- Table 5: RP, HR, BC
    results/tables/structure_premium.csv     -- Structure Premium per domain
    results/figures/data/                    -- JSON data files for figure scripts
"""

import json
import os
import csv
import glob
import math
from collections import defaultdict
from pathlib import Path

RESULTS_DIR   = Path("results")
TABLES_DIR    = Path("results/tables")
FIG_DATA_DIR  = Path("results/figures/data")
DOMAINS_DIR   = Path("benchmark/domains")

PRICE_INPUT  = 3.0  / 1_000_000
PRICE_OUTPUT = 15.0 / 1_000_000

QUERY_TYPES = ["T1_entity", "T2_dependency", "T3_path", "T4_aggregate", "T5_cross_concept"]


def load_system_results(system: str) -> dict[str, list[dict]]:
    """Load all domain results for a system. Returns {domain: [records]}."""
    pattern = RESULTS_DIR / system / f"{system}_*.jsonl"
    by_domain = {}
    for f in glob.glob(str(pattern)):
        if "summary" in f:
            continue
        domain = Path(f).stem.replace(f"{system}_", "")
        records = []
        with open(f) as fh:
            for line in fh:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        if records:
            by_domain[domain] = records
    return by_domain


def compute_domain_stats(records: list[dict]) -> dict:
    """Compute per-domain statistics."""
    if not records:
        return {}

    by_type = defaultdict(list)
    by_hop  = defaultdict(list)
    for r in records:
        qt = r.get("query_type") or r.get("type", "unknown")
        by_type[qt].append(r)
        by_hop[r.get("hop_depth", 0)].append(r)

    all_f1   = [r["f1"] for r in records]
    all_rds  = [r.get("rds", 0) for r in records if r.get("rds", 0) > 0]
    all_tok  = [r.get("total_tokens", 0) for r in records]
    all_cost = [r.get("cost_usd", 0) for r in records]
    all_ret  = [r.get("retrieved_tokens", 0) for r in records]

    type_f1 = {k: round(sum(r["f1"] for r in v) / len(v), 4) for k, v in by_type.items()}
    hop_f1  = {k: round(sum(v) / len(v), 4) for k, v in
               {h: [r["f1"] for r in rs] for h, rs in by_hop.items()}.items()}

    macro_f1  = sum(all_f1) / len(all_f1)
    mean_tok  = sum(all_tok) / len(all_tok) if all_tok else 0
    mean_ret  = sum(all_ret) / len(all_ret) if all_ret else 0
    macro_rds = sum(all_rds) / len(all_rds) if all_rds else 0
    total_cost = sum(all_cost)

    # Context Utilization Rate: fraction of retrieved tokens that appear in answer
    # Proxy: min(relevant_tokens, retrieved_tokens) / retrieved_tokens
    # We use retrieved_tokens vs total_tokens as a CUR proxy
    cur_vals = []
    for r in records:
        ret = r.get("retrieved_tokens", 0)
        total = r.get("total_tokens", 0)
        if total > 0 and ret > 0:
            # CUR = retrieved / total (fraction of context that is retrieved content)
            cur_vals.append(min(ret, total) / total)
    mean_cur = sum(cur_vals) / len(cur_vals) if cur_vals else 0

    # CPCA: cost / F1 (cost per unit of correctness)
    cpca_vals = [r.get("cost_usd", 0) / r["f1"] for r in records if r.get("f1", 0) > 0]
    mean_cpca = sum(cpca_vals) / len(cpca_vals) if cpca_vals else float("inf")

    # Hallucination Rate proxy: F1 == 0 on T1 with non-empty answer
    # (True HR requires concept-set comparison; this is a proxy)
    hr_count = sum(1 for r in records
                   if (r.get("type") or r.get("query_type","")).startswith("T")
                   and r.get("f1", 0) == 0
                   and len(r.get("predicted_answer", "")) > 50)
    hr = hr_count / len(records) if records else 0

    return {
        "n": len(records),
        "macro_f1": round(macro_f1, 4),
        "macro_rds": round(macro_rds, 8),
        "mean_tokens": round(mean_tok, 1),
        "mean_retrieved_tokens": round(mean_ret, 1),
        "total_cost_usd": round(total_cost, 4),
        "mean_cur": round(mean_cur, 4),
        "mean_cpca": round(mean_cpca, 6) if math.isfinite(mean_cpca) else None,
        "f1_by_type": type_f1,
        "f1_by_hop": hop_f1,
        "hr_proxy": round(hr, 4),
    }


def load_dag_richness() -> dict[str, float]:
    """Compute dag_richness = (edges/concepts) * mean_indegree / (orphan_rate + 0.01)."""
    richness = {}
    for domain_path in DOMAINS_DIR.iterdir():
        csv_path = domain_path / "learning-graph.csv"
        if not csv_path.exists():
            continue
        concepts = []
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                deps_raw = row.get("Dependencies", "").strip()
                deps = [d.strip() for d in deps_raw.split("|") if d.strip().isdigit()]
                concepts.append({"id": int(row["ConceptID"]), "deps": deps})

        n = len(concepts)
        if n == 0:
            continue
        n_edges = sum(len(c["deps"]) for c in concepts)
        indegree = defaultdict(int)
        for c in concepts:
            for d in c["deps"]:
                indegree[d] += 1
        mean_ind = sum(indegree.values()) / len(indegree) if indegree else 0
        orphan_rate = sum(1 for c in concepts if not c["deps"]) / n
        edge_ratio = n_edges / n
        r = edge_ratio * mean_ind / (orphan_rate + 0.01)
        richness[domain_path.name] = round(r, 4)
    return richness


def write_csv(path: Path, headers: list, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print(f"  → {path}")


def analyze(systems: list[str]):
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load all results
    all_data = {}
    for sys in systems:
        data = load_system_results(sys)
        all_data[sys] = data
        print(f"{sys}: {len(data)} domains loaded")

    dag_richness = load_dag_richness()

    # ── Table 1: Macro F1, Mean Tokens, RDS, Cost ──────────────────────────────
    print("\nGenerating Table 1 (Macro metrics)...")
    rows_t1 = []
    for sys in systems:
        for domain, records in sorted(all_data[sys].items()):
            s = compute_domain_stats(records)
            rows_t1.append([
                sys, domain,
                s["n"], s["macro_f1"], s["macro_rds"],
                s["mean_tokens"], s["total_cost_usd"],
                s.get("mean_cur", ""), s.get("mean_cpca", ""),
            ])
    write_csv(TABLES_DIR / "table1_macro_f1.csv",
              ["system", "domain", "n_queries", "macro_f1", "macro_rds",
               "mean_tokens", "total_cost_usd", "mean_cur", "mean_cpca"],
              rows_t1)

    # ── Table 2: F1 by query type ───────────────────────────────────────────────
    print("Generating Table 2 (F1 by query type)...")
    rows_t2 = []
    for sys in systems:
        # Aggregate across all domains
        by_type = defaultdict(list)
        for records in all_data[sys].values():
            for r in records:
                qt = r.get("query_type") or r.get("type", "unknown")
                by_type[qt].append(r["f1"])
        row = [sys]
        for qt in QUERY_TYPES:
            vals = by_type.get(qt, [])
            row.append(round(sum(vals) / len(vals), 4) if vals else "")
        rows_t2.append(row)
    write_csv(TABLES_DIR / "table2_by_query_type.csv",
              ["system"] + QUERY_TYPES, rows_t2)

    # ── Table 3: Token counts and RDS ratios ────────────────────────────────────
    print("Generating Table 3 (Tokenomics)...")
    system_agg = {}
    for sys in systems:
        all_records = [r for records in all_data[sys].values() for r in records]
        system_agg[sys] = compute_domain_stats(all_records)

    rows_t3 = []
    for sys in systems:
        s = system_agg[sys]
        rows_t3.append([
            sys, s["n"], s["macro_f1"],
            s["mean_tokens"], s["mean_retrieved_tokens"],
            s["macro_rds"], s["total_cost_usd"],
        ])
    write_csv(TABLES_DIR / "table3_tokenomics.csv",
              ["system", "n_queries", "macro_f1", "mean_total_tokens",
               "mean_retrieved_tokens", "macro_rds", "total_cost_usd"],
              rows_t3)

    # RDS ratios (if multiple systems)
    if len(systems) >= 2:
        print("\nRDS ratios:")
        base = system_agg[systems[-1]]["macro_rds"]  # last system as denominator
        for sys in systems[:-1]:
            ratio = system_agg[sys]["macro_rds"] / base if base > 0 else "N/A"
            print(f"  {sys} / {systems[-1]}: {ratio:.1f}x")

    # ── Table 4: Hop-depth F1 degradation ───────────────────────────────────────
    print("Generating Table 4 (Hop-depth degradation)...")
    rows_t4 = []
    for sys in systems:
        by_hop = defaultdict(list)
        for records in all_data[sys].values():
            for r in records:
                by_hop[r.get("hop_depth", 0)].append(r["f1"])
        row = [sys]
        for hop in range(6):
            vals = by_hop.get(hop, [])
            row.append(round(sum(vals) / len(vals), 4) if vals else "")
        rows_t4.append(row)
    write_csv(TABLES_DIR / "table4_hop_degradation.csv",
              ["system"] + [f"hop_{k}" for k in range(6)], rows_t4)

    # ── Structure Premium analysis ──────────────────────────────────────────────
    print("Generating Structure Premium data...")
    if "ckg" in all_data:
        rows_sp = []
        for domain, records in sorted(all_data["ckg"].items()):
            s   = compute_domain_stats(records)
            r_d = dag_richness.get(domain, 0)
            # RDS ratio vs overall mean (structure premium proxy)
            rows_sp.append([
                domain, s["macro_rds"], s["macro_f1"],
                s["mean_tokens"], r_d
            ])
        write_csv(TABLES_DIR / "structure_premium.csv",
                  ["domain", "macro_rds", "macro_f1", "mean_tokens", "dag_richness"],
                  rows_sp)

    # ── Figure data exports ─────────────────────────────────────────────────────
    print("Exporting figure data...")

    # F1 by hop depth (for hop-degradation figure)
    fig_hop = {}
    for sys in systems:
        by_hop = defaultdict(list)
        for records in all_data[sys].values():
            for r in records:
                by_hop[r.get("hop_depth", 0)].append(r["f1"])
        fig_hop[sys] = {str(k): round(sum(v)/len(v), 4) for k, v in sorted(by_hop.items())}
    (FIG_DATA_DIR / "hop_degradation.json").write_text(json.dumps(fig_hop, indent=2))

    # Per-domain RDS and richness (for structure premium scatter)
    fig_sp = {}
    for sys in systems:
        fig_sp[sys] = {}
        for domain, records in all_data[sys].items():
            s = compute_domain_stats(records)
            fig_sp[sys][domain] = {
                "rds": s["macro_rds"],
                "f1":  s["macro_f1"],
                "tokens": s["mean_tokens"],
                "dag_richness": dag_richness.get(domain, 0)
            }
    (FIG_DATA_DIR / "per_domain_stats.json").write_text(json.dumps(fig_sp, indent=2))

    # F1 by query type (for bar chart)
    fig_types = {}
    for sys in systems:
        by_type = defaultdict(list)
        for records in all_data[sys].values():
            for r in records:
                qt = r.get("query_type") or r.get("type", "unknown")
                by_type[qt].append(r["f1"])
        fig_types[sys] = {qt: round(sum(v)/len(v), 4) for qt, v in by_type.items()}
    (FIG_DATA_DIR / "f1_by_type.json").write_text(json.dumps(fig_types, indent=2))

    print("\n── Summary ──────────────────────────────────────────────")
    for sys in systems:
        s = system_agg[sys]
        print(f"  {sys:<12}  F1={s['macro_f1']:.4f}  "
              f"tokens={s['mean_tokens']:.0f}  "
              f"RDS={s['macro_rds']:.6f}  "
              f"cost=${s['total_cost_usd']:.2f}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", nargs="+", default=["ckg"],
                        choices=["ckg", "rag", "graphrag"],
                        help="Systems to analyze")
    args = parser.parse_args()
    analyze(args.systems)


if __name__ == "__main__":
    main()
