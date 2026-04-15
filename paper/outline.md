# Paper Outline: CKG Benchmark

## Title

**"Benchmarking Knowledge Retrieval Architectures Across 25 Domains:
RAG, GraphRAG, and Compact Knowledge Graphs on the
McCreary Intelligent Textbook Corpus"**

**ArXiv categories:** cs.IR (primary), cs.AI (secondary)

---

## Abstract (draft)

Retrieval-augmented generation (RAG) and graph-based retrieval (GraphRAG)
are the dominant paradigms for grounding LLM responses in structured knowledge.
Both optimize for retrieval recall while treating token cost as a secondary
concern. We introduce Compact Knowledge Graphs (CKG) — pre-structured DAG
representations with explicit concept taxonomy and pipe-delimited dependency
encoding — and present the first large-scale benchmark comparing all three
architectures across 25 domains.

We evaluate on the McCreary Intelligent Textbook Corpus: 25 open-source
educational domains (calculus, genetics, bioinformatics, economics, quantum
computing, and more), each with a standardized learning graph CSV totaling
~6,000 concepts and ~8,500 dependency edges. We introduce five novel metrics:
Reasoning Density Score (RDS = F1 / tokens), Context Utilization Rate,
Hop-Depth F1 Degradation, Cost Per Correct Answer, and Relationship Precision.

CKG achieves macro-average F1 of X.XX vs X.XX (RAG) and X.XX (GraphRAG),
at Xx fewer tokens, with largest gains on multi-hop dependency queries (T3)
where RAG F1 degrades by XX% per additional hop while CKG remains flat.
RDS ratio: CKG vs RAG = Xx, CKG vs GraphRAG = Xx.

Benchmark, dataset, and evaluation harness are released at
huggingface.co/datasets/graphify-md/ckg-benchmark under CC BY 4.0 / MIT.

---

## 1. Introduction

### 1.1 Motivation
- LLM retrieval quality is typically measured by F1 alone
- Token cost is a production constraint, not a research afterthought
- Domain-specific knowledge has latent structure that RAG discards
- GraphRAG re-derives structure from text — but what if the structure is already known?

### 1.2 The Three Paradigms (Table)

| System | Knowledge representation | Retrieval | Build cost |
|--------|--------------------------|-----------|------------|
| RAG | Unstructured text chunks | Embedding similarity | Embed all chunks |
| GraphRAG | Dynamically extracted graph | Graph + community search | Full entity extraction |
| CKG | Pre-structured DAG + taxonomy | Direct concept/edge lookup | Zero (CSV-native) |

### 1.3 Falsifiable Claims
1. CKG achieves higher F1 on T2 (dependency) and T3 (multi-hop path) queries
2. CKG F1 does not degrade with hop depth; RAG F1 degrades significantly
3. CKG RDS ratio ≥ 10x vs RAG across all 25 domains
4. GraphRAG hallucinates edges not present in ground truth DAG (HR > 0)
5. CKG Hallucination Rate = 0 (by construction)
6. The "Structure Premium" hypothesis: RDS advantage correlates with DAG richness

### 1.4 Contributions
1. CKG architecture specification (format, DAG constraints, taxonomy schema)
2. Five novel evaluation metrics (RDS, CUR, Hop-F1, CPCA, RP)
3. The McCreary Corpus as a formal benchmark dataset (first paper to do so)
4. Open benchmark: 25 domains × ~175 queries × 3 systems (~13,000 evaluated pairs)
5. HuggingFace dataset + one-command reproduction harness

---

## 2. Related Work

### 2.1 Retrieval-Augmented Generation
- Lewis et al. (2020) — Retrieval-Augmented Generation for NLP
- Karpukhin et al. (2020) — Dense Passage Retrieval
- BEIR: Thakur et al. (2021) — Heterogeneous IR Benchmark
- RAGAS: Es et al. (2023) — RAG evaluation framework

