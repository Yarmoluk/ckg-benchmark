# CKG Benchmark

**Benchmarking RAG, GraphRAG, and Compressed Knowledge Graphs across 25 educational domains.**

!!! note "Status: Pre-experiment"
    Paper outline, metrics specification, and evaluation harness are complete.
    Corpus extraction and query generation are done. Experimental runs are pending.

## Overview

This benchmark evaluates three LLM knowledge retrieval architectures on structured educational domains from the McCreary Intelligent Textbook Corpus.

| System | Knowledge Representation | Tokens/Query | Build Cost |
|--------|--------------------------|--------------|------------|
| **RAG** | Chunked text + vector embeddings | 3,000--5,000 | Embed all chunks |
| **GraphRAG** | Dynamically extracted entity/relationship graph | 2,000--8,000 | Full entity extraction |
| **CKG** | Pre-structured DAG with explicit taxonomy | 150--400 | Zero (CSV-native) |

## The Core Claim

Pre-structured knowledge graphs (CKG) outperform dynamically extracted graphs (GraphRAG) and vector retrieval (RAG) on domain-specific retrieval tasks---particularly multi-hop dependency and path queries---at a fraction of the token cost.

Measured by **Reasoning Density Score (RDS)**:

$$\text{RDS} = \frac{\text{F1}}{\text{tokens\_consumed}}$$

## By the Numbers

- **22 domains** extracted (STEM, Professional, Foundational)
- **6,351 concepts** with standardized CSV schema
- **3,854 benchmark queries** across 5 query types
- **16 evaluation metrics** (10 novel)
- **3 retrieval architectures** compared

## Authors

- **Daniel Yarmoluk** --- [Graphify.md](https://graphify.md) --- CKG architecture, benchmark design, RDS metric
- **Dan McCreary** --- [Intelligent Textbooks](https://github.com/dmccreary) --- Source corpus

## Quick Links

- [Read the paper](paper/abstract.md)
- [Explore the benchmark](benchmark/index.md)
- [Metrics specification](metrics/index.md)
- [Get started](getting-started.md)
- [GitHub repository](https://github.com/Yarmoluk/ckg-benchmark)
