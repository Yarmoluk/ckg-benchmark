# Getting Started

## Prerequisites

- Python 3.10+
- GitHub CLI (`gh`) for corpus extraction
- An Anthropic API key (for running experiments)

## Installation

```bash
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt
```

## Generate Queries

Generate benchmark queries from any domain's learning graph CSV:

```bash
python evaluation/generate_queries.py \
  --csv benchmark/domains/calculus/learning-graph.csv \
  --domain calculus \
  --output benchmark/queries/queries_calculus.jsonl
```

## Run Experiments

When the evaluation harness is complete:

```bash
python evaluation/harness.py \
  --queries benchmark/queries/queries_calculus.jsonl \
  --systems rag graphrag ckg \
  --output results/
```

## Reproduce Paper Results

```bash
python evaluation/harness.py --reproduce-table-1
```

## Extract Corpus from Source Repos

To re-extract learning graph CSVs from all McCreary textbook repositories:

```bash
bash extract_corpus.sh
```

This requires the GitHub CLI (`gh`) to be installed and authenticated.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | >= 0.25.0 | Claude API |
| `openai` | >= 1.0.0 | Embeddings |
| `faiss-cpu` | >= 1.7.4 | Vector similarity |
| `langchain` | >= 0.1.0 | RAG pipeline |
| `graphrag` | >= 1.0.0 | GraphRAG system |
| `pandas` | >= 2.0.0 | Data processing |
| `numpy` | >= 1.24.0 | Numerical computation |
| `scikit-learn` | >= 1.3.0 | ML utilities |
| `tqdm` | >= 4.65.0 | Progress bars |
