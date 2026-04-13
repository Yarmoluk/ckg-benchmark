# CKG Benchmark — Compressed Knowledge Graphs vs RAG vs GraphRAG

**A reproducible benchmark comparing three retrieval architectures across 25 domains.**

> **Status:** Pre-experiment. Paper outline, metrics, and harness design complete. Seeking collaborators for corpus extraction and experimental runs.

## Authors

- Daniel Yarmoluk — [Graphify.md](https://graphify.md) — CKG architecture, benchmark design, RDS metric
- Dan McCreary — [dmccreary/intelligent-textbooks](https://github.com/dmccreary/intelligent-textbooks) — Corpus (McCreary Intelligent Textbook Corpus)

---

## What This Is

A benchmark and ArXiv paper comparing three LLM knowledge retrieval paradigms:

| Column | System | How knowledge is stored |
|--------|--------|------------------------|
| 1 | **RAG** | Chunked text + vector embeddings |
| 2 | **GraphRAG** | Dynamically extracted entity/relationship graph |
| 3 | **CKG** | Pre-structured DAG with explicit taxonomy (this paper's contribution) |

Evaluated on the **McCreary Intelligent Textbook Corpus** — 25 open-source educational domains with identical schema, totaling ~6,000 concepts and ~8,500 dependency edges.

---

## Repository Structure

```
ckg-benchmark/
├── README.md                  # This file
├── paper/
│   ├── outline.md             # Full paper outline
│   ├── abstract.md            # Draft abstract
│   └── related-work.md        # Literature citations
├── metrics/
│   ├── metrics-spec.md        # All metrics defined (F1, RDS, hop-depth, etc.)
│   └── tokenomics.md          # Full tokenomics framework
├── benchmark/
│   ├── query-taxonomy.md      # T1–T5 query types defined
│   ├── corpus-index.md        # All 25 McCreary repos + stats
│   └── ground-truth-spec.md   # How ground truth is constructed from CSV
├── evaluation/
│   ├── generate_queries.py    # Auto-generate queries from learning-graph.csv
│   ├── harness.py             # Run all 3 systems
│   ├── metrics.py             # F1 + RDS + all new metrics
│   └── requirements.txt
├── architecture/
│   ├── rag-spec.md            # RAG baseline configuration
│   ├── graphrag-spec.md       # GraphRAG configuration
│   └── ckg-spec.md            # CKG architecture specification
└── huggingface/
    └── dataset-card.md        # HuggingFace dataset card template
```

---

## Quick Start (when experiment harness is ready)

```bash
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt

# Generate ground truth queries from any McCreary repo CSV
python evaluation/generate_queries.py \
  --csv path/to/learning-graph.csv \
  --domain calculus \
  --output benchmark/queries_calculus.jsonl

# Run all 3 systems and score
python evaluation/harness.py \
  --queries benchmark/queries_calculus.jsonl \
  --systems rag graphrag ckg \
  --output results/

# Reproduce paper Table 1
python evaluation/harness.py --reproduce-table-1
```

---

## The Core Claim

Pre-structured knowledge graphs (CKG) outperform dynamically extracted graphs (GraphRAG) and vector retrieval (RAG) on domain-specific retrieval tasks — particularly multi-hop dependency and path queries — at a fraction of the token cost.

Measured by **Reasoning Density Score (RDS)**:
```
RDS = F1 / tokens_consumed
```

---

## Target Venue

- ArXiv: cs.IR (primary), cs.AI (secondary)
- HuggingFace: `graphify-md/ckg-benchmark` (dataset + results)
- License: MIT (code), CC BY 4.0 (benchmark data)
