# Introduction

## Motivation

LLM retrieval quality is typically measured by F1 alone, yet token cost is a first-class production constraint---not a research afterthought. Domain-specific knowledge has latent structure that RAG discards through chunking, and GraphRAG re-derives structure from text at significant computational expense. But what if the structure is already known?

## The Three Paradigms

| System | Knowledge Representation | Retrieval Method | Build Cost |
|--------|--------------------------|------------------|------------|
| **RAG** | Unstructured text chunks | Embedding similarity | Embed all chunks |
| **GraphRAG** | Dynamically extracted graph | Graph + community search | Full entity extraction |
| **CKG** | Pre-structured DAG + taxonomy | Direct concept/edge lookup | Zero (CSV-native) |

## Falsifiable Claims

We make the following falsifiable claims, each testable against the benchmark results:

1. CKG achieves higher F1 on T2 (dependency) and T3 (multi-hop path) queries.
2. CKG F1 does not degrade with hop depth; RAG F1 degrades significantly.
3. CKG RDS ratio $\geq$ 10x vs RAG across all 25 domains.
4. GraphRAG hallucinates edges not present in ground truth DAG (HR > 0).
5. CKG Hallucination Rate = 0 (by construction).
6. The **Structure Premium** hypothesis: RDS advantage correlates with DAG richness ($r > 0.7$).

## Contributions

1. The CKG architecture specification (format, DAG constraints, taxonomy schema).
2. Five novel evaluation metrics (RDS, CUR, Hop-F1, CPCA, RP).
3. The McCreary Corpus as a formal benchmark dataset (first paper to do so).
4. An open benchmark: 25 domains x ~175 queries x 3 systems (~13,000 evaluated pairs).
5. A HuggingFace dataset with one-command reproduction harness.
