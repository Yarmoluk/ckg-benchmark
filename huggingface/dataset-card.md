# Dataset Card: CKG Benchmark

## Dataset Summary

The **CKG Benchmark** is a multi-domain information retrieval benchmark for evaluating
LLM knowledge retrieval architectures. It compares three systems — RAG, GraphRAG, and
Compact Knowledge Graphs (CKG) — across 47 educational domains derived from the
McCreary Intelligent Textbook Corpus.

All ground truth is derived deterministically from DAG structure, not human annotation,
making the benchmark fully reproducible.

## Benchmark Details

- **47 domains**: STEM, professional, humanities, and foundational subjects
- **8,121 queries**: auto-generated from DAG edges (T1–T5 query types, seed=42)
- **3 systems evaluated**: RAG (FAISS + MiniLM), GraphRAG (Microsoft v1.x), CKG
- **Novel metrics**: RDS, CPCA, CUR, Hop-Depth F1
- **Standard metrics**: Token F1, BERTScore (roberta-large), Exact Match

## Key Results (April 2026)

| System | Token F1 | BERT F1 | Mean Tokens | RDS | BERT CPCA |
|---|---|---|---|---|---|
| **CKG** | **0.4926** | **0.8569** | **274** | **0.001887** | **$0.000506** |
| RAG | 0.1223 | 0.8168 | ~3,100 | ~0.000029 | $0.013046 |
| GraphRAG | 0.1200 | 0.8246 | ~10,000+ | ~0.000012 | $0.020098 |

**CKG advantages (BERTScore basis — industry-standard semantic scoring):**
- **vs GraphRAG**: higher BERT F1 (0.857 vs 0.825) AND 40x lower BERT CPCA — CKG beats Microsoft's state-of-the-art on both quality and cost
- **vs RAG**: higher BERT F1 (0.857 vs ~0.815) AND ~40x lower BERT CPCA
- 11x fewer tokens per query than RAG baseline
- 65x RDS advantage over RAG (token F1 basis)
- Advantage holds under both exact (token F1) and semantic (BERTScore) evaluation

**T1–T5 CKG BERTScore breakdown:**

| Query Type | Token F1 | BERT F1 | BERT CPCA |
|---|---|---|---|
| T1 entity lookup | 0.2218 | 0.8313 | $0.000576 |
| T2 dependency | 0.6682 | 0.8751 | $0.000302 |
| T3 multi-hop path | 0.6900 | 0.8543 | $0.000504 |
| T4 category aggregate | 0.9803 | 0.9165 | $0.000936 |
| T5 cross-concept | 0.3249 | 0.8487 | $0.000541 |

## Associated Paper

> Yarmoluk, D. & McCreary, D. (2026). "Compact Knowledge Graphs vs. RAG and GraphRAG:
> A Reproducible Benchmark Across 47 Educational Domains." arXiv:XXXX.XXXXX [cs.IR]

## Source Corpus

All learning graphs from the McCreary Intelligent Textbook Corpus:
- https://github.com/dmccreary/ (MIT License)
- 47 repositories, each containing a `learning-graph.csv` in the four-column CKG schema

## Query Schema

```json
{
  "id": "calculus_T2_47",
  "domain": "calculus",
  "query_type": "T2_dependency",
  "query": "What are the prerequisites for Implicit Differentiation?",
  "ground_truth": ["Derivative", "Chain Rule", "Function Notation"],
  "concept_id": 47,
  "hop_depth": 1
}
```

## Result Record Schema

Each result JSONL record contains:
```json
{
  "query_id": "calculus_T2_47",
  "system": "ckg",
  "predicted_answer": "...",
  "prompt_tokens": 284,
  "completion_tokens": 42,
  "total_tokens": 326,
  "f1": 0.6667,
  "precision": 0.75,
  "recall": 0.60,
  "rds": 0.002045,
  "cost_usd": 0.000148,
  "bert_p": 0.8821,
  "bert_r": 0.8654,
  "bert_f1": 0.8737,
  "bert_cpca": 0.000169,
  "latency_ms": 1243
}
```

## Dataset Files

```
benchmark/domains/{domain}/learning-graph.csv   — source CKGs (47 domains)
benchmark/queries/queries_{domain}.jsonl         — benchmark queries per domain
results/ckg/ckg_{domain}.jsonl                   — CKG predictions + scores
results/rag/rag_{domain}.jsonl                   — RAG predictions + scores
results/graphrag/graphrag_{domain}.jsonl         — GraphRAG predictions + scores
results/tables/                                  — paper tables (CSV)
results/figures/data/                            — figure data (JSON)
```

## Novel Metrics

**Reasoning Density Score (RDS)** = F1 / tokens_consumed
- Measures correct information produced per token spent
- CKG: ~0.001887 vs RAG: ~0.000029 (65x advantage)

**Cost Per Correct Answer (CPCA)** = cost_usd / F1
- Translates retrieval quality into dollar cost per correct answer
- BERT CPCA uses BERTScore F1 as the quality denominator (semantic basis)

**Context Utilization Rate (CUR)** = relevant_retrieved_tokens / total_retrieved_tokens
- Measures retrieval precision at the token level

## Reproduce Paper Results

```bash
git clone https://github.com/graphify-md/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt

# Score existing results (no API key needed)
python evaluation/analyze_results.py --systems ckg rag graphrag

# Add BERTScore to results (no API key needed, downloads roberta-large ~500MB)
python evaluation/add_bertscore.py --system ckg rag graphrag

# Re-run CKG from scratch (requires ANTHROPIC_API_KEY)
python evaluation/ckg_harness.py --all --parallel
```

## Evaluation Model

All LLM calls use Claude Haiku 4.5 at temperature=0.
Pricing: $0.80/M input tokens, $4.00/M output tokens.
BERTScore: roberta-large via `bert-score` library.

## Limitations

- Corpus is educational — domain transfer to legal/financial/clinical not evaluated in this release
- Ground truth derived from DAG edges may not capture all semantically valid answers (BERTScore partially addresses this)
- GraphRAG results cover 21 domains vs 47 for CKG/RAG due to compute cost

## Citation

```bibtex
@misc{yarmoluk2026ckg,
  title={Compact Knowledge Graphs vs. RAG and GraphRAG: A Reproducible Benchmark
         Across 47 Educational Domains},
  author={Yarmoluk, Daniel and McCreary, Dan},
  year={2026},
  eprint={XXXX.XXXXX},
  archivePrefix={arXiv},
  primaryClass={cs.IR}
}
```

## License

- Benchmark code: MIT
- Benchmark queries and result data: CC BY 4.0
- Source learning graphs: MIT (McCreary Intelligent Textbook Corpus)
- BERTScore model weights: Apache 2.0 (roberta-large via HuggingFace)

## Authors

- **Daniel Yarmoluk** — Graphify.md (daniel.yarmoluk@gmail.com)
- **Dan McCreary** — netrii / McCreary Intelligent Textbook Corpus
