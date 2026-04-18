---
title: RAG Workflow
description: Build-time and query-time pipeline for Retrieval-Augmented Generation. Chunks markdown text, embeds each chunk, and retrieves the top-five most similar chunks per query, yielding roughly 2,400 tokens of context.
image: /sims/workflow-rag/workflow-rag.png
og:image: /sims/workflow-rag/workflow-rag.png
---

# RAG Workflow

Retrieval-Augmented Generation retrieves text chunks by vector similarity and
hands them to the LLM. Knowledge structure, if any, is inferred by the LLM from
prose.

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Helvetica, Arial, sans-serif','fontSize':'14px','primaryColor':'#E8EEF7','primaryBorderColor':'#3F51B5','primaryTextColor':'#1A237E','lineColor':'#3F51B5','clusterBkg':'#FAFAFE','clusterBorder':'#C5CAE9'}}}%%
flowchart TB
  classDef input fill:#E3F2FD,stroke:#1565C0,stroke-width:1.5px,color:#0D47A1
  classDef process fill:#E8EAF6,stroke:#3949AB,stroke-width:1.5px,color:#1A237E
  classDef store fill:#FFF8E1,stroke:#F9A825,stroke-width:1.5px,color:#E65100
  classDef output fill:#E8F5E9,stroke:#2E7D32,stroke-width:1.5px,color:#1B5E20

  subgraph Index[Build&nbsp;time]
    direction LR
    Text["Domain text<br/>(Markdown chapters)"]:::input --> Chunk["Split into<br/>512-token chunks"]:::process
    Chunk --> Embed["Embed each chunk<br/>(all-MiniLM-L6-v2)"]:::process
    Embed --> FAISS[("FAISS<br/>vector index")]:::store
  end

  subgraph Query[Query&nbsp;time]
    direction LR
    Q(["User query"]):::input --> QE["Embed query"]:::process
    QE --> Retrieve["Top-5 similarity<br/>retrieval"]:::process
    Retrieve --> Ctx["≈ 2,400 tokens<br/>of retrieved context"]:::process
    Ctx --> LLM["LLM<br/>(Claude)"]:::process
    LLM --> Ans(["Answer"]):::output
  end

  FAISS -.-> Retrieve
```

**Typical retrieved context:** ~2,400 tokens (five 512-token chunks with
overlap). **Build cost:** embed every chunk of every document. **Strength:**
works on any unstructured corpus. **Weakness:** structural questions (paths,
prerequisites, taxonomies) require the LLM to infer structure from prose.