### 2.2 Graph-Based Retrieval
- Edge et al. (2024) — From Local to Global: GraphRAG (Microsoft)
- Guo et al. (2024) — LightRAG
- HippoRAG — graph + associative memory
- Distinction: dynamic extraction (GraphRAG) vs pre-structured domain knowledge (CKG)

### 2.3 Knowledge Graphs for LLMs
- Pan et al. (2024) — Unifying LLMs and KGs: a roadmap
- KGQA literature (knowledge graph question answering)
- Structured KGs (Wikidata, UMLS) vs learned graphs (GraphRAG) vs compressed DAGs (CKG)

### 2.4 Evaluation Gaps in IR
- Standard metrics (F1, MRR, NDCG) do not account for token cost
- RAGAS measures faithfulness + relevance but not efficiency
- This paper: first to define RDS and validate it on a multi-domain corpus

### 2.5 Educational Knowledge Graphs
- McCreary (2024) — Intelligent Textbooks methodology
- Learning graph DAGs as structured domain knowledge
- CSV schema: ConceptID | ConceptLabel | Dependencies | TaxonomyID

---

## 3. The McCreary Intelligent Textbook Corpus

*This section formally defines the corpus for the first time in literature.*

### 3.1 Corpus Description
- 25 open-source intelligent textbooks (github.com/dmccreary/*)
- Domains: STEM (calculus, biology, genetics, chemistry, physics, circuits,
  bioinformatics, statistics, quantum computing, geometry, ecology) +
  Professional (economics, organizational analytics, healthcare data modeling,
  database selection, conversational AI, automating instructional design) +
  Foundational (systems thinking, theory of knowledge, digital citizenship,
  prompt engineering, functions, blockchain, AI tracking, ASL)
- Concepts per domain: 200–380 (mean: ~240)
- Total concepts: ~6,000
- Total edges: ~8,500
- Taxonomy categories: 10–17 per domain (domain-specific, standardized structure)
- Raw content: MkDocs Markdown chapters (~3,000–8,000 words per textbook)
- License: MIT

### 3.2 Corpus Schema
```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Function,,FOUND
2,Domain and Range,1,FOUND
4,Composite Function,1|3,FOUND
```

### 3.3 Quality Properties
All 25 DAGs validated for:
- Single connected component
- No self-references
- Foundational concepts (zero prerequisites) ≥ 2 per domain
- Maximum dependency chain reported per domain

---

## 4. Architecture Specifications

### 4.1 RAG Baseline
```
Source:      MkDocs .md chapters per textbook
Chunking:    512 tokens, 50-token overlap
Embeddings:  text-embedding-3-small (OpenAI)
Index:       FAISS flat L2
Retrieval:   top-5 chunks
Generation:  Claude Sonnet 4.6, temperature=0
```

### 4.2 GraphRAG
```
Source:      Same MkDocs .md chapters
System:      Microsoft GraphRAG v1.x, default configuration
Search:      local mode for T1/T2/T5, global mode for T4
Note:        Does NOT use learning-graph.csv — dynamic extraction only
Generation:  Claude Sonnet 4.6, temperature=0
```

### 4.3 CKG (Compact Knowledge Graph)
```
Source:      learning-graph.csv (ConceptID | ConceptLabel | Dependencies | TaxonomyID)
Lookup:      Exact label match → concept node retrieval
Traversal:   BFS for T2 (1-hop), DFS for T3 (full path), filter for T4
Subgraph:    Returns matched concept + direct neighbors + edges
Generation:  Claude Sonnet 4.6, temperature=0
Note:        Zero build cost — CSV-native
```

**Key distinction:** GraphRAG re-derives structure from text that was originally
generated FROM the learning graph CSV. CKG uses the graph directly. The
efficiency gap is structural, not incidental.

---

## 5. Benchmark Design

### 5.1 Query Taxonomy

| Type | Description | Example | Ground truth source |
|------|-------------|---------|---------------------|
| T1 | Entity lookup | "What is Composite Function?" | ConceptLabel + TaxonomyID |
| T2 | Direct dependency | "What are prerequisites for Composite Function?" | Dependencies column |
| T3 | Multi-hop path | "What is the chain from Function to Taylor Series?" | BFS path in DAG |
| T4 | Category aggregate | "List all FOUND concepts" | Filter by TaxonomyID |
| T5 | Cross-concept relationship | "How does Domain and Range relate to Inverse Function?" | Shared neighbors |

### 5.2 Query Generation
Auto-generated from CSV — see `evaluation/generate_queries.py`.

Per domain: ~175 queries (50 T1 + 50 T2 + 25 T3 + 12 T4 + 38 T5)
Total: ~4,375 queries across 25 domains

### 5.3 Human Validation
- 5% sample (~220 queries) reviewed by two annotators
- Cohen's κ reported for inter-annotator agreement
- DAG validation failures handled per domain (documented)

### 5.4 Reproducibility Protocol
- All systems use Claude Sonnet 4.6 at temperature=0
- Token counts via Anthropic `count_tokens()` API
- 3 runs per query, variance reported
- Fixed random seed: 42
- Benchmark version locked: v1.0.0

---

## 6. Metrics

*See `metrics/metrics-spec.md` for full definitions.*

Summary of metrics reported:

**Quality:** Token F1, Edge F1, Exact Match
**Efficiency:** RDS, CUR, CPCA, P@T
**Structure:** Hop-Depth F1, Relationship Precision, Hub Node Recall, Boundary Completeness
**Robustness:** Paraphrase Stability, Hallucination Rate
**Operational:** Index Build Cost, Update Cost

---

## 7. Results

*(Placeholder — filled after experiments)*

### Table 1: Macro-average F1 across 25 domains
### Table 2: F1 by query type (T1–T5)
### Table 3: Token cost and RDS
### Table 4: F1 by hop depth (k=1–5+)
### Table 5: Structural metrics (RP, HNR, BC, HR)
### Figure 1: F1 vs token budget curves (3 systems)
### Figure 2: RDS by domain (scatter, 25 points per system)
### Figure 3: Hop-depth F1 degradation curves
### Figure 4: Structure Premium correlation (RDS ratio vs DAG richness)

---

## 8. Discussion

### 8.1 Where CKG Wins and Why
- T2/T3: explicit edges eliminate multi-hop inference errors
- BC ≈ 1.0 for T4: taxonomy filter is exact
- HR = 0: no hallucinated concepts by construction
- RDS: near-zero build cost + low retrieval tokens

### 8.2 Where RAG Is Competitive
- T1 entity lookup on large open-domain corpora
- Domains without stable taxonomy (rapidly evolving fields)
- When CKG construction is too expensive

### 8.3 GraphRAG's Position
- Better than RAG on multi-hop (graph structure helps)
- Worse than CKG (dynamic extraction introduces noise)
- Most expensive (build + query cost)
- Best use case: unstructured corpora with no available expert taxonomy

### 8.4 The Structure Premium
Report correlation between RDS advantage and DAG richness.
If r > 0.7: strong theoretical validation of CKG thesis.

### 8.5 Limitations
- McCreary corpus is educational — may not generalize to legal/financial domains
- CKG requires upfront expert curation investment
- Ground truth from DAG may not capture all valid answers

---

## 9. Conclusion

- RDS + hop-depth F1 are practical additions to IR evaluation
- CKG outperforms RAG and GraphRAG on structured domain retrieval
- Pre-structured knowledge beats dynamically extracted graphs when domain is stable
- McCreary corpus is a reproducible, citable multi-domain benchmark
- Open benchmark released — community can add domains and systems

---

## References (key)

- Lewis et al. (2020) RAG
- Edge et al. (2024) GraphRAG (Microsoft)
- Thakur et al. (2021) BEIR
- Es et al. (2023) RAGAS
- Pan et al. (2024) LLMs + KGs roadmap
- McCreary (2024) Intelligent Textbooks (GitHub + Medium)
- Karpukhin et al. (2020) DPR
