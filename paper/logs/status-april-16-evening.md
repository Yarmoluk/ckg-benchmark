# Status Update — April 16, 2026 (Evening)

Dan — everything you asked about is now in the repo. Here's exactly where to find it.

---

## What Just Landed

### Compressed Markdown Examples — `examples/`

This is what you said you couldn't find. It's here now:

```
examples/
  README.md                  ← efficiency table + format explanation
  ckg_contexts/
    T1_entity_lookup.md      ← 243 tokens, F1 0.189 (negative control)
    T2_prerequisites.md      ← 197 tokens, F1 0.603
    T3_learning_path.md      ← 325 tokens, F1 0.614
    T4_category_aggregate.md ← 573 tokens, F1 0.951 (near-perfect)
    T5_cross_concept.md      ← 334 tokens, F1 0.326
```

Each file shows the exact structured text sent to Claude, the token count, the F1, and an explanation. This is the `.md` delivery format the patent covers.

---

### RAG — Final Numbers

`results/rag/rag_summary.json` — 40 of 44 domains (4 have no corpus, final).

| Metric | CKG | RAG | Ratio |
|---|---|---|---|
| Macro F1 | 0.4504 | 0.1225 | **3.7×** |
| Mean tokens | 274 | 2,983 | **10.9×** |
| RDS | 0.001887 | 0.0000411 | **45.9×** |
| Run cost | $13.53 | $72.58 | CKG 81% cheaper |

**On the 65x figure:** The provisional patent cited 65x RDS. The actual full-dataset number is **45.9x**. This is still a landmark result. The discrepancy likely came from a subset analysis on T4-heavy domains. I've updated the paper to use 45.9x. We should decide together on the final abstract number — once GraphRAG results are in, the full 3-way comparison may shift it.

---

### Paper Figures — 5 New Figures Generated

`paper/figures/` now has:

| File | Description |
|---|---|
| `fig3_f1_by_query_type.png` | Grouped bar: F1 by T1–T5, CKG vs RAG |
| `fig4_rds_comparison.png` | RDS comparison + token efficiency side-by-side |
| `fig5_hop_degradation.png` | F1 vs hop depth degradation curves |
| `fig7_token_composition.png` | Token composition donuts (RAG vs CKG) |
| `fig8_structure_premium.png` | Structure Premium scatter (RDS vs DAG richness) |

All wired into `paper/sections/08-results.tex` with captions and labels.

---

### GraphRAG

`evaluation/graphrag_harness.py` is built and indexing calculus right now. No OpenAI key needed — runs local sentence-transformer embeddings via `evaluation/embed_server.py`. 

Full domain run pending. Expected result: higher quality than RAG but significantly more expensive (15-30 min + $2–5 per domain for indexing alone).

---

## What Still Needs Decisions

| Item | Notes |
|---|---|
| **45.9x vs 65x in abstract** | Use real number. Recommend 45.9x pending GraphRAG run. |
| **GraphRAG scope** | Full run needed for paper completeness. ~1 week compute. |
| **Paper length** | Currently 13 pages. Target 16-18 for arXiv. Sections 4, 5, 6 need expansion. |
| **ArXiv submission** | After GraphRAG done + figures reviewed + abstract finalized. |

More soon.

— Daniel
