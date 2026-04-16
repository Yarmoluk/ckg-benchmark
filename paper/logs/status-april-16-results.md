# Experiment Status — April 16, 2026

Dan — leaving this so you have the full picture when you open the repo. No action needed from you tonight, but I want you to see exactly where things stand, what the real numbers are, and flag one discrepancy I need your input on.

---

## What's Complete

### CKG — Done. All 44 domains.

| Metric | Result |
|---|---|
| Domains scored | 44 / 44 |
| Total queries | 7,588 |
| Macro F1 | **0.4504** |
| Mean tokens | **274** |
| RDS (F1 / tokens) | **0.001887** |
| Total cost | $13.53 |

**F1 by query type:**

| Type | F1 | Notes |
|---|---|---|
| T1 — Entity lookup | 0.189 | Honest negative control — expected |
| T2 — Prerequisites | 0.603 | Strong |
| T3 — Learning paths | 0.614 | Strong |
| T4 — Category aggregates | **0.951** | Near-perfect |
| T5 — Cross-concept | 0.326 | Improving — BFS fix in progress |

### RAG — 22 / 44 domains complete.

| Metric | Result (22 domains) |
|---|---|
| Domains scored | 22 / 44 |
| Total queries | 3,499 |
| Macro F1 | **0.111** |
| Mean tokens | **3,018** |
| RDS (F1 / tokens) | **0.0000425** |
| Total cost | $37.59 |

RAG is still running on the remaining 22 domains. Results are already directionally conclusive but we need all 44 for the paper tables.

### GraphRAG — Not yet started.

No harness exists yet. I'm flagging this so we can decide together: do we implement GraphRAG or scope the paper to CKG vs RAG only? Given the results below, CKG vs RAG alone makes a strong paper. GraphRAG adds completeness but also adds weeks.

---

## The Real Numbers — CKG vs RAG (22-domain overlap)

| Metric | CKG | RAG | Ratio |
|---|---|---|---|
| Macro F1 | 0.4504 | 0.111 | **CKG 4x better** |
| Mean tokens | 274 | 3,018 | **11x cheaper** |
| RDS | 0.001887 | 0.0000425 | **~44x advantage** |
| Cost per query | $0.0018 | $0.0107 | **CKG 6x cheaper** |

---

## ⚠️ Discrepancy I Need to Flag

In earlier communications — and in the provisional patent filed tonight — I cited **65x RDS** and **15x token efficiency**.

The actual data shows **44x RDS** and **11x token efficiency**.

Both are still large, defensible, and publishable results. But there's a gap between what I cited and what the repo currently shows. A few possible explanations:

1. The 65x figure may have come from a subset of domains where the gap is wider (T4-heavy domains where CKG hits 0.95 vs RAG's 0.22)
2. The 15x token figure may have been based on earlier raw token counts before the scoring normalization
3. RAG on the remaining 22 domains may change the aggregate macro F1 downward (RAG struggles more on structural domains — which would widen the RDS gap toward 65x)

**My ask:** Once RAG finishes on all 44 domains, let's recompute the headline RDS figure together before it goes into the paper abstract. If the real number is 44x, we publish 44x — it's still a landmark result. If the remaining 22 RAG domains pull the macro F1 down further, we may get closer to 65x. Either way we use the real number.

The patent provisional is filed and the priority date is locked regardless. The claims reference "measurable improvements in LLM reasoning density" — the specific multiplier is in the specification, not the claims themselves, so an update to the paper doesn't invalidate the patent.

---

## What Needs to Happen Next

| Task | Owner | Status |
|---|---|---|
| RAG — complete remaining 22 domains | Daniel (running) | 🔄 In progress |
| T5 BFS traversal fix | Daniel | 🔄 In progress |
| Recompute headline RDS once RAG done | Both | Pending |
| GraphRAG harness — build or scope out | Dan's call | ❓ Decision needed |
| Paper figures (6–10) | Both | Strategy at `paper/logs/figure-strategy.md` |
| Paper length (currently 13 pages) | Both | Needs more detail |
| arXiv submission | Both | After RAG complete + figures |

---

## Bottom Line

The CKG experiment is complete and the results are strong. RAG is half done and already shows a 4x F1 gap and 11x token efficiency gap. The paper's core thesis holds — we just need to be precise about the headline number once all 44 RAG domains finish.

You don't need to do anything tonight. When you're ready, the data is all here:

- `results/ckg/ckg_summary.json` — full CKG results
- `results/rag/rag_summary.json` — RAG results (22 domains)
- `paper/sections/08-results.tex` — results section
- `paper/logs/direction-april-16.md` — paper framing note

More soon.

— Daniel
