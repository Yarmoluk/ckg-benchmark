# Track 3 Highlights — For Dan McCreary
**Date:** 2026-05-09

Dan —

Here's what we built and what I need your eyes on.

---

## What We Did

Pulled the entire GLP-1 agonist trial registry from ClinicalTrials.gov. Every semaglutide, tirzepatide, liraglutide, dulaglutide, and exenatide trial in the NIH database — 1,894 trials, full protocol text. Measured the corpus at **2,682,496 tokens** (11.3 MB).

The GLP-1 CKG we already benchmarked encodes the domain knowledge of that corpus in **2,614 tokens** (7.2 KB).

That is a **1,026× token compression**.

---

## The Three Numbers That Matter

| | Value |
|---|---|
| Source corpus | 2,682,496 tokens |
| CKG | 2,614 tokens |
| Compression | **1,026×** |
| CKG Macro F1 (170 queries) | **0.5298** |
| Long-context cost per query | **$8.05** (projected) |
| CKG cost per query | **$0.00108** (measured) |
| Cost ratio | **7,454×** |

---

## The Structural Finding

No current model can hold the full corpus in a single context window:

- Claude Sonnet 4.6 (200K): **7.5% of corpus** per query
- Gemini 1.5 Pro (1M): **37.3% of corpus** per query
- CKG: **100% of domain** per query, at 2,614 tokens

Long-context is not a slower, more expensive CKG. It is architecturally excluded from the full domain at this corpus size. The CKG is the only approach that accesses the complete knowledge structure per query.

---

## What's Verifiable Right Now (No API Spend)

Five of seven claims require zero LLM calls:

1. Corpus is 2.68M tokens — run `corpus_builder_ct.py`, count with tiktoken
2. CKG is 2,614 tokens — count the CSV
3. Compression is 1,026× — arithmetic
4. No model fits the full corpus — published context limits vs. measured token count
5. Long-context costs $8.05/query — published API pricing × token count

The remaining two (CKG F1 = 0.5298, RAG F1 = 0.1538) are already in the benchmark results and cost less than $1 to rerun.

---

## What's Not Done Yet

The long-context baseline (Condition C) — sending the full corpus to a model per query — has not been run. Estimated cost: $1,369 for 170 queries. I don't have the budget right now.

This is the open question I'd like your read on: **is the cost projection + structural exclusion finding sufficient for publication, or do we need the live accuracy comparison?**

My instinct is that the structural finding stands on its own. A query approach that discards 93% of the source corpus and costs $8/query is not a viable clinical AI strategy regardless of what accuracy number we measure. But you may see it differently.

---

## Four Questions for You

1. **Condition C model:** Gemini 1.5 Pro (1M context, 37% coverage) or Claude Sonnet 4.6 (200K, 7.5%)? Cross-model comparison is messy, but Gemini makes the case harder to win, which makes it more credible if we do win.

2. **Corpus provenance:** The CKG was built from ClinicalTrials.gov + domain literature. The corpus here is ClinicalTrials.gov only. Does that gap matter for the compression claim?

3. **PubMed extension:** Should we add PubMed abstracts for the same drugs to bring the corpus closer to the CKG's full knowledge source? That would push the corpus to 5M+ tokens and make the compression ratio even more dramatic.

4. **Venue:** Does this belong in the arXiv paper as Track 3, or does it stand alone as a benchmark note?

---

## Files

```
docs/paper/track3-short-paper.md       ← 2-page technical brief
docs/paper/track3-methodology.md       ← full methodology for replication
evaluation/corpus_builder_ct.py        ← reproducible corpus pull script
results/track3/ct_glp1_corpus.txt      ← 11.3 MB corpus (git-ignored, rebuild locally)
results/track3/ct_glp1_summary.json    ← all measured stats
```

Run to reproduce the corpus:
```bash
python evaluation/corpus_builder_ct.py --max-trials 2000
```

Let me know what you think. Happy to get on a call if easier.

— Daniel
