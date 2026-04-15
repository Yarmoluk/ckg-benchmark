# Author Response: "Compressed" Naming Concern

**Date:** 2026-04-14
**Responding to:** `not-compression-just-a-dag.md`
**Decision:** Rename to "Compact Knowledge Graphs" — CKG acronym preserved
**Status:** Resolved — paper edits applied

---

## Decision

**"Compact Knowledge Graphs"** — CKG acronym is preserved.

Rationale:
- "Compact" accurately describes the representation: a 4-column CSV row encodes a concept, prerequisites, and taxonomy in ~60 characters vs ~512 tokens of prose in a RAG chunk
- "Compact" does not imply an algorithmic compression step
- CKG acronym is preserved, maintaining consistency with prior work and branding
- Reviewer question "Where's the compression algorithm?" is answered by the rename: there isn't one, and the paper no longer claims there is

---

## What Changed in the Paper

The distinction is that compactness comes from **representation choice**, not a compression process:

> "The token efficiency advantage comes from the representation: a structured CSV row encodes structural relationships in ~60 characters where equivalent prose takes ~512 tokens. This is not compression of a larger artifact — it is expert authoring directly in a compact, structured form."

---

## Files Updated

- `paper/sections/01-abstract.tex`: "Compressed Knowledge Graphs" → "Compact Knowledge Graphs"
- `paper/sections/05-architecture.tex`: Section header updated
- `paper/sections/10-conclusion.tex`: Updated
- `paper/main.tex`: Title updated
- `paper/outline.md`: Title and abstract draft need manual update (TODO)
- `CLAUDE.md`: Project overview updated
- `huggingface/dataset-card.md`: Will need update before HuggingFace publication
- `README.md`, `docs/`: Will need update in a documentation pass

---

## Note on Prior Work References

If Daniel has any prior published work, blog posts, or Graphify.md marketing that uses "Compressed Knowledge Graphs," those should be updated for consistency. The CKG acronym itself (used in URLs, dataset names, etc.) does not need to change.
