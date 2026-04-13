# Dataset Card: CKG Benchmark

## Dataset Summary

The **CKG Benchmark** is a multi-domain information retrieval benchmark
for evaluating LLM knowledge retrieval architectures. It is derived from
the McCreary Intelligent Textbook Corpus — 25 open-source educational
domains with standardized learning graph structure.

## Benchmark Details

- **25 domains**: STEM, professional, and foundational subjects
- **~4,375 queries**: auto-generated from DAG structure (T1–T5 query types)
- **Ground truth**: derived directly from learning-graph.csv DAG edges
- **3 systems evaluated**: RAG, GraphRAG, CKG
- **Novel metrics**: RDS, CUR, Hop-Depth F1, CPCA, Relationship Precision

## Associated Paper

> Yarmoluk, D. & McCreary, D. (2026). "Benchmarking Knowledge Retrieval
> Architectures Across 25 Domains: RAG, GraphRAG, and Compressed Knowledge
> Graphs on the McCreary Intelligent Textbook Corpus." arXiv:XXXX.XXXXX

## Source Corpus

All learning graphs from: https://github.com/dmccreary/
License: MIT — see individual repos for attribution.

## Query Schema

```json
{
  "id": "calculus_T2_47",
  "domain": "calculus",
  "type": "T2_dependency",
  "query": "What are the prerequisites for Implicit Differentiation?",
  "ground_truth": ["Derivative", "Chain Rule", "Function Notation"],
  "concept_id": 47,
  "hop_depth": 1
}
```

## Splits

- `queries_all.jsonl` — full benchmark, all 25 domains
- `queries_{domain}.jsonl` — per-domain splits
- `results/rag_predictions.jsonl` — RAG system outputs
- `results/graphrag_predictions.jsonl` — GraphRAG system outputs
- `results/ckg_predictions.jsonl` — CKG system outputs
- `results/scores.json` — final paper metrics

## Reproduce Paper Results

```bash
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt
python evaluation/harness.py --reproduce-table-1
# Should match Table 1 within ±0.01 F1
```

## Limitations

- Corpus is educational — domain transfer to legal/financial not tested
- CKG requires expert-curated taxonomy (not zero-cost for new domains)
- Ground truth from DAG may not capture all valid natural language answers

## License

- Code: MIT
- Benchmark data: CC BY 4.0
- Source learning graphs: MIT (McCreary)
