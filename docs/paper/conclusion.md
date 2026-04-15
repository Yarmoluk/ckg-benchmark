# Conclusion

We presented the CKG Benchmark, the first large-scale comparison of RAG, GraphRAG, and Compressed Knowledge Graphs across 25 educational domains. Our key findings are:

1. **RDS and Hop-Depth F1** are practical additions to IR evaluation that jointly measure quality and efficiency---metrics missing from existing benchmarks like BEIR and RAGAS.
2. **CKG outperforms RAG and GraphRAG** on structured domain retrieval, particularly on multi-hop dependency queries where explicit edges prevent the transitive inference failures inherent in embedding-based approaches.
3. **Pre-structured knowledge beats dynamically extracted graphs** when the domain is stable and expert-curated taxonomies are available.
4. **The McCreary Corpus** is a reproducible, citable multi-domain benchmark with standardized schema across 25 domains.

## Future Work

We identify three directions for future research:

- **Domain generalization**: Extending the benchmark to non-educational domains (legal, medical, financial) to test generalizability.
- **Hybrid architectures**: Combining CKG structure with RAG's ability to retrieve rich contextual information.
- **Automated CKG construction**: Building CKGs from unstructured text, eliminating the expert curation requirement.

## Open Benchmark

The complete benchmark---corpus, queries, evaluation harness, and results---is released at [HuggingFace](https://huggingface.co/datasets/graphify-md/ckg-benchmark) under CC BY 4.0 (data) and MIT (code). We invite the community to add domains, systems, and metrics.
