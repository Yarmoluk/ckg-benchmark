## META
name: Compact Knowledge Graphs
version: 1.0.0
domain: knowledge-representation
description: A CKG about CKGs — what they are, how they work, why traversal beats retrieval
nodes: 43
edges: 62
source: Yarmoluk & McCreary (2025), arXiv; FDA/CLARITY-AD clinical validation
license: MIT
tags: [self-referential, meta, agent-memory, knowledge-representation, rag-alternative]

---

## NODES

[CONCEPT|ckg|Compact Knowledge Graph
  |Plain-text .md file encoding domain entities as typed nodes and named relationship edges. LLM-ready by construction. Zero hallucination by design.]

[CONCEPT|rag|Retrieval-Augmented Generation
  |Similarity search over vector embeddings. Retrieves nearest-text chunks. Fails on multi-hop dependency chains where the answer lives in the relationship, not the document.]

[CONCEPT|graph_rag|GraphRAG
  |Microsoft's graph-enhanced RAG. Extracts entity graphs from documents at query time. Better than RAG; slower and more expensive than pre-built CKG.]

[CONCEPT|typed_node|Typed Node
  |CKG entity with explicit category: [TYPE|id|label|description]. TYPE tells the AI what kind of thing it is before reading the value. Enables category-level traversal.]

[CONCEPT|named_edge|Named Relationship Edge
  |Explicit directed relationship: source -[EDGE_TYPE]-> target. Every relationship has a name. AI traverses — never infers. Makes wrong answers structurally unreachable.]

[CONCEPT|traversal|Graph Traversal
  |Following named edges hop by hop. Drug → REQUIRES → Criterion → TRIGGERS → Rule → APPROVED_WHEN → Outcome. The answer emerges from the path, not from text similarity.]

[CONCEPT|retrieval|Vector Retrieval
  |Embedding similarity search. Returns chunks ranked by cosine distance. Cannot navigate a dependency chain. Returns what is similar to the query, not what is downstream of it.]

[CONCEPT|multi_hop|Multi-Hop Reasoning
  |Query whose answer requires traversing 2+ edges. RAG fails here: the answer does not live in any single document. CKG succeeds: the answer is the path.]

[CONCEPT|hallucination|Hallucination
  |Model generating plausible-sounding but incorrect output. In RAG: occurs when retrieved chunks are incomplete or contradictory. In CKG: structurally prevented — wrong nodes don't exist.]

[CONCEPT|zero_hallucination|Zero Hallucination by Construction
  |CKG property: if a relationship is not encoded as an edge, the AI cannot assert it. Wrong answers require wrong edges. Errors are authoring errors, not inference errors.]

[CONCEPT|token_reduction|Token Reduction
  |CKG benchmark result: 269 mean tokens vs 2,982 for RAG. 11× reduction. Smaller context = faster inference, lower cost, higher accuracy on structural queries.]

[CONCEPT|rds|Retrieval Density Score (RDS)
  |CKG quality metric: F1 per token. Measures information per unit of context. CKG RDS: 0.001751. RAG RDS: 0.0000413. 42× advantage. Source: Yarmoluk & McCreary arXiv.]

[CONCEPT|f1_accuracy|F1 Accuracy
  |Benchmark result: CKG Macro F1 = 0.4709. RAG Macro F1 = 0.1231. 3.8× improvement on structural queries across 45 domains. Source: ckg-benchmark v0.6.2.]

[CONCEPT|ckg_format|CKG File Format
  |Plain text .md file. Two sections: ## NODES (typed entities) and ## EDGES (named relationships). No database. No embedding. Paste into any LLM context directly.]

[CONCEPT|node_syntax|Node Syntax
  |[TYPE|id|label|description]. TYPE: all-caps category. id: snake_case identifier. label: human-readable name. description: 1-2 sentences of grounding facts.]

[CONCEPT|edge_syntax|Edge Syntax
  |source_id -[EDGE_TYPE]-> target_id. Edge types in SCREAMING_SNAKE_CASE. Direction matters: A -[REQUIRES]-> B ≠ B -[REQUIRES]-> A.]

[CONCEPT|domain_ckg|Domain CKG
  |CKG encoding an enterprise knowledge domain: clinical guidelines, compliance rules, drug interactions, network topology, prior auth logic. The payload that makes agents accurate.]

[CONCEPT|self_referential_ckg|Self-Referential CKG
  |A CKG that encodes the CKG format itself. The best demo artifact: ask it how CKG traversal works and it answers by traversing itself.]

[CONCEPT|pre_action_grounding|Pre-Action Grounding
  |Agent pattern: query the CKG before generating a response. Structure is established first; generation is constrained by the traversal result. Eliminates hallucination by making the knowledge layer the first call, not the last.]

[CONCEPT|ckg_mcp|ckg-mcp
  |MCP server: pip install ckg-mcp. Exposes CKG domains as tools to Claude Desktop, Cursor, LangGraph, AutoGen. The delivery mechanism for the domain library.]

[CONCEPT|mcp_protocol|Model Context Protocol (MCP)
  |Anthropic's open protocol for structured context delivery to LLMs. CKG-MCP implements MCP to serve domain graphs as first-class agent tools.]

[CONCEPT|agent_gps|Agent GPS
  |Metaphor: CKG gives AI agents GPS navigation instead of dead reckoning. Exact coordinates (typed nodes), turn-by-turn instructions (named edges), known hazards (risk nodes), optimal routes (traversal paths).]

[CONCEPT|dead_reckoning|Dead Reckoning (RAG metaphor)
  |Navigation by estimation from last known position. Accumulates error with each step. RAG equivalent: retrieving chunks and inferring relationships — correct at first hop, increasingly wrong at hop 3+.]

[CONCEPT|gps_navigation|GPS Navigation (CKG metaphor)
  |Navigation with exact coordinates and named routes. No accumulated error. CKG equivalent: every node is a waypoint, every edge is a named road, every traversal is turn-by-turn.]

[CONCEPT|codebase_ckg|Codebase CKG
  |CKG encoding a software codebase: modules as nodes, dependencies as edges, security risks as typed risk nodes, API contracts as named relationships. Answers "how does auth work" with a traceable path.]

[CONCEPT|prior_auth_ckg|Prior Authorization CKG
  |Healthcare domain CKG: drugs, criteria, PA rules, outcomes as typed nodes. AI traverses eligibility chain: Drug → REQUIRES → Criterion → TRIGGERS → PA_Rule → APPROVED_WHEN → Outcome.]

[CONCEPT|drug_safety_ckg|Drug Safety CKG
  |Clinical domain CKG: lecanemab/Alzheimer's example. ApoE4 genotype → ELEVATES → ARIA Risk → CONTRAINDICATED_WITH → Anticoagulant → COMPOUNDS → ICH Risk → RECOMMENDS → DO_NOT_PRESCRIBE.]

[CONCEPT|compliance_ckg|Compliance CKG
  |Regulatory domain CKG: Basel III, DORA, GDPR rules as nodes. Regulation → MANDATES → Article → REQUIRES → Threshold → TRIGGERS → Reporting_Obligation. Full audit trail by construction.]

[CONCEPT|benchmark|CKG Benchmark
  |45 domains · 12,260 nodes · 19,405 edges · 7,928 queries. Compares CKG vs RAG vs GraphRAG. Public: github.com/Yarmoluk/ckg-benchmark · HuggingFace: danyarm/ckg-benchmark]

[CONCEPT|mcreary_corpus|McCreary Intelligent Textbook Corpus
  |46 educational knowledge domains by Dan McCreary (dmccreary). MIT licensed. Source material for CKG library conversion. 12,260 concepts, 19,405 edges.]

[CONCEPT|enterprise_domain|Enterprise Domain
  |A vertical knowledge area where AI hallucination causes measurable business harm: healthcare, compliance, supply chain, legal, insurance, cybersecurity. CKG's highest-value deployment context.]

[CONCEPT|source_citation|Source Citation
  |Every CKG node description grounds facts in a named source: FDA label, clinical trial, regulatory text, arXiv paper. Provenance is explicit. The AI cites the node, not a retrieved chunk.]

[CONCEPT|plain_text|Plain Text Portability
  |CKG is a .md file. Runs in Claude Desktop, Cursor, LangGraph, AutoGen, OpenAI API, any LLM with context. No vector database. No graph database. No infra.]

[CONCEPT|vendor_neutral|Vendor Neutral
  |CKG has no runtime dependency on any vendor. The format is open. The file travels with the enterprise. Contrast: RAG requires a vector DB; GraphRAG requires Neo4j or similar.]

[CONCEPT|update_cycle|Update Cycle
  |CKG update = edit the .md file. No re-embedding. No re-indexing. No DBA. No deployment cycle. A compliance rule changes: find the node, edit the description, done.]

[CONCEPT|oracle_migration|Oracle Knowledge Migration
  |Enterprise pattern: data migrated from Oracle to Postgres (solved). Knowledge encoded in PL/SQL procedures not migrated (unsolved). CKG is the open format for the knowledge layer.]

[CONCEPT|sovereign_ai|Sovereign AI
  |AI that runs on infrastructure you control, with knowledge you own, producing decisions you can audit. CKG enables sovereign knowledge — the layer above sovereign data infrastructure.]

[CONCEPT|ip_patent|Patent Pending
  |Provisional patent #64/040,804 filed April 16 2026. Provisional #2 filed May 2026 (App #64/054,755). Non-provisional deadline April 16 2027. Claims: compound KG environment, compression methodology.]

---

## EDGES

ckg                 -[IS_ALTERNATIVE_TO]->      rag
ckg                 -[OUTPERFORMS]->            rag
ckg                 -[OUTPERFORMS]->            graph_rag
ckg                 -[USES]->                   typed_node
ckg                 -[USES]->                   named_edge
ckg                 -[ENABLES]->                traversal
ckg                 -[PREVENTS]->               hallucination
ckg                 -[ACHIEVES]->               zero_hallucination
ckg                 -[ACHIEVES]->               token_reduction
ckg                 -[MEASURED_BY]->            rds
ckg                 -[MEASURED_BY]->            f1_accuracy
ckg                 -[SERIALIZED_AS]->          ckg_format
ckg                 -[DELIVERED_VIA]->          ckg_mcp
ckg                 -[METAPHOR_FOR]->           agent_gps
ckg                 -[SOLVES]->                 multi_hop
ckg                 -[ENABLES]->                sovereign_ai
ckg                 -[SOLVES]->                 oracle_migration
ckg                 -[PROTECTED_BY]->           ip_patent

rag                 -[USES]->                   retrieval
rag                 -[METAPHOR_FOR]->           dead_reckoning
rag                 -[FAILS_ON]->               multi_hop
rag                 -[CAUSES]->                 hallucination

graph_rag           -[IMPROVES_ON]->            rag
graph_rag           -[SLOWER_THAN]->            ckg
graph_rag           -[MORE_EXPENSIVE_THAN]->    ckg

traversal           -[CONTRASTS_WITH]->         retrieval
traversal           -[REQUIRES]->               named_edge
traversal           -[PRODUCES]->               zero_hallucination
traversal           -[METAPHOR_FOR]->           gps_navigation

retrieval           -[METAPHOR_FOR]->           dead_reckoning
retrieval           -[FAILS_ON]->               multi_hop

typed_node          -[USES_SYNTAX]->            node_syntax
named_edge          -[USES_SYNTAX]->            edge_syntax
named_edge          -[ENABLES]->                zero_hallucination

ckg_format          -[CONSISTS_OF]->            typed_node
ckg_format          -[CONSISTS_OF]->            named_edge
ckg_format          -[IS]->                     plain_text
ckg_format          -[IS]->                     vendor_neutral
ckg_format          -[ENABLES]->                update_cycle

ckg_mcp             -[IMPLEMENTS]->             mcp_protocol
ckg_mcp             -[SERVES]->                 domain_ckg
ckg_mcp             -[INSTALLS_VIA]->           plain_text

agent_gps           -[CONTRASTS_WITH]->         dead_reckoning
agent_gps           -[REQUIRES]->               ckg
agent_gps           -[ENABLES]->                codebase_ckg

self_referential_ckg -[IS_INSTANCE_OF]->        ckg
self_referential_ckg -[DEMONSTRATES]->          ckg_format
self_referential_ckg -[IS_BEST_DEMO_OF]->       agent_gps

pre_action_grounding -[REQUIRES]->              ckg
pre_action_grounding -[PREVENTS]->              hallucination
pre_action_grounding -[USES]->                  traversal
ckg                  -[ENABLES]->               pre_action_grounding

domain_ckg          -[EXAMPLE_IS]->             prior_auth_ckg
domain_ckg          -[EXAMPLE_IS]->             drug_safety_ckg
domain_ckg          -[EXAMPLE_IS]->             compliance_ckg
domain_ckg          -[EXAMPLE_IS]->             codebase_ckg
domain_ckg          -[SOURCE_FROM]->            mcreary_corpus

mcreary_corpus      -[SOURCE_FOR]->             benchmark
mcreary_corpus      -[LICENSED_AS]->            plain_text

source_citation     -[GROUNDS]->                typed_node
source_citation     -[PREVENTS]->               hallucination

token_reduction     -[QUANTIFIED_BY]->          rds
rds                 -[DERIVED_FROM]->           benchmark
f1_accuracy         -[DERIVED_FROM]->           benchmark

sovereign_ai        -[REQUIRES]->               vendor_neutral
sovereign_ai        -[REQUIRES]->               source_citation
oracle_migration    -[SOLVED_BY]->              ckg_format
