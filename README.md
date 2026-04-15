# CKG Benchmark

**A reproducible benchmark comparing RAG, GraphRAG, and Compressed Knowledge Graphs across 22 educational domains.**

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Pre-experiment](https://img.shields.io/badge/Status-Pre--experiment-yellow.svg)]()
[![Domains: 22](https://img.shields.io/badge/Domains-22-green.svg)]()
[![Queries: 3,854](https://img.shields.io/badge/Queries-3%2C854-green.svg)]()

## Overview

This benchmark evaluates three LLM knowledge retrieval architectures on structured educational domains:

| System | Knowledge Representation | Tokens/Query | Build Cost |
|--------|--------------------------|--------------|------------|
| **RAG** | Chunked text + vector embeddings | 3,000-5,000 | Embed all chunks |
| **GraphRAG** | Dynamically extracted entity/relationship graph | 2,000-8,000 | Full entity extraction |
| **CKG** | Pre-structured DAG with explicit taxonomy | 150-400 | Zero (CSV-native) |

**Core claim:** Pre-structured knowledge graphs (CKG) outperform dynamically extracted graphs (GraphRAG) and vector retrieval (RAG) on domain-specific retrieval tasks -- particularly multi-hop dependency and path queries -- at a fraction of the token cost.

## Authors

- **Daniel Yarmoluk** -- [Graphify.md](https://graphify.md) -- CKG architecture, benchmark design, RDS metric
- **Dan McCreary** -- [Intelligent Textbooks](https://github.com/dmccreary) -- Source corpus (McCreary Intelligent Textbook Corpus)

## The Corpus

The benchmark is built on the **McCreary Intelligent Textbook Corpus** -- 22 open-source educational domains with identical schema:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Function,,FOUND
2,Domain and Range,1,FOUND
4,Composite Function,1|3,FOUND
```

**By the numbers:**

- **22 domains** extracted (24 identified, 22 with valid CSVs)
- **6,351 concepts** total
- **3,854 benchmark queries** across 5 query types
- **3 categories:** STEM, Professional, Foundational

### Domain List

| Category | Domains |
|----------|---------|
| **STEM** | Calculus (325 concepts), Biology, Genetics, Bioinformatics, Statistics, Quantum Computing, Circuits, Geometry, Ecology, Moss |
| **Professional** | Economics, Organizational Analytics, Healthcare Data, Conversational AI, Automating Instructional Design, Blockchain, Claude Skills |
| **Foundational** | Systems Thinking, Theory of Knowledge, Digital Citizenship, Prompt Engineering, Tracking AI, US Geography, ASL |

## Query Types

Queries are auto-generated from each domain's DAG structure:

| Type | Description | Example | Per Domain |
|------|-------------|---------|------------|
| **T1** | Entity lookup | "What is Composite Function?" | ~50 |
| **T2** | Direct dependency | "What are the prerequisites for Implicit Differentiation?" | ~50 |
| **T3** | Multi-hop path | "What is the prerequisite chain from Function to Taylor Series?" | ~25 |
| **T4** | Category aggregate | "List all FOUND concepts" | ~15 |
| **T5** | Cross-concept relationship | "How does Domain and Range relate to Inverse Function?" | ~38 |

## Novel Metrics

Beyond standard IR metrics (F1, Exact Match), this benchmark introduces:

| Metric | Formula | What It Measures |
|--------|---------|------------------|
| **RDS** (Reasoning Density Score) | F1 / tokens_consumed | Quality per token spent |
| **Hop-Depth F1 Degradation** | F1 at hop depth k=1,2,3,4,5+ | Multi-hop reasoning capability |
| **CUR** (Context Utilization Rate) | relevant_tokens / total_retrieved_tokens | Retrieval precision |
| **CPCA** (Cost Per Correct Answer) | cost_per_query / F1 | Real-world cost efficiency |
| **Relationship Precision** | predicted_edges & truth_edges / predicted_edges | Structural fidelity |
| **Hallucination Rate** | queries with hallucinated concepts / total | CKG = 0 by construction |

See [`metrics/metrics-spec.md`](metrics/metrics-spec.md) for full definitions of all 16 metrics.

## Repository Structure

```
ckg-benchmark/
├── README.md
├── extract_corpus.sh              # Clone McCreary repos and extract CSVs
│
├── benchmark/
│   ├── corpus-index.md            # All domains with metadata
│   ├── domains/                   # 22 domain directories
│   │   ├── calculus/
│   │   │   └── learning-graph.csv # 325 concepts
│   │   ├── biology/
│   │   └── ...
│   └── queries/                   # 22 JSONL query files (3,854 total)
│       ├── queries_calculus.jsonl
│       └── ...
│
├── evaluation/
│   ├── generate_queries.py        # Auto-generate queries from CSV DAGs
│   ├── metrics.py                 # F1, RDS, CUR, CPCA, HR implementations
│   ├── harness.py                 # Main runner (placeholder)
│   └── requirements.txt
│
├── metrics/
│   ├── metrics-spec.md            # All 16 metrics defined
│   └── tokenomics.md              # Token accounting framework
│
├── paper/
│   └── outline.md                 # Full paper outline and abstract
│
└── huggingface/
    └── dataset-card.md            # HuggingFace dataset card template
```

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt

# Generate queries from a domain CSV
python evaluation/generate_queries.py \
  --csv benchmark/domains/calculus/learning-graph.csv \
  --domain calculus \
  --output benchmark/queries/queries_calculus.jsonl

# Run all 3 systems and score (when harness is complete)
python evaluation/harness.py \
  --queries benchmark/queries/queries_calculus.jsonl \
  --systems rag graphrag ckg \
  --output results/

# Reproduce paper Table 1
python evaluation/harness.py --reproduce-table-1
```

### Extract Corpus from Source Repos

```bash
# Requires GitHub CLI (gh)
bash extract_corpus.sh
```

## Falsifiable Claims

1. CKG achieves higher F1 on T2 (dependency) and T3 (multi-hop path) queries
2. CKG F1 does not degrade with hop depth; RAG F1 degrades significantly
3. CKG RDS ratio >= 10x vs RAG across all domains
4. GraphRAG hallucinates edges not present in ground truth DAG (HR > 0)
5. CKG Hallucination Rate = 0 (by construction)
6. **Structure Premium hypothesis:** RDS advantage correlates with DAG richness (r > 0.7)

## Dependencies

- Python 3.10+
- `anthropic` >= 0.25.0 (Claude API)
- `openai` >= 1.0.0
- `faiss-cpu` >= 1.7.4
- `langchain` >= 0.1.0
- `graphrag` >= 1.0.0
- `pandas`, `numpy`, `scikit-learn`, `tqdm`

## Current Status

| Component | Status |
|-----------|--------|
| Paper outline | Done |
| Metrics specification (16 metrics) | Done |
| Tokenomics framework | Done |
| Corpus extraction (22 domains) | Done |
| Query generation (3,854 queries) | Done |
| Evaluation harness skeleton | Done |
| Experimental runs | Not started |
| Results and analysis | Not started |
| ArXiv submission | Not started |

## Target Venue

- **ArXiv:** cs.IR (primary), cs.AI (secondary)
- **HuggingFace:** `graphify-md/ckg-benchmark`

## Reproducibility

- Fixed random seed: 42
- All systems use Claude Sonnet 4.6 at temperature=0
- Token counts via Anthropic `count_tokens()` API
- 3 runs per query, variance reported
- CSV-based ground truth (deterministic DAGs)

## License

- **Code:** MIT
- **Benchmark data:** CC BY 4.0
- **Source learning graphs:** MIT ([McCreary Intelligent Textbooks](https://github.com/dmccreary))

## Citation

```bibtex
@misc{yarmoluk2026ckg,
  title={Benchmarking Knowledge Retrieval Architectures Across 25 Domains:
         RAG, GraphRAG, and Compressed Knowledge Graphs on the
         McCreary Intelligent Textbook Corpus},
  author={Yarmoluk, Daniel and McCreary, Dan},
  year={2026},
  note={Pre-print in preparation}
}
```
