# Cost Reconciliation — v0.6.2 internal correction

Date: 2026-08-01. Scope: cost figures only, plus one reproducibility finding.
The cost correction was originally staged as
`table3_tokenomics_v0.6.3-corrected.csv`. The correction is now present in
`analyze_results.py` and `table3_tokenomics.csv` for reference, but paper and
public narrative surfaces are intentionally left at the prior collaborated text
until there is an explicit publishing decision.

## 1. What was wrong

All harnesses call the same model (`claude-haiku-4-5-20251001`), but priced it
differently:

| harness | constants used | actual Haiku 4.5 price |
|---|---|---|
| ckg_harness, krb_eval | $0.80 / $4.00 per MTok | $1.00 / $5.00 |
| rag_harness, graphrag_harness, analyzers | $3.00 / $15.00 (Sonnet) | $1.00 / $5.00 |

A 3.75× asymmetry favoring CKG, baked into the stored `cost_usd` of every
result record. `analyze_results.py` summed those stored values, so the
published cost comparison measured the constants, not the systems.

## 2. The fix (structural)

- `analyze_results.py` now DERIVES cost from `prompt_tokens`/`completion_tokens`
  at analysis time and never trusts stored `cost_usd`.
- Records lacking the split but carrying `total_tokens` are repriced with the
  documented 85% input / 15% output estimate. Only records without usable token
  counts fall back to stored cost and are counted in `n_cost_fallback`.

## 3. Corrected numbers (current artifacts, uniform pricing)

| system | n | macro F1 | total cost | vs published cost |
|---|---:|---:|---:|---:|
| ckg | 8,121 | 0.4926 | **$4.39** | $7.81 |
| rag | 7,414 | 0.1223 | **$26.26** | $76.23 |
| graphrag | 2,683 | 0.1200 | **$14.81**† | $44.43 |

† graphrag records store no prompt/completion split, so the analyzer uses the
85% input / 15% output estimate used by the GraphRAG harness when writing
`cost_usd`. The analyzer now reports 2,683 total-token estimates and 0
stored-cost fallbacks for GraphRAG.

**Headline change: RAG/CKG cost ratio ≈ 9.8× published → 6.0× corrected.**
CKG's cost rises under honest pricing (output is 26% of its tokens and 64% of
its true cost); RAG's falls by 3×. The 11× token ratio (264 vs 2,986) is a
measurement, not a price assumption — unchanged. Robustness: deduplicating
retried queries (148 ckg / 137 rag / 38 graphrag records) moves no ratio by
more than 0.02.

## 4. Reproducibility finding — record counts and F1 drift

The current results directory does not reproduce locked v0.6.2:

| | v0.6.2 published | current artifacts |
|---|---:|---:|
| ckg queries | 7,758 | 8,121 |
| ckg macro F1 | 0.4709 | 0.4926 |
| ckg stored-cost sum | $7.81 | $3.51 |

F1 is untouched by any pricing change, so the result files were re-run or
extended after the tables were locked. The stored-cost sum ($3.51 at the
$0.80/$4.00 constants) cannot produce $7.81 under any subset, confirming the
drift. Direction is favorable (current F1 is higher), but a benchmark whose
locked tables cannot be regenerated from its artifacts is exposed to exactly
the critique this project levels at LOCOMO-based evaluations.

## 5. Publishing decision

1. Decide: re-lock on current artifacts (n=8,121, F1 0.4926, cost $4.39) or
   re-run all three systems from scratch for a clean lineage.
2. If publishing the corrected aggregate, update paper + site: cost claim
   $76.23/$7.81 → corrected pair; ratio ~6×.
3. Regenerate graphrag with the fixed harness so the split is stored and the
   fallback path goes quiet.
4. Bump `\paperversion` only when the corrected aggregate is intentionally
   promoted into the paper.
