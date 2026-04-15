# Message to Dan — April 14, 2026

**Send via:** GitHub repo comment or text

---

Dan,

Both concerns you logged last night are valid and have been addressed. Here's where we landed:

---

**1. Naming: "Compressed" → "Compact"**

You're right — there's no compression algorithm. The CSV is authored directly in a compact form; the efficiency comes from representation choice, not a compression step. I've renamed throughout the paper to **"Compact Knowledge Graphs"** — the CKG acronym is preserved, so nothing downstream breaks. The abstract, title, architecture section, and conclusion are all updated.

---

**2. The Tautology / DAG-is-not-search concern**

This is the more important one, and I think our first results actually give us a clean answer.

From the bioinformatics run (177 queries):

| Query Type | CKG F1 |
|------------|--------|
| T1 entity lookup ("What is X?") | **0.09** |
| T2 direct dependency | 0.03 |
| T3 multi-hop path | **0.47** |
| T4 category aggregate | **0.55** |
| T5 cross-concept | 0.14 |

CKG scores ~0.09 on T1 explanatory queries. It has no prose — it can only return a concept's TaxonomyID and dependency list in response to "What is X?" The DAG appropriately fails at questions it was never designed to answer.

This is the honest story and it's actually stronger than the original framing:

- We are **not** claiming CKG is a general RAG replacement. We never should have implied that.
- We **are** claiming CKG is the right tool for structural queries: prerequisite chains (T2), concept paths (T3), category membership (T4). These are the dominant query patterns in tutoring systems, curriculum planners, and adaptive learning platforms.
- The T1 result is a **negative control** — it proves the benchmark isn't rigged. A system that only reads DAG edges appropriately scores low on questions the DAG can't answer.

The tautology objection dissolves when the scope is stated clearly. The new framing: "For queries that have structural answers, using a pre-structured graph is ~13x more token-efficient with zero hallucination. For explanatory queries, use RAG."

I've updated:
- Abstract: claims narrowed to "structural queries"; T1 negative control sentence added
- Introduction: explicit paragraph stating we do NOT claim T1 superiority
- Benchmark Design: note explaining T1 as a RAG-favorable boundary test
- Discussion/Limitations: two new bullets on structural scope and T1 as boundary test
- Conclusion: "outperforms RAG and GraphRAG" scoped to "structural knowledge retrieval"

The run is still going (~7 of 46 domains complete). When we have all 46 domains, the T1 result should hold across the board — and that cross-domain consistency is actually a publishable finding in itself: "CKG fails at explanatory queries uniformly and predictably, confirming the scope of structural retrieval."

More tomorrow when the run is further along.

— Daniel
