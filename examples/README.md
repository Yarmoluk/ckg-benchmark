# CKG Context Examples

This directory contains worked examples of the **compressed knowledge graph contexts** that CKG sends to Claude for each query type. These are the actual structured text files that produce the benchmark's token efficiency results.

## What "compressed markdown" means

Instead of sending 3,000 tokens of raw chapter text (RAG), CKG extracts the exact subgraph relevant to the query and sends it as a structured list. The result is:

| Metric | CKG | RAG | Ratio |
|---|---|---|---|
| Mean tokens | **274** | 2,983 | **11x cheaper** |
| Macro F1 | **0.4504** | 0.1225 | **3.7x better** |
| RDS (F1/tokens) | **0.001887** | 0.0000411 | **~46x better** |

## Examples by query type

| File | Query Type | F1 | Tokens |
|---|---|---|---|
| [T1_entity_lookup.md](ckg_contexts/T1_entity_lookup.md) | Entity definition | 0.189 | 243 |
| [T2_prerequisites.md](ckg_contexts/T2_prerequisites.md) | Direct prerequisites | 0.603 | 197 |
| [T3_learning_path.md](ckg_contexts/T3_learning_path.md) | Multi-hop path | 0.614 | 325 |
| [T4_category_aggregate.md](ckg_contexts/T4_category_aggregate.md) | Category listing | **0.951** | 573 |
| [T5_cross_concept.md](ckg_contexts/T5_cross_concept.md) | Cross-concept traversal | 0.326 | 334 |

## How the context is generated

The CKG harness (`evaluation/ckg_harness.py`) extracts subgraphs from the domain CSV using BFS/DFS:

```
benchmark/domains/{domain}/learning-graph.csv
    → BFS subgraph extraction
    → Structured markdown context (100–600 tokens)
    → Claude Sonnet 4.6
    → Answer scored against ground truth
```

The context format is:
```
KNOWLEDGE GRAPH SUBGRAPH:
  [TAXONOMY_ID] Concept Label | prerequisites: Prereq1, Prereq2
  [TAXONOMY_ID] Prereq1 | prerequisites: ...
```

This is the `.md` delivery format claimed in USPTO Provisional Patent Application #64/040,804.
