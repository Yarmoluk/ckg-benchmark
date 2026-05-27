## META
name: Conversational AI
version: 1.0.0
domain: conversational-ai
description: The architecture, components, and evaluation of AI systems that conduct multi-turn natural language dialogue with users.
nodes: 52
edges: 75
source: McCreary Intelligent Textbook Corpus (MIT)
license: MIT

---

## NODES

[CONCEPT|natural_language_processing|Natural Language Processing
  |Field of AI concerned with enabling machines to understand, interpret, and generate human language. The foundational discipline underlying every conversational AI component from intent parsing to response generation.]

[CONCEPT|large_language_model|Large Language Model
  |Neural network trained on massive text corpora that generates coherent, contextually appropriate language. The engine inside modern conversational agents, replacing the rule-based NLU/NLG pipelines of earlier chatbots.]

[CONCEPT|transformer_architecture|Transformer Architecture
  |Self-attention neural architecture enabling LLMs to model relationships between tokens across long sequences. Its positional encoding and multi-head attention are what allow coherent multi-turn conversation.]

[CONCEPT|attention_mechanism|Attention Mechanism
  |Component of Transformers that computes weighted relevance scores between all token pairs. Allows the model to "look back" at earlier conversation turns when generating each new token.]

[CONCEPT|token|Token
  |Sub-word unit processed by an LLM. Understanding tokens explains why context windows are measured in tokens, not words, and why conversation history has hard capacity limits.]

[CONCEPT|tokenization|Tokenization
  |Conversion of raw text into token sequences using a learned vocabulary (e.g., BPE). Non-English languages and special characters often tokenize inefficiently, affecting response latency.]

[CONCEPT|word_embedding|Word Embedding
  |Dense vector representation of a token capturing its semantic relationships to other tokens. The geometric structure of embedding space enables similarity-based search and clustering of intents.]

[CONCEPT|embedding_vector|Embedding Vector
  |Specific numerical representation of a piece of text in a high-dimensional vector space. Similar meanings cluster nearby; distance metrics (cosine, dot product) enable retrieval.]

[CONCEPT|vector_space_model|Vector Space Model
  |Mathematical framework representing text as vectors in a high-dimensional space where proximity encodes semantic similarity. Foundation of modern embedding-based search and retrieval.]

[CONCEPT|vector_database|Vector Database
  |Specialized store for embedding vectors with fast approximate nearest-neighbor search. Enables sub-100ms semantic retrieval across millions of documents in production conversational systems.]

[CONCEPT|approximate_nearest_neighbor|Approximate Nearest Neighbor
  |Algorithm that finds semantically close vectors quickly by sacrificing exhaustive search for speed. Makes real-time embedding retrieval practical at scale; FAISS is the dominant open-source implementation.]

[CONCEPT|faiss|FAISS
  |Facebook AI Similarity Search — open-source library for efficient similarity search over dense vector collections. Used in RAG pipelines to retrieve relevant documents before response generation.]

[CONCEPT|chatbot|Chatbot
  |Software system that conducts natural language conversations with users, ranging from rule-based scripts to LLM-powered agents. The deployment artifact that end users actually interact with.]

[CONCEPT|conversational_agent|Conversational Agent
  |LLM-powered system capable of multi-turn dialogue with memory, tool access, and goal-directed planning. Distinguished from simple chatbots by its ability to handle ambiguity and pursue objectives across turns.]

[CONCEPT|dialog_system|Dialog System
  |Formal architecture for managing the structure of a conversation: intent classification, state tracking, policy selection, and response generation. Modern LLMs subsume most classical dialog system components.]

[CONCEPT|intent_recognition|Intent Recognition
  |Classification of user input into a predefined action or goal category (e.g., "book_flight", "check_balance"). Determines what the system should do next. In LLM systems, often replaced by free-form instruction following.]

[CONCEPT|intent_modeling|Intent Modeling
  |Building and maintaining the taxonomy of intents the system can handle, including edge cases and conflicting signals. Poor intent coverage is the most common failure mode in production chatbot deployments.]

