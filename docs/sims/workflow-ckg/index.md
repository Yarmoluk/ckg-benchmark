---
title: CKG Workflow
description: Build-time and query-time pipeline for Compact Knowledge Graph retrieval. Parses a pre-authored DAG directly and extracts the relevant subgraph by BFS or DFS traversal, yielding roughly 150 to 400 tokens of context per query.
image: /sims/workflow-ckg/workflow-ckg.png
og:image: /sims/workflow-ckg/workflow-ckg.png
---

# CKG Workflow

Compact Knowledge Graph retrieval reads a pre-authored DAG directly and
extracts the subgraph relevant to each query by BFS/DFS traversal. No
embedding model, no dynamic extraction, no inference of structure from prose.

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Helvetica, Arial, sans-serif','fontSize':'14px','primaryColor':'#FCE4EC','primaryBorderColor':'#AD1457','primaryTextColor':'#880E4F','lineColor':'#AD1457','clusterBkg':'#FFF8F9','clusterBorder':'#F8BBD0'}}}%%
flowchart TB
  classDef input fill:#FCE4EC,stroke:#AD1457,stroke-width:1.5px,color:#880E4F
  classDef process fill:#F3E5F5,stroke:#6A1B9A,stroke-width:1.5px,color:#4A148C
  classDef store fill:#FFF3E0,stroke:#E65100,stroke-width:1.5px,color:#BF360C
  classDef output fill:#E3F2FD,stroke:#1565C0,stroke-width:1.5px,color:#0D47A1

  subgraph Index[Build&nbsp;time]
    direction LR
    Desc["Course description<br/>(audience, prereqs,<br/>objectives)"]:::input --> LGG["/learning-graph-generator<br/>skill + SME review"]:::process
    LGG --> CSV["learning-graph.csv<br/>G = (C, E, T, τ)"]:::input
    CSV --> Load["Parse DAG<br/>(zero compute)"]:::process
    Load --> DAG[("In-memory<br/>DAG")]:::store
  end

  subgraph Query[Query&nbsp;time]
    direction LR
    Q(["User query"]):::input --> Classify["Classify as<br/>T1–T5"]:::process
    Classify --> Traverse["BFS/DFS subgraph<br/>extraction"]:::process
    Traverse --> Ctx["≈ 150–400 tokens<br/>of retrieved context"]:::process
    Ctx --> LLM["LLM<br/>(Claude)"]:::process
    LLM --> Ans(["Answer"]):::output
  end

  DAG -.-> Traverse
```

**Typical retrieved context:** ~150–400 tokens. **Build cost:** zero at inference
time — the DAG is authored once (see the Agent Skill workflow in
[Learning Graph Economics](../../paper/learning-graph-economics.md)).
**Strength:** deterministic traversal, closed vocabulary, hallucination rate
zero by construction on structural queries. **Weakness:** only works in
domains with a stable authored DAG and when queries map cleanly to traversal
operations.
