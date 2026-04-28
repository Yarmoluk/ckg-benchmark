"""
Add BERTScore to existing benchmark results.

Reads saved JSONL result files, computes BERTScore (P/R/F1) for each record,
and writes back updated files with bert_p, bert_r, bert_f1, bert_cpca added.

No API calls — operates entirely on saved results.

Why BERTScore:
  Token F1 penalises paraphrase and partial matches. BERTScore uses contextual
  embeddings (roberta-large) and captures semantic similarity, neutralising the
  "you're penalising prose" objection. Running both metrics side-by-side lets
  the paper show CKG's advantage holds under both exact and semantic scoring.

CPCA with BERTScore:
  bert_cpca = cost_usd / bert_f1
  Directly translates to "our system costs X per semantically-correct answer"
  — the enterprise buying-decision framing Hohman described.

Usage:
    python evaluation/add_bertscore.py --system ckg
    python evaluation/add_bertscore.py --system ckg rag graphrag
    python evaluation/add_bertscore.py --system ckg --model roberta-large
    python evaluation/add_bertscore.py --system ckg --dry-run
"""

import json
import argparse
import math
from collections import defaultdict
from pathlib import Path

RESULTS_DIR  = Path("results")
PRICE_INPUT  = 3.0  / 1_000_000
PRICE_OUTPUT = 15.0 / 1_000_000

QUERY_TYPES = ["T1_entity", "T2_dependency", "T3_path", "T4_aggregate", "T5_cross_concept"]


def load_records(path: Path) -> list[dict]:
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def score_file(
    path: Path,
    model_type: str,
    batch_size: int,
    device: str,
    dry_run: bool,
) -> dict:
    """Add bert_p, bert_r, bert_f1, bert_cpca to every record in a JSONL file.
    Returns before/after summary stats."""
    from bert_score import score as bert_score_fn

    records = load_records(path)
    if not records:
        return {}

    candidates = []
    references = []
    valid_indices = []

    for i, r in enumerate(records):
        pred = r.get("predicted_answer", "").strip()
        gt   = r.get("ground_truth", [])
        ref  = " ".join(gt) if isinstance(gt, list) else str(gt)
        if pred and ref and pred != "[DRY RUN]":
            candidates.append(pred)
            references.append(ref)
            valid_indices.append(i)

    if not candidates:
        return {"n": len(records), "skipped": len(records)}

    if dry_run:
        for i in valid_indices:
            records[i]["bert_p"]    = 0.0
            records[i]["bert_r"]    = 0.0
            records[i]["bert_f1"]   = 0.0
            records[i]["bert_cpca"] = None
        return {"n": len(records), "dry_run": True}

    # Batch compute BERTScore — roberta-large by default
    P, R, F = bert_score_fn(
        candidates,
        references,
        model_type=model_type,
        device=device,
        batch_size=batch_size,
        lang="en",
        verbose=False,
    )

    old_f1_sum = 0.0
    new_f1_sum = 0.0

    # Write scores back to records
    for list_pos, rec_idx in enumerate(valid_indices):
        r = records[rec_idx]
        bp   = round(float(P[list_pos]), 4)
        br   = round(float(R[list_pos]), 4)
        bf1  = round(float(F[list_pos]), 4)
        cost = r.get("cost_usd", 0.0)
        bert_cpca = round(cost / bf1, 8) if bf1 > 0 else None

        old_f1_sum += r.get("f1", 0.0)
        new_f1_sum += bf1

        records[rec_idx]["bert_p"]    = bp
        records[rec_idx]["bert_r"]    = br
        records[rec_idx]["bert_f1"]   = bf1
        records[rec_idx]["bert_cpca"] = bert_cpca

    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    n = len(valid_indices)
    return {
        "n":          n,
        "old_f1":     round(old_f1_sum / n, 4),
        "bert_f1":    round(new_f1_sum / n, 4),
        "delta":      round((new_f1_sum - old_f1_sum) / n, 4),
    }


