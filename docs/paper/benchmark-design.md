# Benchmark Design

## Query Taxonomy

We define five query types (T1--T5), each targeting a different aspect of knowledge retrieval capability.

| Type | Description | Example | Ground Truth Source |
|------|-------------|---------|---------------------|
| **T1** | Entity lookup | "What is Composite Function?" | ConceptLabel + TaxonomyID |
| **T2** | Direct dependency | "What are prerequisites for Composite Function?" | Dependencies column |
| **T3** | Multi-hop path | "What is the chain from Function to Taylor Series?" | BFS path in DAG |
| **T4** | Category aggregate | "List all FOUND concepts" | Filter by TaxonomyID |
| **T5** | Cross-concept relationship | "How does Domain and Range relate to Inverse Function?" | Shared neighbors |

## Query Generation

Queries are auto-generated from each domain's CSV using `generate_queries.py` with a fixed random seed of 42.

**Per domain:** ~175 queries (50 T1 + 50 T2 + 25 T3 + 12 T4 + 38 T5)

**Total:** ~4,375 queries across 25 domains

### Generation Rules

- **T1**: Random sample of 50 concepts; query is "What is {label}?"
- **T2**: Random sample of 50 concepts with at least 1 dependency
- **T3**: Random pairs of foundational/terminal concepts with path length 2--5
- **T4**: One query per taxonomy category
- **T5**: Random sample of 38 directly connected concept pairs

### Query Format (JSONL)

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

## Human Validation

A 5% sample (~220 queries) is reviewed by two annotators. Cohen's kappa is reported for inter-annotator agreement.

## Reproducibility Protocol

- All systems use Claude Sonnet 4.6 at temperature=0
- Token counts via Anthropic `count_tokens()` API
- 3 runs per query, variance reported
- Fixed random seed: 42
- Benchmark version locked: v1.0.0
- One-command reproduction: `python evaluation/harness.py --reproduce-table-1`
