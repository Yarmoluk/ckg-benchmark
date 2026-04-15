# Why CSV Over JSON for Learning Graph Representation

**Date:** 2026-04-14
**Context:** Design decision for the CKG benchmark corpus format

## Decision

The benchmark uses the 4-column CSV files (`ConceptID, ConceptLabel, Dependencies, TaxonomyID`) rather than the JSON files also present in McCreary textbook repos.

## Reasons

### 1. Schema Uniformity Across 25 Domains

Every McCreary textbook stores its learning graph at `docs/learning-graph/learning-graph.csv` with an identical 4-column schema. This flat, rigid structure makes cross-domain comparison trivial. JSON files in these repos vary in structure, nesting, and field names across domains.

### 2. The CSV Is the Ground Truth

The benchmark's ground truth is derived directly from DAG edges in the CSV:

- **T2 queries:** Direct dependency lookups from the `Dependencies` column
- **T3 queries:** BFS paths computed over the DAG adjacency list
- **T4 queries:** Taxonomy filters on the `TaxonomyID` column

The pipe-delimited `Dependencies` column encodes the DAG adjacency list in a single field. `generate_queries.py` can parse any domain's CSV with ~10 lines of code and produce deterministic, reproducible queries with no schema negotiation.

### 3. CKG's Efficiency Claim Depends on Minimal Representation

The core argument of the paper is that CKG achieves high F1 at 150--400 tokens per query *because* the knowledge representation is compressed. A 4-column CSV row like:

```
47,Implicit Differentiation,12|15|3,CORE
```

encodes a concept, its prerequisites, and its category in ~60 characters. The equivalent JSON with nested objects, arrays, and field names would be 3--5x larger, undermining the tokenomics argument.

### 4. Zero Build Cost

CKG's claimed advantage is zero indexing cost --- the CSV *is* the index. If the representation were JSON, you'd either need to parse nested structures into a graph (adding build cost) or maintain a flattened JSON that's functionally a worse CSV.

### 5. The JSON Files Serve a Different Purpose

The JSON files in McCreary repos (when they exist) are typically for the interactive vis-network viewer. They contain rendering metadata (x/y positions, colors, group assignments) that is irrelevant to the retrieval benchmark. The CSV is the canonical source of *structural* knowledge; the JSON is a *visualization* artifact derived from it.

## Summary

| Factor | CSV | JSON |
|--------|-----|------|
| Schema consistency across 25 repos | Identical 4-column schema | Varies per repo |
| Token efficiency | ~60 chars per concept | 180--300 chars per concept |
| Build cost for CKG | Zero (direct lookup) | Parsing required |
| Ground truth derivation | Direct from columns | Requires field mapping |
| Contains rendering metadata | No | Yes (irrelevant to benchmark) |
| Deterministic query generation | Trivial | Requires schema negotiation |