def print_comparison_table(systems: list[str]):
    """Print a side-by-side token F1 vs BERTScore comparison table by query type."""
    print("\n── Comparison: Token F1 vs BERTScore by Query Type ──")
    header = f"  {'System':<12} {'Query Type':<22} {'Token F1':>9} {'BERT F1':>9} {'BERT CPCA':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for system in systems:
        pattern = RESULTS_DIR / system / f"{system}_*.jsonl"
        all_records = []
        for fpath in sorted(Path(".").glob(str(pattern))):
            if "summary" in fpath.name:
                continue
            all_records.extend(load_records(fpath))

        if not all_records:
            continue

        by_type = defaultdict(list)
        for r in all_records:
            qt = r.get("query_type") or r.get("type", "unknown")
            by_type[qt].append(r)

        for qt in QUERY_TYPES:
            recs = by_type.get(qt, [])
            if not recs:
                continue
            tok_f1  = round(sum(r.get("f1", 0)       for r in recs) / len(recs), 4)
            bert_f1 = round(sum(r.get("bert_f1", 0)  for r in recs) / len(recs), 4)
            # Mean CPCA excluding infinities
            cpca_vals = [r["bert_cpca"] for r in recs if r.get("bert_cpca") is not None]
            mean_cpca = round(sum(cpca_vals) / len(cpca_vals), 6) if cpca_vals else None
            cpca_str  = f"${mean_cpca:.6f}" if mean_cpca else "—"
            print(f"  {system:<12} {qt:<22} {tok_f1:>9.4f} {bert_f1:>9.4f} {cpca_str:>12}")

        # System totals
        tok_f1_all  = [r.get("f1", 0) for r in all_records]
        bert_f1_all = [r.get("bert_f1", 0) for r in all_records if "bert_f1" in r]
        cpca_all    = [r["bert_cpca"] for r in all_records if r.get("bert_cpca")]
        tok_mean    = round(sum(tok_f1_all) / len(tok_f1_all), 4) if tok_f1_all else 0
        bert_mean   = round(sum(bert_f1_all) / len(bert_f1_all), 4) if bert_f1_all else 0
        cpca_mean   = round(sum(cpca_all) / len(cpca_all), 6) if cpca_all else None
        cpca_str    = f"${cpca_mean:.6f}" if cpca_mean else "—"
        print(f"  {system:<12} {'MACRO':>22} {tok_mean:>9.4f} {bert_mean:>9.4f} {cpca_str:>12}")
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", nargs="+", default=["ckg"],
                        help="Systems to score (ckg, rag, graphrag)")
    parser.add_argument("--model", default="roberta-large",
                        help="HuggingFace model for BERTScore (default: roberta-large)")
    parser.add_argument("--batch-size", type=int, default=64,
                        help="BERTScore batch size (default: 64, lower if OOM)")
    parser.add_argument("--device", default=None,
                        help="Device: cuda, mps, cpu (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip computation, write zeros — test pipeline only")
    args = parser.parse_args()

    # Auto-detect device
    device = args.device
    if device is None:
        try:
            import torch
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        except ImportError:
            device = "cpu"

    print(f"\nBERTScore — model={args.model}  device={device}  "
          f"batch={args.batch_size}  {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("Note: first run downloads ~500MB model weights to ~/.cache/huggingface\n")

    for system in args.system:
        pattern = RESULTS_DIR / system / f"{system}_*.jsonl"
        files = [p for p in sorted(Path(".").glob(str(pattern)))
                 if "summary" not in p.name]

        if not files:
            print(f"No result files for {system}")
            continue

        print(f"── {system} ({len(files)} domains) ──")
        print(f"  {'Domain':<35} {'n':>5} {'Token F1':>9} {'BERT F1':>9} {'Delta':>7}")
        print("  " + "-" * 70)

        total_old = 0
        total_new = 0
        total_n   = 0

        for fpath in files:
            domain = fpath.stem.replace(f"{system}_", "")
            stats  = score_file(fpath, args.model, args.batch_size, device, args.dry_run)
            if stats and not stats.get("dry_run") and not stats.get("skipped"):
                delta_str = f"{stats['delta']:>+.4f}"
                print(f"  {domain:<35} {stats['n']:>5} "
                      f"{stats['old_f1']:>9.4f} {stats['bert_f1']:>9.4f} {delta_str:>7}")
                total_old += stats["old_f1"] * stats["n"]
                total_new += stats["bert_f1"] * stats["n"]
                total_n   += stats["n"]
            elif stats.get("dry_run"):
                print(f"  {domain:<35} {'[dry run]':>5}")
            else:
                print(f"  {domain:<35} {'[skip]':>5}")

        if total_n > 0:
            print(f"\n  {'MACRO':<35} {total_n:>5} "
                  f"{total_old/total_n:>9.4f} {total_new/total_n:>9.4f} "
                  f"{(total_new-total_old)/total_n:>+7.4f}")

    print_comparison_table(args.system)


if __name__ == "__main__":
    main()
