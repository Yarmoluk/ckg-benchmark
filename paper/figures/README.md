# Figures

## Conventions

- **Format:** PNG only (ArXiv-compatible)
- **Resolution:** 300 DPI minimum
- **Size:** Under 1 MB per figure
- **Colors:** High contrast, colorblind-friendly palette
- **Labels:** Use `\label{fig:shortname}` and reference with `\ref{fig:shortname}`
- **Width:** `\includegraphics[width=0.95\textwidth]{figures/filename.png}`

## All 7 Figures

| # | Label | Section | Description | File | Status |
|---|-------|---------|-------------|------|--------|
| 1 | `fig:architecture` | Introduction | Three-architecture pipeline diagram | *placeholder in .tex* | Needs drawing |
| 2 | `fig:f1-token-budget` | Results | F1 vs token budget curves (3 systems) | *pending* | Needs data |
| 3 | `fig:rds-by-domain` | Results | RDS scatter plot (22 domains x 3 systems) | *pending* | Needs data |
| 4 | `fig:hop-degradation` | Results | Hop-depth F1 degradation curves | *pending* | Needs data |
| 5 | `fig:corpus-heatmap` | Corpus | Per-domain statistics heatmap | `corpus-heatmap.png` | Done |
| 6 | `fig:token-composition` | Results | Token composition stacked bars | `token-composition.png` | Done |
| 7 | `fig:structure-premium` | Discussion | RDS ratio vs DAG richness correlation | *pending* | Needs data |

## Planned Tables

Tables are defined inline in section files (not separate figures):

| # | Label | Section | Description |
|---|-------|---------|-------------|
| 1 | `tab:macro-results` | Results | Macro-average F1, EM, tokens, RDS, CPCA |
| 2 | `tab:f1-by-type` | Results | F1 by query type T1--T5 |
| 3 | `tab:paradigms` | Introduction | Three paradigms comparison |
| 4 | `tab:query-types` | Benchmark Design | Query taxonomy |
| 5 | `tab:rag-config` | Architecture | RAG configuration |
| 6 | `tab:graphrag-config` | Architecture | GraphRAG configuration |
| 7 | `tab:ckg-config` | Architecture | CKG configuration |

## Generation Scripts

```bash
# Figure 5: Corpus heatmap (uses real CSV data)
python paper/figures/create_corpus_heatmap.py

# Figure 6: Token composition (estimated, update after experiments)
python paper/figures/create_token_composition.py
```

## Figure 1: Architecture Diagram

This should be created manually in draw.io or similar. It shows three parallel
pipelines side by side:

- **RAG:** MkDocs chapters -> chunking -> embeddings -> FAISS top-5 -> Claude
- **GraphRAG:** MkDocs chapters -> entity extraction -> graph communities -> Claude
- **CKG:** learning-graph.csv -> concept lookup -> BFS/DFS subgraph -> Claude
