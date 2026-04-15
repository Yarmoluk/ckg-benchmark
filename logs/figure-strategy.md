# Figure Strategy

**Paper:** Benchmarking Knowledge Retrieval Architectures Across 25 Domains
**Date:** 2026-04-14
**Total figures:** 8 (3 done, 1 placeholder, 4 awaiting experimental data)

## Design Rationale

A typical ArXiv AI paper has 5--8 figures. We target 8 to cover three roles:

1. **Orientation** (Figures 1--2): Help readers understand what we're comparing and what the data looks like before seeing any results.
2. **Evidence** (Figures 3--7): Present experimental results across multiple dimensions --- efficiency curves, per-domain analysis, hop-depth degradation, token breakdown, and structural metrics.
3. **Theory** (Figure 8): Validate the Structure Premium hypothesis with a correlation plot.

## Figure Inventory

| # | Label | Section | Role | File | Status |
|---|-------|---------|------|------|--------|
| 1 | `fig:architecture` | Introduction | Orientation | *placeholder in .tex* | Needs draw.io diagram |
| 2 | `fig:learning-graph` | Corpus | Orientation | `calculus-learning-graph.png` | **Done** |
| 3 | `fig:f1-token-budget` | Results | Evidence | --- | Needs experimental data |
| 4 | `fig:rds-by-domain` | Results | Evidence | --- | Needs experimental data |
| 5 | `fig:hop-degradation` | Results | Evidence | --- | Needs experimental data |
| 6 | `fig:corpus-heatmap` | Corpus | Orientation | `corpus-heatmap.png` | **Done** |
| 7 | `fig:token-composition` | Results | Evidence | `token-composition.png` | **Done** (estimated) |
| 8 | `fig:structure-premium` | Discussion | Theory | --- | Needs experimental data |

## Figure Descriptions

### Figure 1: Three-Architecture Pipeline Diagram
**Section:** Introduction | **Status:** Placeholder
Three parallel pipelines showing how each system processes a query:

- RAG: MkDocs chapters -> 512-token chunks -> embeddings -> FAISS top-5 -> Claude
- GraphRAG: MkDocs chapters -> entity extraction -> graph communities -> Claude
- CKG: learning-graph.csv -> concept lookup -> BFS/DFS subgraph -> Claude

**Action:** Create in draw.io or Figma. This is the "money figure" that readers scan first.

### Figure 2: Calculus Learning Graph Screenshot
**Section:** Corpus | **Status:** Done
Screenshot of the interactive learning graph viewer for the calculus domain (380 concepts, 539 edges). Shows color-coded taxonomy categories, directed prerequisite edges, category filters, and corpus statistics. Gives readers a concrete visual of what a learning graph DAG looks like.

**Source:** `docs/img/calculus-learning-graph.png`

### Figure 3: F1 vs Token Budget Curves
**Section:** Results | **Status:** Blocked on experiments
Line plot with token budget on x-axis (100, 250, 500, 1000, 2000, 5000, 10000) and mean F1 on y-axis. One line per system.

**Expected shape:** CKG plateaus at ~400 tokens. RAG rises slowly, plateaus at ~4,000. GraphRAG has high variance.

**Generation:** Python/matplotlib script after `harness.py` runs.

### Figure 4: RDS by Domain Scatter Plot
**Section:** Results | **Status:** Blocked on experiments
Scatter plot with 22 points per system (one per domain). X-axis: domain, Y-axis: RDS. Three colors for RAG/GraphRAG/CKG.

**Purpose:** Shows whether CKG's RDS advantage is consistent across all domains or varies.

### Figure 5: Hop-Depth F1 Degradation Curves
**Section:** Results | **Status:** Blocked on experiments
Line plot with hop depth (k=1,2,3,4,5+) on x-axis and F1 on y-axis. One line per system.

**Expected shape:** RAG degrades steeply at k>=2. CKG stays flat. This is the key structural argument figure.

### Figure 6: Corpus Heatmap
**Section:** Corpus | **Status:** Done
Heatmap showing per-domain statistics (concepts, edges, taxonomy categories, foundation concepts, edge/concept ratio) across all 22 domains grouped by category.

**Generated from real data:** 6,206 concepts, 10,342 edges.
**Script:** `paper/figures/create_corpus_heatmap.py`

### Figure 7: Token Composition Stacked Bars
**Section:** Results | **Status:** Done (estimated values)
Stacked bar chart breaking down tokens per query: query, system prompt, retrieval context, completion. One bar per system.

**Key visual:** RAG bar is 13x taller than CKG, dominated by retrieval context (red).
**Script:** `paper/figures/create_token_composition.py`
**Note:** Update with actual token counts after experiments.

### Figure 8: Structure Premium Correlation
**Section:** Discussion | **Status:** Blocked on experiments
Scatter plot with DAG richness on x-axis and RDS ratio (CKG/RAG) on y-axis. 22 points (one per domain). Include regression line and Pearson r value.

**Purpose:** Validates or falsifies the Structure Premium hypothesis (target: r > 0.7).

## Conventions

- **Format:** PNG only (ArXiv compatible)
- **Resolution:** 300 DPI minimum
- **Size:** Under 1 MB per figure
- **Colors:** High contrast, colorblind-friendly
- **LaTeX labels:** `\label{fig:shortname}` referenced with `\ref{fig:shortname}`
- **Width:** `\includegraphics[width=0.95\textwidth]{figures/filename.png}` (or 0.85 for smaller)
- **Generation scripts** live alongside PNGs in `paper/figures/`

## Blocking Dependencies

Figures 3, 4, 5, 8 all require experimental results from `evaluation/harness.py`. Figure 7 uses estimated values that should be updated with actuals. Figure 1 needs manual creation in a diagramming tool.

**Critical path:** Implement `harness.py` -> run experiments -> generate figures 3, 4, 5, 8 -> update figure 7 -> draw figure 1 -> paper is figure-complete.
