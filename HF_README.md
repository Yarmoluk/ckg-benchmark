---
license: cc-by-4.0
task_categories:
- question-answering
- text-retrieval
tags:
- knowledge-graph
- rag
- retrieval
- benchmark
- llm
- knowledge-representation
language:
- en
pretty_name: CKG Benchmark
size_categories:
- 10K<n<100K
---

# CKG Benchmark

**Pre-structured knowledge graphs outperform RAG by 4× F1 at 11× lower token cost — across 47 benchmarked domains.**

| System | Macro F1 | Tokens/query | RDS | Run Cost |
|--------|----------|-------------|-----|----------|
| **CKG** | **0.4709** | **269** | **0.00175** | **$7.81** |
| RAG | 0.1231 | 2,982 | 0.0000413 | $76.23 |
| GraphRAG | 0.1200 | 3,450 | 0.0000452 | $44.43 |

**42× more intelligence per token than RAG. Zero hallucinations by construction.**

## Dataset Contents

```
domains/{domain}/learning-graph.csv   — structured DAG (ConceptID, ConceptLabel, Dependencies, TaxonomyID)
queries/queries_{domain}.jsonl        — 7,928 benchmark queries (T1–T5 types)
results/                              — per-system JSONL results + summary CSVs
```

## Domain Library (52 total)

### Benchmarked Educational Domains (47)

| Domain | Category |
|--------|----------|
| algebra-1 | Mathematics |
| asl-book | Language |
| automating-instructional-design | Education Technology |
| bioinformatics | Life Sciences |
| biology | Life Sciences |
| blockchain | Computer Science |
| calculus | Mathematics |
| chemistry | Natural Science |
| circuits | Engineering |
| claude-skills | AI / LLM |
| computer-science | Computer Science |
| conversational-ai | AI / LLM |
| data-science-course | Data Science |
| dementia | Healthcare |
| digital-citizenship | Social / Civic |
| digital-electronics | Engineering |
| ecology | Natural Science |
| economics-course | Social Science |
| ethics-course | Philosophy |
| fft-benchmarking | Signal Processing |
| functions | Mathematics |
| genetics | Life Sciences |
| geometry-course | Mathematics |
| glp1-obesity | Healthcare / Pharma |
| infographics | Design / Communication |
| intro-to-graph | Computer Science |
| intro-to-physics-course | Natural Science |
| it-management-graph | IT Management |
| learning-linux | Computer Science |
| linear-algebra | Mathematics |
| machine-learning-textbook | AI / Machine Learning |
| microsims | Education Technology |
| modeling-healthcare-data | Healthcare Analytics |
| moss | Biology / Botany |
| organizational-analytics | Business Analytics |
| personal-finance | Finance |
| pre-calc | Mathematics |
| prompt-class | AI / LLM |
| quantum-computing | Computer Science |
| reading-for-kindergarten | Education |
| signal-processing | Engineering |
| statistics-course | Data Science |
| systems-thinking | Systems Science |
| theory-of-knowledge | Philosophy |
| tracking-ai-course | AI / LLM |
| unicorns | Business / Finance |
| us-geography | Geography |

### Enterprise Domains (5, unbenchmarked — community contribution)

| Domain | Category | Concepts |
|--------|----------|---------|
| payer-formulary | Healthcare Payer Analytics | 75 |
| drug-interactions | Clinical Pharmacology | 70 |
| icd10-metabolic | Medical Coding | 70 |
| cpt-em-coding | Medical Billing | 80 |
| hipaa-compliance | Healthcare Compliance | 75 |

## Query Types

| Type | Description | Example |
|------|-------------|---------|
| T1 | Entity lookup | "What is Composite Function?" |
| T2 | Direct dependency | "What are the prerequisites for Implicit Differentiation?" |
| T3 | Multi-hop path | "What is the prerequisite chain from Function to Taylor Series?" |
| T4 | Category aggregate | "List all FOUND concepts" |
| T5 | Cross-concept relationship | "How does Domain and Range relate to Inverse Function?" |

## Two-Track Design

**Track 1 — McCreary Intelligent Textbook Corpus**
44 open-source educational domains. Hand-authored learning-graph CSVs. STEM, Professional, Foundational.

**Track 2 — Pipeline-Generated Commercial Domain**
GLP-1/Obesity pharmacology assembled from ClinicalTrials.gov API in one session. No expert curation. CKG F1 = 0.5298 — exceeds hand-curated average.

## Key Finding: CKG improves with hop depth, RAG plateaus

| hop depth | CKG F1 | RAG F1 |
|-----------|--------|--------|
| 0 | 0.374 | 0.073 |
| 1 | 0.519 | 0.066 |
| 2 | 0.573 | 0.226 |
| 3 | 0.671 | 0.138 |
| 4 | 0.751 | 0.166 |
| **5** | **0.772** | 0.170 |

## Novel Metrics

- **RDS** (Retrieval Density Score) = F1 / tokens_consumed — intelligence per token
- **Hop-Depth F1** — multi-hop reasoning quality vs. chain length
- **CPCA** — cost per correct answer

## Citation

```bibtex
@misc{yarmoluk2026ckg,
  title={Benchmarking Knowledge Retrieval Architectures Across Educational
         and Commercial Domains: RAG, GraphRAG, and Compact Knowledge Graphs},
  author={Yarmoluk, Daniel and McCreary, Dan},
  year={2026},
  note={Pre-print in preparation. v0.6.2. Patent pending App #64/040,804.}
}
```

## Links

- Paper: [graphifymd.com/paper.html](https://graphifymd.com/paper.html)
- Benchmark repo: [github.com/Yarmoluk/ckg-benchmark](https://github.com/Yarmoluk/ckg-benchmark)
- MCP server: [github.com/Yarmoluk/ckg-mcp](https://github.com/Yarmoluk/ckg-mcp) — `pip install ckg-mcp`
- Live demo: [huggingface.co/spaces/danyarm/ckg-demo](https://huggingface.co/spaces/danyarm/ckg-demo)
- Commercial deployment: [graphifymd.com](https://graphifymd.com)

## License

- Dataset: CC BY 4.0
- Source learning graphs: MIT (McCreary Intelligent Textbooks)
- Enterprise domains: CC BY 4.0
