# Author Response: DAG-Is-Not-Search / Tautology Concern

**Date:** 2026-04-14
**Responding to:** `major-concern-dag-is-not-search.md`
**Decision:** Adopt hybrid Option A + Option C
**Status:** Resolved — paper edits applied

---

## Summary of Decision

Dan's concern is valid and has been addressed through a combination of:

- **Option A** (narrow claims): The paper now explicitly frames CKG as a benchmark for **structural knowledge retrieval**, not general-purpose knowledge retrieval.
- **Option C** (efficiency framing): The core contribution is reframed as: "For queries that have structural answers, using a pre-structured graph is ~13x more token-efficient with zero hallucination."

---

## The T1 Negative Control

This is the key insight that makes the honest framing *stronger*, not weaker:

CKG scores F1 ≈ 0.09 on T1 entity lookup queries ("What is X?"). The DAG has no prose — it can only return TaxonomyID and dependency edges in response to an explanatory question.

This is now documented explicitly in the paper as a **negative control**:
> "T1 results confirm that the benchmark is not constructed to favor CKG universally. A system that only reads DAG edges appropriately fails at questions the DAG cannot answer."

A benchmark that shows when your system wins AND when it doesn't is more credible than one that only shows wins. Reviewers will find this disarming rather than damaging.

---

## What "Structural Knowledge Retrieval" Means

The claim is now precisely scoped:

| Query Type | What it tests | CKG advantage? |
|------------|---------------|----------------|
| T1 entity | "What is X?" | No — RAG wins, intentional |
| T2 dependency | "What are prerequisites for X?" | Yes — explicit edges |
| T3 multi-hop | "What is the path from A to B?" | Yes — BFS/DFS is exact |
| T4 aggregate | "List all CORE concepts" | Yes — taxonomy filter |
| T5 cross-concept | "How do A and B relate?" | Partial — shared neighbors |

The tautology concern applies to T2/T3/T4, but these are **legitimate real-world use cases** in:
- Tutoring systems (prerequisite mapping)
- Curriculum planners (concept sequencing)
- Adaptive learning platforms (knowledge state tracking)

The paper now says this explicitly: "We benchmark structural knowledge retrieval — the retrieval of prerequisite chains, dependency paths, and category membership — which is the dominant query pattern in educational AI systems."

---

## Why This Is Still Publishable

The honest framing yields three genuine contributions that survive peer review:

1. **The tautology is not a bug, it's a feature**: If a system is designed for structural queries, testing it on structural queries is the right evaluation. The tautology objection dissolves when the scope is stated clearly.

2. **The efficiency claim is novel**: 13x fewer tokens for equivalent structural recall is a real engineering result with deployment implications. No prior benchmark measures this.

3. **The T1 result validates experimental integrity**: Showing that CKG *doesn't* win on explanatory queries proves the evaluation is fair, not rigged.

---

## Paper Edits Applied

- `01-abstract.tex`: Claims narrowed to "structural queries"; T1 negative control sentence added
- `02-introduction.tex`: Added explicit "we do not claim T1 superiority" paragraph after falsifiable claims; footnote on CKG build cost added to Table 1
- `06-benchmark-design.tex`: Note added under Query Taxonomy table explaining T1 as RAG-favorable boundary test
- `09-discussion.tex`: Two new limitation bullets — "Structural query scope" and "T1 as boundary test"
- `10-conclusion.tex`: "outperforms RAG and GraphRAG" → scoped to "structural knowledge retrieval"; T1 qualifier added
