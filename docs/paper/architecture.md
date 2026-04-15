# Architecture Specifications

All three systems use Claude Sonnet 4.6 at temperature=0 for generation, ensuring fair comparison. The systems differ only in how knowledge is stored and retrieved.

## RAG Baseline

| Parameter | Value |
|-----------|-------|
| Source | MkDocs `.md` chapters per textbook |
| Chunking | 512 tokens, 50-token overlap |
| Embeddings | `text-embedding-3-small` (OpenAI) |
| Index | FAISS flat L2 |
| Retrieval | Top-5 chunks |
| Generation | Claude Sonnet 4.6, temperature=0 |

**Token profile:** 3,000--5,000 tokens per query. High noise ratio (chunks contain off-topic content).

## GraphRAG

| Parameter | Value |
|-----------|-------|
| Source | Same MkDocs `.md` chapters |
| System | Microsoft GraphRAG v1.x, default configuration |
| Search | Local mode for T1/T2/T5, global mode for T4 |
| Note | Does **not** use `learning-graph.csv`---dynamic extraction only |
| Generation | Claude Sonnet 4.6, temperature=0 |

**Token profile:** 2,000--8,000 tokens per query (high variance). Medium noise ratio. Build cost: HIGH.

## CKG (Compressed Knowledge Graph)

| Parameter | Value |
|-----------|-------|
| Source | `learning-graph.csv` (ConceptID, ConceptLabel, Dependencies, TaxonomyID) |
| Lookup | Exact label match -> concept node retrieval |
| Traversal | BFS for T2 (1-hop), DFS for T3 (full path), filter for T4 |
| Subgraph | Matched concept + direct neighbors + edges |
| Generation | Claude Sonnet 4.6, temperature=0 |
| Note | Zero build cost---CSV-native |

**Token profile:** 150--400 tokens per query. Near-zero noise ratio.

## Key Distinction

!!! important "The Structural Efficiency Gap"
    GraphRAG re-derives structure from text that was originally generated **from** the learning graph CSV. CKG uses the graph directly. The efficiency gap is structural, not incidental.
