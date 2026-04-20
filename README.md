# CKG Benchmark

**Pre-structured knowledge graphs outperform RAG by 4× F1 using 11× fewer tokens per query — across 45 domains.**

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Complete](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()
[![Domains: 45](https://img.shields.io/badge/Domains-45-green.svg)]()
[![Queries: 7,928](https://img.shields.io/badge/Queries-7%2C928-green.svg)]()
[![Version: 0.6.2](https://img.shields.io/badge/Paper-v0.6.2-blue.svg)]()

> **Deploy this architecture in your organization → [graphifymd.com](https://graphifymd.com)**

---

## Read the Paper

> **[→ Read the paper (graphifymd.com/paper.html)](https://graphifymd.com/paper.html)**
>
> **[→ Download PDF](https://github.com/Yarmoluk/ckg-benchmark/raw/main/paper/main.pdf)**

| Format | Link |
|--------|------|
| HTML pre-print (full paper) | [paper/paper.html](paper/paper.html) — renders in browser |
| PDF | [paper/main.pdf](paper/main.pdf) — download or view |
| Mobile-optimized | [paper/read-on-phone.html](paper/read-on-phone.html) |
| LaTeX source | [paper/main.tex](paper/main.tex) — v0.6.2 |
| ArXiv | Pre-print in preparation |

---

## Results at a Glance

| System | Macro F1 | Tokens/query | RDS | Run Cost |
|--------|----------|-------------|-----|----------|
| **CKG** | **0.4709** | **269** | **0.00201** | **$7.81** |
| RAG | 0.1231 | 2,982 | 0.0000482 | $76.23 |
| GraphRAG | 0.1200 | 3,450 | 0.0000452 | $44.43 |

**42× more intelligence per token than RAG. Zero hallucinations by construction.**

### F1 by Query Type

| System | T1 entity | T2 dependency | T3 path | T4 aggregate | T5 cross |
|--------|-----------|--------------|---------|-------------|---------|
| **CKG** | 0.207 | **0.634** | **0.660** | **0.964** | **0.323** |
| RAG | 0.094 | 0.078 | 0.201 | 0.286 | 0.115 |
| GraphRAG | 0.108 | 0.073 | 0.208 | 0.054 | 0.183 |

### F1 by Hop Depth — CKG gets stronger, RAG plateaus

| System | hop=0 | hop=1 | hop=2 | hop=3 | hop=4 | hop=5 |
|--------|-------|-------|-------|-------|-------|-------|
| **CKG** | 0.374 | 0.519 | 0.573 | 0.671 | 0.751 | **0.772** |
| RAG | 0.073 | 0.066 | 0.226 | 0.138 | 0.166 | 0.170 |

### Track 2 — Commercial Domain (GLP-1/Obesity, pipeline-generated)

| System | Macro F1 | Tokens/query | RDS |
|--------|----------|-------------|-----|
| **CKG** | **0.5298** | 346 | 0.00153 |
| RAG | 0.1538 | 2,828 | 0.0000544 |
| GraphRAG | 0.1436 | 3,450 | 0.0000416 |

Built from the ClinicalTrials.gov API in one automated session — no expert curation. CKG F1 exceeds the hand-curated Track 1 average by 12.5%.

---

## What Is CKG?

Three architectures. Same questions. Wildly different results.

| System | Knowledge representation | Retrieval | Tokens/query |
|--------|--------------------------|-----------|--------------|
| **RAG** | Chunked text + vector embeddings | Cosine similarity, top-5 | ~2,982 |
| **GraphRAG** | Dynamically extracted entity graph | Community search | ~3,450 |
| **CKG** | Pre-structured DAG + taxonomy | BFS/DFS subgraph extraction | ~269 |

**Core finding:** Pre-structured knowledge graphs (CKG) outperform RAG and GraphRAG on structural queries — dependency resolution, multi-hop path traversal, category aggregation — at 11× lower token cost and zero hallucination rate.

The advantage holds whether knowledge is hand-curated (Track 1, 44 educational domains) or assembled programmatically from external APIs (Track 2, pharma domain). Structure is the signal — not curation effort.

---

## Two-Track Design

### Track 1 — McCreary Intelligent Textbook Corpus
44 open-source educational domains with hand-authored learning-graph CSVs:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Function,,FOUND
2,Domain and Range,1,FOUND
4,Composite Function,1|3,FOUND
```

- **44 domains** · **12,260+ concepts** · **7,758 queries** · STEM, Professional, Foundational

### Track 2 — Pipeline-Generated Commercial Domain
GLP-1/Obesity pharmacology — assembled from the ClinicalTrials.gov API in one session:

- 668 semaglutide trials + 224 tirzepatide trials + 158 pipeline agents indexed
- 90 concepts · 170 dependency edges · 170 benchmark queries
- No expert curation · No proprietary data · CKG F1 = 0.5298

---

## Query Types

| Type | Description | Example |
|------|-------------|---------|
| **T1** | Entity lookup | "What is Composite Function?" |
| **T2** | Direct dependency | "What are the prerequisites for Implicit Differentiation?" |
| **T3** | Multi-hop path | "What is the prerequisite chain from Function to Taylor Series?" |
| **T4** | Category aggregate | "List all FOUND concepts" |
| **T5** | Cross-concept relationship | "How does Domain and Range relate to Inverse Function?" |

---

## Novel Metrics

| Metric | Formula | What It Measures |
|--------|---------|------------------|
| **RDS** | F1 / tokens_consumed | Intelligence per token — the compound efficiency score |
| **Hop-Depth F1** | F1 at hop depth k=0…5 | Multi-hop reasoning quality vs. chain length |
| **CUR** | relevant_tokens / total_retrieved | Retrieval precision |
| **CPCA** | cost_per_query / F1 | Real-world cost efficiency |
| **Hallucination Rate** | hallucinated_concepts / total | CKG = 0 by construction |

---

## Falsifiable Claims — All Confirmed

1. ✅ CKG achieves higher F1 on T2 (dependency) and T3 (multi-hop) queries — **confirmed** (0.634 vs 0.078; 0.660 vs 0.201)
2. ✅ CKG F1 does not degrade with hop depth — **confirmed and stronger**: improves continuously to hop=5 (0.772)
3. ✅ CKG RDS ≥ 10× vs RAG — **confirmed**: 42×
4. ✅ CKG Hallucination Rate = 0 by construction — **confirmed**
5. ✅ Structure Premium hypothesis — **null result**: r = −0.09; advantage is uniform across all DAG richness levels
6. ✅ Track 2 cross-domain transfer — **confirmed**: pipeline-generated pharma F1 = 0.530 > hand-curated average 0.471

---

## Quick Start

```bash
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install -r evaluation/requirements.txt

# Run CKG on a domain
python evaluation/ckg_harness.py --domain calculus

# Run RAG on a domain
python evaluation/rag_harness.py --domain calculus

# Analyze all results
python evaluation/analyze_results.py
```

---

## Repository Structure

```
ckg-benchmark/
├── benchmark/
│   ├── domains/          # 45 domain directories with learning-graph.csv
│   └── queries/          # JSONL query files per domain
├── corpus/               # Prose corpus for RAG and GraphRAG
│   └── glp1-obesity/     # Track 2 commercial corpus (5 documents)
├── evaluation/
│   ├── ckg_harness.py    # CKG runner
│   ├── rag_harness.py    # RAG runner (FAISS)
│   ├── graphrag_harness.py
│   ├── generate_queries.py
│   └── analyze_results.py
├── results/
│   ├── ckg/              # Per-domain JSONL results (45 domains)
│   ├── rag/              # Per-domain JSONL results (40 domains)
│   ├── graphrag/         # Per-domain JSONL results (15 domains)
│   └── tables/           # Final summary CSVs
└── paper/
    ├── main.tex          # LaTeX source — v0.6.2
    ├── main.pdf          # Compiled PDF
    ├── paper.html        # Full paper — readable in browser
    ├── read-on-phone.html
    └── sections/         # 12 section files
```

---

## Commercial Applications

The benchmark numbers translate directly to enterprise cost and accuracy:

| What RAG costs you | What CKG delivers |
|--------------------|-------------------|
| 2,982 tokens/query average | 269 tokens/query — 11× reduction |
| $76.23 to run 7,928 queries | $7.81 for the same workload |
| F1 = 0.123 on structural queries | F1 = 0.471 — 4× more accurate answers |
| Hallucinations on multi-hop chains | Zero hallucinations by construction |
| F1 degrades past hop=2 | F1 improves to hop=5 (0.772) |

**Any domain where knowledge has stable structure — clinical, regulatory, legal, financial, educational — is a candidate.** Track 2 proved this extends beyond hand-curated data: a GLP-1/Obesity pharmacology CKG built entirely from the ClinicalTrials.gov API in one session achieved F1 = 0.530, exceeding the hand-curated educational average.

The architecture is patent-pending (App #64/040,804). Commercial deployment, pilot engagements, and enterprise licensing are available through **[Graphify.md](https://graphifymd.com)**.

> Interested in deploying CKG in your organization? → [graphifymd.com](https://graphifymd.com)

---

## Authors

- **Daniel Yarmoluk** — [Graphify.md](https://graphifymd.com) — CKG architecture, benchmark design, Track 2 pipeline, RDS metric
- **Dan McCreary** — [Intelligent Textbooks](https://github.com/dmccreary) — Source corpus (McCreary Intelligent Textbook Corpus), DAG methodology

## Status

| Component | Status |
|-----------|--------|
| Track 1 CKG results (44 domains, 7,758 queries) | ✅ Complete |
| Track 1 RAG results (40 domains, 7,191 queries) | ✅ Complete |
| Track 1 GraphRAG results (15 domains, 2,683 queries) | ✅ Complete |
| Track 2 GLP-1 domain (all 3 systems, 170 queries each) | ✅ Complete |
| All figures generated | ✅ Complete |
| Paper draft (v0.6.2) | ✅ In review |
| ArXiv submission | Pending Dan McCreary review |
| HuggingFace dataset | Pending |

## License

- **Code:** MIT
- **Benchmark data:** CC BY 4.0
- **Source learning graphs:** MIT ([McCreary Intelligent Textbooks](https://github.com/dmccreary))

## Citation

```bibtex
@misc{yarmoluk2026ckg,
  title={Benchmarking Knowledge Retrieval Architectures Across Educational
         and Commercial Domains: RAG, GraphRAG, and Compact Knowledge Graphs},
  author={Yarmoluk, Daniel and McCreary, Dan},
  year={2026},
  note={Pre-print in preparation. v0.6.2. Patent pending App \#64/040,804.}
}
```
