# Related Work

## Retrieval-Augmented Generation

Lewis et al. (2020) introduced RAG as a method for grounding language model outputs in retrieved passages. Dense Passage Retrieval (DPR) by Karpukhin et al. (2020) established embedding-based retrieval as the dominant paradigm. The BEIR benchmark (Thakur et al., 2021) provided heterogeneous evaluation across IR tasks, and RAGAS (Es et al., 2023) introduced evaluation metrics for RAG pipelines including faithfulness and relevance.

## Graph-Based Retrieval

Edge et al. (2024) introduced GraphRAG, using LLM-extracted entity graphs with community detection for multi-hop reasoning. LightRAG (Guo et al., 2024) and HippoRAG proposed lighter-weight graph-based alternatives. The key distinction for this benchmark: these systems perform **dynamic extraction** from text, while CKG uses **pre-structured domain knowledge**.

## Knowledge Graphs for LLMs

Pan et al. (2024) provide a comprehensive roadmap for unifying LLMs and knowledge graphs. The KGQA literature demonstrates structured query answering over knowledge graphs such as Wikidata and UMLS. CKG differs from these approaches by using lightweight DAG representations rather than full ontologies, trading expressiveness for efficiency.

## Evaluation Gaps in IR

Standard IR metrics (F1, MRR, NDCG) do not account for token cost. RAGAS measures faithfulness and relevance but not efficiency. This paper introduces **Reasoning Density Score (RDS)** and validates it on a multi-domain corpus---the first metric to jointly optimize quality and token consumption.

## Educational Knowledge Graphs

McCreary (2024) introduced the Intelligent Textbooks methodology, using learning graph DAGs as structured domain knowledge with a standardized CSV schema:

```
ConceptID | ConceptLabel | Dependencies | TaxonomyID
```

This work is the first to formalize this corpus as a citable benchmark dataset.
