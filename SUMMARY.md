# CKG Benchmark — One-Page Summary

> Pre-structured knowledge graphs outperform RAG 4× at 11× lower token cost.
> Full paper · 45 domains · 7,928 queries · open source.

---

## The Finding

Three retrieval architectures. Same queries. Same LLM. Different structure going in.

| System | F1 Score | Tokens/query | Cost/query |
|---|---|---|---|
| RAG (FAISS + Claude) | 0.123 | 2,982 | ~$0.009 |
| GraphRAG (Microsoft) | 0.120 | 3,450 | ~$0.013 |
| **CKG (pre-structured DAG)** | **0.471** | **269** | **~$0.001** |

**CKG is 42× more efficient per correct answer than RAG.**

---

## Why the Gap Is So Large

RAG retrieves the most *similar* text chunks. For simple lookups, this works.
For multi-hop questions — prerequisites, dependency chains, regulatory trees — it fragments the answer across chunks that contradict each other.

CKG pre-structures domain knowledge as a directed acyclic graph (DAG). Queries traverse pre-built dependency paths. No similarity search. No hallucination by construction.

**F1 by hop depth:**

| Hop depth | CKG F1 | RAG F1 |
|---|---|---|
| 1 | 0.374 | 0.312 |
| 2 | 0.512 | 0.298 |
| 3 | 0.631 | 0.241 |
| 4 | 0.714 | 0.198 |
| 5 | **0.772** | 0.187 |

CKG improves continuously. RAG plateaus at hop=2 and degrades. The deeper the question, the larger the gap.

---

## Where CKG Dominates

| Query type | CKG F1 | RAG F1 | Advantage |
|---|---|---|---|
| Aggregate (T4) | 0.964 | 0.286 | 3.4× |
| Path traversal (T3) | 0.660 | 0.201 | 3.3× |
| Dependency (T2) | 0.634 | 0.078 | 8.1× |
| Cross-concept (T5) | 0.323 | 0.115 | 2.8× |
| Entity lookup (T1) | 0.207 | 0.094 | 2.2× |

Biggest win: dependency queries (8.1×). These are the queries that matter most in clinical, legal, financial, and regulatory domains.

---

## Structure Is the Signal — Not Curation Effort

Track 2: GLP-1/pharma domain built from ClinicalTrials.gov API in a single session. No expert curation.

**F1 = 0.530** — higher than the 45-domain average.

If a domain has knowable dependencies, it can be CKG-ified. The structure, not the effort, drives accuracy.

---

## The Architecture

```
CSV (ConceptID, ConceptLabel, Dependencies, TaxonomyID)
         ↓
    DAG in memory
         ↓
  BFS/DFS traversal
         ↓
  Structured context → LLM → Answer
```

No vector index. No embedding model. No retrieval pipeline. Just a graph traversal on a structured file.

A domain CSV with 500 concepts and 1,200 edges fits in ~50KB. The same knowledge in RAG requires a full embedding pipeline and returns 3,000+ tokens per query.

---

## Use It

**Live demo:** huggingface.co/spaces/danyarm/ckg-demo

**MCP server** (works in Claude Code, any MCP-compatible agent):
```
pip install ckg-mcp
```

**Full dataset** (45 domain CSVs + 7,928 query JSONL + results):
huggingface.co/datasets/danyarm/ckg-benchmark

**Paper + LaTeX source:**
github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf

**Custom domain** (clinical, legal, financial, regulatory):
graphifymd.com

---

## Cite

```bibtex
@misc{yarmoluk2026ckg,
  title   = {Compact Knowledge Graphs Outperform RAG on Structural Queries},
  author  = {Yarmoluk, Daniel},
  year    = {2026},
  url     = {https://github.com/Yarmoluk/ckg-benchmark}
}
```

---

*MIT license (code) · CC BY 4.0 (data) · graphifymd.com*
