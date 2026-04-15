# Query Types

The benchmark defines five query types (T1--T5), each testing a different retrieval capability.

## T1: Entity Lookup

- **Question pattern:** "What is {ConceptLabel}?"
- **Ground truth:** ConceptLabel + TaxonomyID
- **Hop depth:** 0
- **Per domain:** ~50 queries (random sample)

Tests basic concept retrieval. All three systems should perform well here.

## T2: Direct Dependency

- **Question pattern:** "What are the prerequisites for {ConceptLabel}?"
- **Ground truth:** Labels of all direct dependencies
- **Hop depth:** 1
- **Per domain:** ~50 queries (concepts with at least 1 dependency)

Tests single-hop relationship retrieval. CKG reads directly from the Dependencies column.

## T3: Multi-Hop Path

- **Question pattern:** "What is the prerequisite chain from {A} to {B}?"
- **Ground truth:** Complete BFS path labels
- **Hop depth:** 2--5
- **Per domain:** ~25 queries

Tests transitive reasoning across multiple hops. This is where CKG's structural advantage is largest---RAG must infer transitive dependencies from unstructured text.

## T4: Category Aggregate

- **Question pattern:** "List all {TaxonomyID} concepts in this knowledge graph"
- **Ground truth:** All concepts matching the taxonomy filter
- **Hop depth:** 0
- **Per domain:** ~12--17 queries (one per taxonomy category)

Tests category-level retrieval. CKG filters by TaxonomyID column for exact completeness.

## T5: Cross-Concept Relationship

- **Question pattern:** "How does {A} relate to {B}?"
- **Ground truth:** Shared neighbors + direct dependency
- **Hop depth:** 1
- **Per domain:** ~38 queries

Tests relational understanding between connected concepts.

## Query Distribution

| Type | Queries/Domain | Total (~22 domains) | Hop Depth |
|------|----------------|---------------------|-----------|
| T1 | ~50 | ~1,100 | 0 |
| T2 | ~50 | ~1,100 | 1 |
| T3 | ~25 | ~550 | 2--5 |
| T4 | ~15 | ~330 | 0 |
| T5 | ~38 | ~836 | 1 |
| **Total** | **~175** | **~3,854** | |