[CONCEPT|entity_extraction|Entity Extraction
  |Identifying and pulling out key pieces of information from user input (dates, names, amounts, locations). Feeds downstream reasoning and database lookups; accuracy here gates accuracy everywhere else.]

[CONCEPT|named_entity_recognition|Named Entity Recognition
  |Specific NLP task of labeling sequences of tokens as person, organization, location, date, etc. A prerequisite for structured data extraction from conversational user inputs.]

[CONCEPT|user_query|User Query
  |The text input submitted by a user in a conversational turn. The primary signal the system must interpret — ambiguous, often incomplete, and shaped by what the user assumes the system knows.]

[CONCEPT|chatbot_response|Chatbot Response
  |The system's reply to a user query. Quality is judged on accuracy, coherence, helpfulness, tone, and latency. Every component of the pipeline ultimately affects response quality.]

[CONCEPT|response_generation|Response Generation
  |The process of producing a natural language reply given the interpreted query, retrieved context, and conversation history. In LLM systems, this is the model's forward pass given a constructed prompt.]

[CONCEPT|response_quality|Response Quality
  |Composite metric covering accuracy, relevance, coherence, and user satisfaction. The target variable the entire conversational AI stack is optimized toward.]

[CONCEPT|response_latency|Response Latency
  |Time elapsed between user query submission and system response delivery. Affects perceived conversational naturalness. Driven by model size, retrieval time, and infrastructure.]

[CONCEPT|user_feedback|User Feedback
  |Explicit signals (thumbs up/down, ratings, corrections) or implicit signals (re-queries, abandonment) indicating whether a response met the user's need. Primary training signal for system improvement.]

[CONCEPT|feedback_loop|Feedback Loop
  |Mechanism that routes user feedback back into system improvement — reranking, fine-tuning, or prompt adjustment. Without a feedback loop, deployed chatbots degrade relative to shifting user needs.]

[CONCEPT|ai_flywheel|AI Flywheel
  |Virtuous cycle where more users generate more feedback, which improves the model, which attracts more users. Conversational AI products with strong flywheels compound advantages over time.]

[CONCEPT|conversation_context|Conversation Context
  |Accumulated information from prior turns in a session: user statements, system responses, extracted entities, and inferred goals. The richer the context, the more coherent the system's next response.]

[CONCEPT|chat_history|Chat History
  |Stored record of prior messages in a session. Injected into the LLM context window to enable multi-turn coherence. Subject to context window limits; must be managed, summarized, or pruned for long sessions.]

[CONCEPT|session_management|Session Management
  |Logic governing the lifecycle of a conversation: session initialization, context persistence, timeout handling, and state reset. Poor session management causes context bleed between unrelated conversations.]

[CONCEPT|chatbot_framework|Chatbot Framework
  |Software library providing scaffolding for building conversational agents: prompt management, memory, tool routing, and LLM API abstraction. Reduces time-to-deployment from months to days.]

[CONCEPT|langchain|LangChain
  |Open-source Python and JavaScript framework for building LLM-powered applications including conversational agents. Provides chains, agents, memory, and tool-use abstractions built on any LLM backend.]

[CONCEPT|llamaindex|LlamaIndex
  |Data framework for connecting LLMs to external data sources. Particularly strong for RAG over structured and unstructured enterprise data — complements LangChain's agent orchestration focus.]

[CONCEPT|rag_pattern|RAG Pattern
  |Retrieve-then-Generate architecture: fetch relevant documents from an external store, inject them into the LLM context, and generate a grounded response. Standard pattern for knowledge-intensive conversational tasks.]

[CONCEPT|retrieval_augmented_generation|Retrieval-Augmented Generation
  |Instantiation of the RAG pattern with a specific retriever (e.g., vector database) and a specific generator (LLM). Grounds responses in external knowledge, reducing hallucination on factual queries.]

[CONCEPT|context_window|Context Window
  |Maximum token capacity an LLM can process in a single inference call. In conversational AI, the context window must accommodate system prompt, chat history, retrieved documents, and response generation headroom simultaneously.]

[CONCEPT|hallucination|Hallucination
  |Model-generated content that is factually incorrect but presented confidently. The primary reliability risk in LLM-based conversational AI; mitigated by retrieval grounding, constraint prompting, and output validation.]

[CONCEPT|graphrag_pattern|GraphRAG Pattern
  |RAG variant that retrieves from a knowledge graph rather than a flat vector index. Enables multi-hop reasoning over structured relationships — effective when answers span multiple interconnected entities.]

[CONCEPT|knowledge_graph|Knowledge Graph
  |Structured representation of entities and their named relationships as nodes and edges. Enables precise, traversal-based retrieval that flat vector search cannot replicate for relational queries.]

[CONCEPT|graph_database|Graph Database
  |Storage system optimized for traversing graph structures. Supports queries like "find all drugs that treat a disease whose gene is expressed in a specific tissue." Neo4j is the dominant open-source option.]

[CONCEPT|nlp_pipeline|NLP Pipeline
  |Sequential processing chain: tokenization → POS tagging → dependency parsing → NER → intent recognition. Each stage outputs structured data consumed by the next. LLMs compress or bypass many pipeline stages.]

[CONCEPT|natural_language_to_sql|Natural Language to SQL
  |Translating a user's plain-language query into a SQL statement for database execution. Enables non-technical users to query structured enterprise data through conversational interfaces.]

[CONCEPT|personalization|Personalization
  |Tailoring system responses to individual user preferences, history, and profile data. Increases engagement and task completion rates but raises data governance and privacy requirements.]

[CONCEPT|user_profile|User Profile
  |Persistent representation of a user's attributes, preferences, and history. The data store enabling personalization across sessions. Must be updated, protected, and sometimes forgotten on request.]

[CONCEPT|data_privacy|Data Privacy
  |Policies and technical controls ensuring user data is collected, stored, and used in compliance with user consent and regulatory requirements. Conversational AI systems inherently collect sensitive data.]

[CONCEPT|gdpr|GDPR
  |EU General Data Protection Regulation. Mandates data minimization, user consent, right to erasure, and breach notification. Applies to any conversational AI serving EU users, regardless of company location.]

[CONCEPT|authentication|Authentication
  |Verification that a user is who they claim to be before granting access to personalized data or privileged actions. A prerequisite for any conversational AI handling sensitive accounts or transactions.]

[CONCEPT|chatbot_metrics|Chatbot Metrics
  |Quantitative measures of system performance: containment rate, escalation rate, task completion rate, CSAT, and response latency. Required for evidence-based iteration and stakeholder reporting.]

[CONCEPT|user_satisfaction|User Satisfaction
  |Aggregate measure of how well the conversational experience met user expectations and needs. The most important long-run metric — all technical metrics are proxies for it.]

[CONCEPT|response_accuracy|Response Accuracy
  |Proportion of system responses that are factually correct and task-relevant. Distinct from user satisfaction — accurate but unhelpful responses score low on both.]

[CONCEPT|chatbot_evaluation|Chatbot Evaluation
  |Systematic process of measuring system performance across multiple dimensions using held-out test cases, human raters, or automated metrics. Precedes any production deployment or major system change.]

[CONCEPT|ab_testing|A/B Testing
  |Controlled experiment comparing two system variants (prompts, models, UI changes) on live traffic to measure which produces better outcomes. The gold standard for validating conversational AI improvements.]

---

## EDGES

natural_language_processing  -[PREREQUISITE_FOR]->    intent_recognition
natural_language_processing  -[PREREQUISITE_FOR]->    entity_extraction
natural_language_processing  -[PREREQUISITE_FOR]->    natural_language_to_sql
natural_language_processing  -[COMPONENT_OF]->        nlp_pipeline
large_language_model         -[BUILT_ON]->            transformer_architecture
large_language_model         -[IMPROVES_ON]->         dialog_system
large_language_model         -[ENABLES]->             response_generation
large_language_model         -[CONSTRAINS]->          context_window
transformer_architecture     -[COMPONENT_OF]->        attention_mechanism
attention_mechanism          -[ENABLES]->             conversation_context
token                        -[DEFINED_BY]->          tokenization
token                        -[COMPONENT_OF]->        context_window
word_embedding               -[PRODUCES]->            embedding_vector
word_embedding               -[BUILT_ON]->            vector_space_model
embedding_vector             -[STORED_IN]->           vector_database
vector_space_model           -[PREREQUISITE_FOR]->    approximate_nearest_neighbor
vector_database              -[IMPLEMENTS]->          approximate_nearest_neighbor
vector_database              -[ENABLES]->             retrieval_augmented_generation
approximate_nearest_neighbor -[USED_BY]->             faiss
faiss                        -[COMPONENT_OF]->        rag_pattern
chatbot                      -[INSTANCE_OF]->         conversational_agent
chatbot                      -[PRODUCES]->            chatbot_response
chatbot                      -[GENERATES]->           user_feedback
chatbot                      -[REQUIRES]->            authentication
conversational_agent         -[BUILT_ON]->            large_language_model
conversational_agent         -[REQUIRES]->            dialog_system
conversational_agent         -[USES]->                chatbot_framework
dialog_system                -[REQUIRES]->            intent_recognition
dialog_system                -[REQUIRES]->            session_management
intent_recognition           -[REQUIRES]->            entity_extraction
intent_recognition           -[BUILDS_ON]->           intent_modeling
entity_extraction            -[IMPLEMENTED_BY]->      named_entity_recognition
user_query                   -[TRIGGERS]->            intent_recognition
user_query                   -[TRIGGERS]->            entity_extraction
chatbot_response             -[PRODUCED_BY]->         response_generation
chatbot_response             -[MEASURED_BY]->         response_quality
chatbot_response             -[MEASURED_BY]->         response_latency
response_generation          -[REQUIRES]->            conversation_context
response_generation          -[USES]->                rag_pattern
response_quality             -[MEASURED_BY]->         response_accuracy
response_quality             -[CONTRIBUTES_TO]->      user_satisfaction
response_latency             -[AFFECTS]->             user_satisfaction
user_feedback                -[FEEDS]->               feedback_loop
feedback_loop                -[ENABLES]->             ai_flywheel
feedback_loop                -[IMPROVES]->            response_quality
ai_flywheel                  -[REQUIRES]->            feedback_loop
conversation_context         -[STORED_IN]->           chat_history
chat_history                 -[CONSTRAINED_BY]->      context_window
session_management           -[MANAGES]->             chat_history
chatbot_framework            -[IMPLEMENTS]->          session_management
langchain                    -[INSTANCE_OF]->         chatbot_framework
langchain                    -[INTEGRATES]->          rag_pattern
llamaindex                   -[INSTANCE_OF]->         chatbot_framework
llamaindex                   -[OPTIMIZED_FOR]->       retrieval_augmented_generation
rag_pattern                  -[PREREQUISITE_FOR]->    retrieval_augmented_generation
retrieval_augmented_generation -[MITIGATES]->         hallucination
retrieval_augmented_generation -[USES]->              vector_database
hallucination                -[THREATENS]->           response_accuracy
graphrag_pattern             -[EXTENDS]->             rag_pattern
graphrag_pattern             -[REQUIRES]->            knowledge_graph
knowledge_graph              -[STORED_IN]->           graph_database
graph_database               -[ENABLES]->             graphrag_pattern
nlp_pipeline                 -[PRODUCES]->            intent_recognition
natural_language_to_sql      -[REQUIRES]->            entity_extraction
personalization              -[REQUIRES]->            user_profile
personalization              -[IMPROVES]->            user_satisfaction
user_profile                 -[SUBJECT_TO]->          data_privacy
data_privacy                 -[GOVERNED_BY]->         gdpr
authentication               -[PREREQUISITE_FOR]->    personalization
chatbot_metrics              -[INCLUDES]->            user_satisfaction
chatbot_metrics              -[INCLUDES]->            response_accuracy
chatbot_metrics              -[INCLUDES]->            response_latency
chatbot_evaluation           -[USES]->                chatbot_metrics
chatbot_evaluation           -[REQUIRES]->            ab_testing
ab_testing                   -[VALIDATES]->           response_quality
