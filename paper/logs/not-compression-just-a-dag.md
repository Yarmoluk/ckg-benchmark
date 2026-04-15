# CKG Naming Issue: There Is No Compression

**Date:** 2026-04-14
**Status:** Open — needs author decision before submission

## The Problem

The "C" in CKG stands for "Compressed," but there is no compression algorithm, no compression step, and no lossy or lossless transformation applied to the data. The CSV file is simply authored as a compact, structured representation of domain knowledge. A reviewer will ask: "Where's the compression?"

The honest answer is: there isn't one.

## What's Actually Happening

A domain expert writes a 4-column CSV:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
47,Implicit Differentiation,12|15|3,CORE
```

This row encodes a concept, its prerequisites, and its category in ~60 characters. The equivalent information in a RAG chunk takes ~512 tokens of surrounding prose. The CSV is not compressed *from* something larger — it was authored directly in this compact form.

The token efficiency advantage comes from the **representation choice**, not from a compression process:

- RAG stores knowledge as prose → retrieves noisy chunks → 3,000–5,000 tokens/query
- GraphRAG extracts structure from prose → retrieves summaries → 2,000–8,000 tokens/query
- CKG uses a structured CSV directly → retrieves exact subgraph → 150–400 tokens/query

The CSV is compact because it **only encodes structural relationships** (concept X depends on concepts Y and Z). It does not contain explanatory text, examples, or context. That's not compression — that's a different representation serving a different purpose.

## Alternative Names

| Name | Pros | Cons |
|------|------|------|
| **Compressed Knowledge Graphs** (current) | Catchy, implies efficiency | Misleading — no compression step |
| **Compact Knowledge Graphs** | Honest about small footprint | Doesn't imply an algorithm |
| **Curated Knowledge Graphs** | Emphasizes expert authoring | Doesn't highlight efficiency |
| **Canonical Knowledge Graphs** | Emphasizes authoritative source | Too formal |
| **CSV Knowledge Graphs** | Dead simple, says what it is | Not academic enough |
| **Concise Knowledge Graphs** | Accurate, implies density | Weaker branding |

## Recommendation

If keeping the CKG acronym is important for branding consistency with Daniel's prior work, **"Compact Knowledge Graphs"** is the safest rename — it preserves the acronym while removing the implication of an algorithmic compression step.

If accuracy matters more than acronym preservation, **"Curated Knowledge Graphs"** best describes the actual process: an expert curates a DAG of concepts and dependencies, and that curated structure is used directly for retrieval.

## Action Required

Authors should decide before ArXiv submission. This will affect the paper title, abstract, and all references to "CKG" throughout.
