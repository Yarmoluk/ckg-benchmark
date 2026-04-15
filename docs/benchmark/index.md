# Benchmark Overview

The CKG Benchmark evaluates three retrieval architectures across 22 educational domains using 3,854 auto-generated queries with deterministic ground truth.

## What Makes This Benchmark Unique

1. **Deterministic ground truth** derived from DAG edges (not human annotation)
2. **Five query types** (T1--T5) testing different retrieval capabilities
3. **Efficiency metrics** that account for token cost, not just quality
4. **22 domains** with identical schema enabling cross-domain analysis
5. **One-command reproduction** with fixed random seed (42)

## Benchmark Statistics

| Statistic | Value |
|-----------|-------|
| Domains extracted | 22 |
| Total concepts | 6,351 |
| Total queries | 3,854 |
| Query types | 5 (T1--T5) |
| Systems compared | 3 (RAG, GraphRAG, CKG) |
| Evaluation metrics | 16 (10 novel) |
| Random seed | 42 |

## Domain Categories

| Category | Count | Domains |
|----------|-------|---------|
| STEM | 10 | Calculus, Biology, Genetics, Bioinformatics, Statistics, Quantum Computing, Circuits, Geometry, Ecology, Moss |
| Professional | 7 | Economics, Organizational Analytics, Healthcare Data, Conversational AI, Automating Instructional Design, Blockchain, Claude Skills |
| Foundational | 7 | Systems Thinking, Theory of Knowledge, Digital Citizenship, Prompt Engineering, Tracking AI, US Geography, ASL |

## Data Format

All domain data uses a standardized CSV schema:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Function,,FOUND
2,Domain and Range,1,FOUND
4,Composite Function,1|3,FOUND
```

Queries are stored as JSONL files:

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
