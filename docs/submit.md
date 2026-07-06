# Submit Your System

Add your retrieval system to the KRB leaderboard.

The harness handles dataset loading, LLM calls, and scoring — you implement
one method.

---

## The interface

```python
from abc import ABC, abstractmethod
from pathlib import Path

class Retriever(ABC):

    @abstractmethod
    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        """
        Return the context string your system would prepend to the query.
        The harness calls Claude with: system_prompt + context + query.

        domain     : e.g. "calculus"
        query_text : benchmark query string
        meta       : full query record — type, concept_id, hop_depth, ground_truth
        """

    def setup(self, domain: str, graph_path: Path):
        """Called once per domain before queries run. Pre-load indexes here."""
        pass

    def generate(self, context, query_text, client, model):
        """Override to use a different LLM. Default: Claude Haiku."""
        ...
```

Import it directly from the evaluation module:

```python
from evaluation.krb_eval import Retriever, run_eval
```

---

## Minimal example — plain RAG

```python
from pathlib import Path
from evaluation.krb_eval import Retriever, run_eval

class SimpleRAGRetriever(Retriever):
    """FAISS + sentence-transformers RAG over the domain CSV."""

    def __init__(self):
        self._retrievers = {}

    def setup(self, domain: str, graph_path: Path):
        import csv
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings

        docs = []
        with open(graph_path) as f:
            for row in csv.DictReader(f):
                deps = row.get("Dependencies", "").replace("|", ", ")
                docs.append(f"[{row['TaxonomyID']}] {row['ConceptLabel']} | prerequisites: {deps}")

        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vs  = FAISS.from_texts(docs, emb)
        self._retrievers[domain] = vs.as_retriever(search_kwargs={"k": 5})

    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        r = self._retrievers.get(domain)
        if not r:
            return ""
        chunks = r.invoke(query_text)
        return "RETRIEVED CONTEXT:\n" + "\n".join(c.page_content for c in chunks)


if __name__ == "__main__":
    results = run_eval(
        retriever=SimpleRAGRetriever(),
        system_name="simple-rag-minilm",
        domains=["calculus", "biology"],   # or None for all domains
        dry_run=False,
    )
    print(f"Macro F1: {results['macro_f1']}")
    # → writes krb_submission_simple-rag-minilm_<timestamp>.json
```

---

## RAGAS example (runnable — see `evaluation/ragas_retriever.py`)

ChromaDB + sentence-transformers retrieval with optional RAGAS v0.2 scoring
(Faithfulness, ResponseRelevancy, LLMContextRecall) after the KRB eval.

```bash
pip install chromadb sentence-transformers langchain-anthropic langchain-huggingface
pip install ragas   # only for --ragas-eval

# Test pipeline — no API calls
python evaluation/ragas_retriever.py --domain calculus --dry-run

# KRB eval — 2 domains (~$0.30 Haiku)
ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --domain calculus biology

# KRB + RAGAS metrics (Faithfulness / Relevancy / Context Recall)
ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --domain calculus --ragas-eval

# Full benchmark — all domains (~$5)
ANTHROPIC_API_KEY=sk-ant-... python evaluation/ragas_retriever.py --all
```

Or call it directly from Python:

```python
from evaluation.ragas_retriever import RAGASRetriever
from evaluation.krb_eval import run_eval

retriever = RAGASRetriever(embed_model="all-MiniLM-L6-v2", top_k=5)
results = run_eval(
    retriever=retriever,
    system_name="chromadb-minilm-top5",
    domains=["calculus", "biology"],
)
print(f"Macro F1: {results['macro_f1']}")
```

---

## LlamaIndex example

```python
from pathlib import Path
import csv
from evaluation.krb_eval import Retriever, run_eval

class LlamaIndexRetriever(Retriever):

    def __init__(self):
        self._indexes = {}

    def setup(self, domain: str, graph_path: Path):
        from llama_index.core import VectorStoreIndex, Document

        docs = []
        with open(graph_path) as f:
            for row in csv.DictReader(f):
                deps = row.get("Dependencies", "").replace("|", ", ")
                text = f"[{row['TaxonomyID']}] {row['ConceptLabel']} | prerequisites: {deps}"
                docs.append(Document(text=text, metadata={"domain": domain}))

        self._indexes[domain] = VectorStoreIndex.from_documents(docs)

    def retrieve(self, domain: str, query_text: str, meta: dict) -> str:
        index = self._indexes.get(domain)
        if not index:
            return ""
        retriever = index.as_retriever(similarity_top_k=5)
        nodes = retriever.retrieve(query_text)
        return "RETRIEVED CONTEXT:\n" + "\n".join(n.text for n in nodes)


if __name__ == "__main__":
    results = run_eval(
        retriever=LlamaIndexRetriever(),
        system_name="llamaindex-v0.10",
        domains=None,   # all 45 domains — ~$5 compute
    )
```

---

## Run it

```bash
# Test your retrieval pipeline without spending API credits
python your_retriever.py --dry-run

# Full eval, two domains
ANTHROPIC_API_KEY=sk-ant-... python your_retriever.py

# Full eval, all domains (~$5 with Haiku)
python evaluation/krb_eval.py --system ckg --all
```

The harness writes two files to `krb_results/`:

| File | Contents |
|------|----------|
| `krb_submission_{name}.json` | Summary scores — submit this |
| `krb_{name}_queries.jsonl` | Per-query results for your analysis |

---

## Submit

Open a GitHub issue with your results:

[**→ Submit results (GitHub issue)**](https://github.com/Yarmoluk/ckg-benchmark/issues/new?template=submission.md&title=Submission%3A+%5Byour-system-name%5D){ .md-button .md-button--primary }

Attach your `krb_submission_{name}.json` file and include:

- System name and version
- Brief description (2–3 sentences)
- Whether you used the graph CSV, raw text, or an external corpus
- Any deviations from the default Claude Haiku evaluator

Results appear on the leaderboard after a spot-check of the submission file.

---

## What gets scored

| Metric | Description |
|--------|-------------|
| **Macro F1** | Token-level F1 averaged across all queries and domains |
| **Mean tokens** | Average context tokens per query |
| **RDS** | F1 / tokens — retrieval density score (the core efficiency metric) |
| **F1 by query type** | T1 entity · T2 dependency · T3 path · T4 aggregate · T5 cross-concept |
| **F1 by hop depth** | 1-hop through 5-hop query performance |

See [Metrics](metrics/index.md) for full definitions.

---

## Baseline numbers (v0.6.2)

| System | Macro F1 | Mean tokens | RDS |
|--------|----------|-------------|-----|
| CKG (reference) | **0.471** | 269 | 0.00175 |
| RAG (FAISS + MiniLM) | 0.123 | 2,982 | 0.0000412 |
| GraphRAG | 0.120 | — | — |

Beat 0.471 F1 or 0.00175 RDS to claim the top spot.
