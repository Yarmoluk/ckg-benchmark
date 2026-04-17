# CLAUDE.md -- Project Instructions for Claude Code

## Project Overview

This is the **CKG Benchmark** repository -- a reproducible benchmark comparing three LLM knowledge retrieval architectures (RAG, GraphRAG, Compact Knowledge Graphs) across 46 educational domains. The benchmark uses the McCreary Intelligent Textbook Corpus as its data source.

**Authors:** Daniel Yarmoluk (Graphify.md) and Dan McCreary
**Target:** ArXiv paper (cs.IR primary, cs.AI secondary) + HuggingFace dataset

## Repository Layout

```
benchmark/domains/{domain}/learning-graph.csv  -- Source data (22 domains, 6,351 concepts)
benchmark/queries/queries_{domain}.jsonl       -- Generated benchmark queries (3,854 total)
evaluation/generate_queries.py                 -- Query generator from CSV DAGs
evaluation/metrics.py                          -- All metric implementations
evaluation/harness.py                          -- Main experiment runner (placeholder)
evaluation/requirements.txt                    -- Python dependencies
metrics/metrics-spec.md                        -- Full metric definitions (16 metrics)
metrics/tokenomics.md                          -- Token cost accounting framework
paper/outline.md                               -- Paper structure and abstract
huggingface/dataset-card.md                    -- HuggingFace dataset card
```

## Key Conventions

### CSV Schema (all domains use this)
```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
```
- `Dependencies` is pipe-delimited (`1|3|5`)
- `TaxonomyID` is a domain-specific category label (e.g., `FOUND`, `CORE`, `ADV`)

### Query Types
- **T1** = entity lookup, **T2** = direct dependency, **T3** = multi-hop path
- **T4** = category aggregate, **T5** = cross-concept relationship

### Query ID Format
`{domain}_T{n}_{concept_id}` (e.g., `calculus_T2_47`)

### Metrics (novel ones starred)
- Token F1, Edge F1, Exact Match (standard)
- *RDS = F1 / tokens_consumed (core novel metric)
- *Hop-Depth F1 Degradation
- *CUR (Context Utilization Rate)
- *CPCA (Cost Per Correct Answer)
- *Relationship Precision, Hub Node Recall, Boundary Completeness
- Hallucination Rate, Paraphrase Stability

### Pricing Constants
Claude Sonnet 4.6: $3/M input tokens, $15/M output tokens

## Development Commands

```bash
# Install dependencies
pip install -r evaluation/requirements.txt

# Generate queries for a domain
python evaluation/generate_queries.py \
  --csv benchmark/domains/calculus/learning-graph.csv \
  --domain calculus \
  --output benchmark/queries/queries_calculus.jsonl

# Run experiments (when harness.py is complete)
python evaluation/harness.py \
  --queries benchmark/queries/queries_calculus.jsonl \
  --systems rag graphrag ckg \
  --output results/

# Extract corpus from McCreary GitHub repos (requires gh CLI)
bash extract_corpus.sh
```

## Code Style

- Python 3.10+ with type hints
- Use `dataclass` for structured data (see `QueryResult` in metrics.py)
- Random seed: 42 for all query generation
- Temperature: 0 for all LLM calls
- Use `defaultdict` and `statistics` module patterns already established

## Architecture Details

### Three Systems Being Compared
1. **RAG:** MkDocs chapters -> 512-token chunks -> FAISS -> top-5 retrieval -> Claude
2. **GraphRAG:** MkDocs chapters -> Microsoft GraphRAG v1.x -> local/global search -> Claude
3. **CKG:** learning-graph.csv -> BFS/DFS subgraph extraction -> Claude

### Key Insight
GraphRAG dynamically extracts structure from text that was *originally generated from* the learning-graph CSV. CKG uses the CSV directly. The efficiency gap is structural, not incidental.

## What Still Needs to Be Done

- Implement `harness.py` to run all 3 systems end-to-end
- Execute experiments across all 22 domains
- Generate results tables (Tables 1-5 in paper outline)
- Validate the Structure Premium hypothesis (RDS vs DAG richness correlation)
- Finalize paper for ArXiv submission
- Publish dataset to HuggingFace (`graphify-md/ckg-benchmark`)

## Paper Versioning

The paper version lives in exactly one place:

```latex
\newcommand{\paperversion}{MAJOR.MINOR.PATCH}
```

at the top of `paper/main.tex`. It renders on the title page via the
`\date{}` line. Bump it whenever you make a substantive change; do **not**
bump it for every edit.

Use semantic-version discipline:

- **PATCH** (`0.4.0` -> `0.4.1`) -- typo fixes, spelling corrections,
  grammar tweaks, figure-caption polish, formatting adjustments,
  citation-style fixes, broken-link repairs. Anything that does not
  change the paper's claims, numbers, or structure. **Small copyedits
  only ever touch the patch number.**
- **MINOR** (`0.4.1` -> `0.5.0`) -- new section or subsection,
  methodology changes, new figure or table, replacing an estimate with
  measured data, refactoring an argument, adding or removing a
  hypothesis. Anything a reviewer would notice beyond a diff of minor
  wording.
- **MAJOR** (`0.x.y` -> `1.0.0`) -- reserved for the frozen ArXiv
  submission. After 1.0.0, further major bumps mark subsequent
  substantive revisions (e.g., post-review v2).

Rules:

1. One bump per coherent change set. If a session fixes three typos, that
   is one PATCH bump, not three.
2. Never decrement. If a change has to be rolled back, bump forward to a
   new version that reflects the rollback.
3. When in doubt between PATCH and MINOR, ask: *"would a reader reviewing
   the change set learn anything they did not already know from the
   previous version?"* If yes, it is at least MINOR.
4. The `\paperversion` macro is the single source of truth. Do not
   hardcode version strings anywhere else in the paper.

## Important Notes

- The `corpus/` directory (cloned repos) is gitignored -- only extracted CSVs are committed
- Ground truth is deterministic (derived from DAG edges, not human annotation)
- 5 domains from the original 27 may be missing CSVs -- check `benchmark/corpus-index.md`
- All source repos are MIT licensed
