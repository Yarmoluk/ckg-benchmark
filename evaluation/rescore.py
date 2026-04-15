"""
Re-score saved harness results with the fixed token_f1 scorer.

The F1 scorer was originally broken in two ways:
1. Markdown bold markers (**word**) prevented token matching
2. Stopword list was too narrow

This script re-reads all saved JSONL result files, recomputes F1/RDS/CPCA
using the corrected scorer, and writes updated files in-place.

No API calls are made. Only the scoring fields are updated.

Usage:
    python evaluation/rescore.py --system ckg
    python evaluation/rescore.py --system rag
    python evaluation/rescore.py --system ckg rag
"""

import json
import re
import argparse
import glob
from pathlib import Path
from collections import defaultdict

RESULTS_DIR  = Path("results")
PRICE_INPUT  = 3.0  / 1_000_000
PRICE_OUTPUT = 15.0 / 1_000_000

STOPWORDS = {
    "what","is","the","a","an","of","for","are","in","and","or","to","with",
    "how","does","related","which","these","those","all","list","describe",
    "explain","between","concept","concepts","based","on","knowledge","graph",
    "subgraph","prerequisites","prerequisite","following"
}


def normalize_text(text: str) -> str:
    text = re.sub(r'\*+', ' ', text)
    text = re.sub(r'_+', ' ', text)
    text = re.sub(r'`+', ' ', text)
    text = re.sub(r'#+\s*', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
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


def rescore_file(path: Path) -> dict:
    """Re-score a single domain JSONL file. Returns before/after stats."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not records:
        return {}

    old_f1_sum = 0
    new_f1_sum = 0

    updated = []
    for r in records:
        predicted = r.get("predicted_answer", "")
        ground_truth = r.get("ground_truth", [])

        old_f1 = r.get("f1", 0)
        old_f1_sum += old_f1

        if not predicted or predicted == "[DRY RUN]":
            updated.append(r)
            new_f1_sum += old_f1
            continue

        scores = token_f1(predicted, ground_truth)
        new_f1 = scores["f1"]
        new_f1_sum += new_f1

        total_tokens = r.get("total_tokens", r.get("prompt_tokens", 0) + r.get("completion_tokens", 0))
        rds = new_f1 / total_tokens if total_tokens > 0 else 0.0

        r_updated = {
            **r,
            "f1": new_f1,
            "precision": scores["precision"],
            "recall": scores["recall"],
            "rds": round(rds, 8),
        }
        updated.append(r_updated)

    # Write back
    with open(path, "w") as f:
        for r in updated:
            f.write(json.dumps(r) + "\n")

    n = len(records)
    return {
        "n": n,
        "old_f1": round(old_f1_sum / n, 4),
        "new_f1": round(new_f1_sum / n, 4),
        "delta": round((new_f1_sum - old_f1_sum) / n, 4)
    }


def summarize_domain(path: Path) -> dict:
    """Compute summary stats for a rescored domain file."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not records:
        return {}

    by_type = defaultdict(list)
    for r in records:
        qt = r.get("query_type") or r.get("type", "unknown")
        by_type[qt].append(r)

    all_f1  = [r["f1"] for r in records]
    all_rds = [r.get("rds", 0) for r in records if r.get("rds", 0) > 0]
    all_tok = [r.get("total_tokens", 0) for r in records]
    all_cost = [r.get("cost_usd", 0) for r in records]

    return {
        "n_queries": len(records),
        "macro_f1": round(sum(all_f1) / len(all_f1), 4),
        "macro_rds": round(sum(all_rds) / len(all_rds), 8) if all_rds else 0,
        "mean_tokens": round(sum(all_tok) / len(all_tok), 1) if all_tok else 0,
        "total_cost_usd": round(sum(all_cost), 4),
        "f1_by_type": {k: round(sum(r["f1"] for r in v) / len(v), 4) for k, v in by_type.items()},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", nargs="+", default=["ckg"],
                        help="Systems to rescore")
    args = parser.parse_args()

    for system in args.system:
        pattern = RESULTS_DIR / system / f"{system}_*.jsonl"
        files = [p for p in sorted(Path(".").glob(str(pattern)))
                 if "summary" not in p.name]

        if not files:
            print(f"No result files found for {system}")
            continue

        print(f"\n── Rescoring {system} ({len(files)} domains) ──")
        print(f"{'Domain':<35} {'Old F1':>7} {'New F1':>7} {'Delta':>7}")
        print("-" * 60)

        all_summaries = {}
        total_old = 0
        total_new = 0
        total_n   = 0

        for f in files:
            domain = f.stem.replace(f"{system}_", "")
            stats = rescore_file(f)
            if stats:
                print(f"  {domain:<33} {stats['old_f1']:>7.4f} {stats['new_f1']:>7.4f} "
                      f"{stats['delta']:>+7.4f}")
                total_old += stats["old_f1"] * stats["n"]
                total_new += stats["new_f1"] * stats["n"]
                total_n   += stats["n"]

                # Rebuild domain summary
                all_summaries[domain] = summarize_domain(f)

        if total_n > 0:
            print(f"\n  {'TOTAL':<33} "
                  f"{total_old/total_n:>7.4f} "
                  f"{total_new/total_n:>7.4f} "
                  f"{(total_new-total_old)/total_n:>+7.4f}")

        # Rebuild aggregate summary
        all_records = []
        for f in files:
            if "summary" in f.name:
                continue
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            all_records.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

        if all_records:
            all_f1  = [r["f1"] for r in all_records]
            all_rds = [r.get("rds", 0) for r in all_records if r.get("rds", 0) > 0]
            all_tok = [r.get("total_tokens", 0) for r in all_records]
            all_cost = [r.get("cost_usd", 0) for r in all_records]
            by_type = defaultdict(list)
            by_hop  = defaultdict(list)
            for r in all_records:
                qt = r.get("query_type") or r.get("type", "unknown")
                by_type[qt].append(r["f1"])
                by_hop[r.get("hop_depth", 0)].append(r["f1"])

            global_summary = {
                "n_queries": len(all_records),
                "macro_f1": round(sum(all_f1) / len(all_f1), 4),
                "macro_rds": round(sum(all_rds) / len(all_rds), 8) if all_rds else 0,
                "mean_tokens": round(sum(all_tok) / len(all_tok), 1) if all_tok else 0,
                "total_cost_usd": round(sum(all_cost), 4),
                "f1_by_type": {k: round(sum(v) / len(v), 4) for k, v in by_type.items()},
                "f1_by_hop":  {k: round(sum(v) / len(v), 4) for k, v in by_hop.items()},
                "by_domain": all_summaries,
                "scorer_version": "v2_markdown_stripped"
            }

            summary_path = RESULTS_DIR / system / f"{system}_summary.json"
            import json as _json
            summary_path.write_text(_json.dumps(global_summary, indent=2))
            print(f"\n  Summary saved → {summary_path}")

            print(f"\n  F1 by query type (post-rescore):")
            for qt in sorted(global_summary["f1_by_type"]):
                print(f"    {qt:<28} {global_summary['f1_by_type'][qt]:.4f}")


if __name__ == "__main__":
    main()
