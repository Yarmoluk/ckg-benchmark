# Figures

## Conventions

- **Format:** PNG only (ArXiv-compatible)
- **Resolution:** 300 DPI minimum
- **Size:** Under 1 MB per figure
- **Colors:** High contrast, colorblind-friendly palette
- **Labels:** Use `\label{fig:shortname}` and reference with `\ref{fig:shortname}`
- **Width:** `\includegraphics[width=0.95\textwidth]{figures/filename.png}`

## Planned Figures

| # | Label | Section | Description | Status |
|---|-------|---------|-------------|--------|
| 1 | `fig:f1-token-budget` | Results | F1 vs token budget curves (3 systems) | Pending |
| 2 | `fig:rds-by-domain` | Results | RDS scatter plot (25 domains x 3 systems) | Pending |
| 3 | `fig:hop-degradation` | Results | Hop-depth F1 degradation curves | Pending |
| 4 | `fig:structure-premium` | Results | RDS ratio vs DAG richness correlation | Pending |

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

## Creating Figures

Use Python/matplotlib for data-driven charts. Place generation scripts alongside
the output PNG:

```bash
python figures/create_hop_degradation.py  # generates fig:hop-degradation
```
