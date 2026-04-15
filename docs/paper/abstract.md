# Abstract

Retrieval-augmented generation (RAG) and graph-based retrieval (GraphRAG) are the dominant paradigms for grounding LLM responses in structured knowledge. Both optimize for retrieval recall while treating token cost as a secondary concern. We introduce **Compressed Knowledge Graphs (CKG)**---pre-structured DAG representations with explicit concept taxonomy and pipe-delimited dependency encoding---and present the first large-scale benchmark comparing all three architectures across 46 domains.

We evaluate on the **McCreary Intelligent Textbook Corpus**: 46 open-source educational domains (calculus, chemistry, computer science, genetics, bioinformatics, economics, machine learning, and more), each with a standardized learning graph CSV totaling 12,260 concepts and 19,405 dependency edges. We introduce five novel metrics: **Reasoning Density Score** (RDS = F1 / tokens), **Context Utilization Rate**, **Hop-Depth F1 Degradation**, **Cost Per Correct Answer**, and **Relationship Precision**.

!!! warning "Results Pending"
    Experimental results will be added after benchmark runs are complete.

Benchmark, dataset, and evaluation harness are released at [HuggingFace](https://huggingface.co/datasets/graphify-md/ckg-benchmark) under CC BY 4.0 / MIT.

**ArXiv categories:** cs.IR (primary), cs.AI (secondary)
