# About

## What Is This?

The CKG Benchmark is a reproducible benchmark and ArXiv paper comparing three LLM knowledge retrieval paradigms:

1. **RAG** (Retrieval-Augmented Generation) --- chunked text with vector embeddings
2. **GraphRAG** --- dynamically extracted entity/relationship graphs
3. **CKG** (Compressed Knowledge Graphs) --- pre-structured DAGs with explicit taxonomy

## Why Does This Matter?

Standard IR benchmarks measure quality only. In production LLM systems, **token cost is a first-class constraint**:

- Enterprise AI budgets are token-denominated
- Latency scales with token count
- Context window limits bound what can be retrieved
- Cost per query determines whether a system is deployable at scale

A retrieval system that achieves F1=0.85 at 300 tokens is strictly better than one achieving F1=0.87 at 4,000 tokens for most real-world deployments.

## The Hypothesis

The efficiency advantage of CKG is not random but proportional to the **structural richness** of the domain's DAG. We call this the **Structure Premium** hypothesis.

## Target Venue

- **ArXiv:** cs.IR (primary), cs.AI (secondary)
- **Dataset:** [HuggingFace](https://huggingface.co/datasets/graphify-md/ckg-benchmark) (planned)

## License

- **Code:** MIT
- **Benchmark data:** CC BY 4.0
- **Source learning graphs:** MIT ([McCreary Intelligent Textbooks](https://github.com/dmccreary))
