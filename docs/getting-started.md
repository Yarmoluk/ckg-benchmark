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

## Run the CKG Baseline

Evaluate the built-in CKG system against any domain:

```bash
# Single domain (~$0.12 with Haiku)
ANTHROPIC_API_KEY=sk-ant-... python evaluation/krb_eval.py --system ckg --domain calculus

# All domains (~$5)
ANTHROPIC_API_KEY=sk-ant-... python evaluation/krb_eval.py --system ckg --all

# Test retrieval pipeline without API calls
python evaluation/krb_eval.py --system ckg --domain calculus --dry-run
```

## Plug In Your Own System

Subclass `Retriever` and implement one method:

```python
from evaluation.krb_eval import Retriever, run_eval

class MyRetriever(Retriever):
    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        # Return the context string to prepend to the query.
        return my_retrieval_function(domain, query_text)

results = run_eval(
    retriever=MyRetriever(),
    system_name="my-system-v1",
    domains=["calculus", "biology"],   # or None for all 45
)
# → writes krb_results/krb_submission_my-system-v1.json
```

See [Submit Your System](submit.md) for full RAG and LlamaIndex examples.

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
