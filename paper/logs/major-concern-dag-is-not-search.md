# MAJOR CONCERN: A Learning Dependency DAG Is Not a Search System

**Date:** 2026-04-14
**Severity:** High — could undermine the paper's core claims if not addressed
**Status:** Open — requires author response before proceeding

## The Problem

The learning graph DAG encodes **pedagogical ordering**: "Concept X should be learned after concepts Y and Z." This is a curriculum sequencing tool, not a knowledge retrieval system.

The paper claims CKG outperforms RAG and GraphRAG on "knowledge retrieval." But the DAG cannot answer the most basic knowledge question: **"What is X?"** It can only answer structural questions about the relationships between concepts:

- "What are the prerequisites for X?" → read the Dependencies column
- "What is the path from A to B?" → BFS over the DAG
- "List all CORE concepts" → filter by TaxonomyID

These are legitimate queries, but they are a **narrow, self-referential subset** of what users actually need from a knowledge system. The benchmark is testing whether a system can retrieve information that is explicitly stored in the DAG — which the DAG trivially wins because it *is* the ground truth.

## What the DAG Can Answer

| Query Type | Example | DAG Answer |
|------------|---------|------------|
| T2: Prerequisites | "What should I learn before Implicit Differentiation?" | Concepts 12, 15, 3 |
| T3: Learning path | "What is the chain from Function to Taylor Series?" | [Function, Limit, Derivative, ...] |
| T4: Category listing | "List all foundational concepts" | Filter TaxonomyID = FOUND |

## What the DAG Cannot Answer

| Query Type | Example | DAG Answer |
|------------|---------|------------|
| Explanation | "What is Implicit Differentiation?" | ❌ No explanatory content |
| How-to | "How do I perform Implicit Differentiation?" | ❌ No procedural knowledge |
| Why | "Why is the Chain Rule needed for Implicit Differentiation?" | ❌ No causal reasoning |
| Comparison | "How does Implicit Differentiation differ from Explicit?" | ❌ No descriptive content |
| Application | "When would I use Implicit Differentiation?" | ❌ No contextual knowledge |

## The Tautology Risk

The benchmark generates ground truth **from the DAG itself** (T2 ground truth = the Dependencies column, T3 ground truth = BFS paths, T4 ground truth = TaxonomyID filters). Then it tests whether CKG (which reads the DAG directly) outperforms RAG and GraphRAG (which must infer this structure from text).

This is close to tautological: "A system that directly reads a data structure retrieves that data structure's contents more accurately than systems that must infer it from prose."

A reviewer could argue this is not a fair comparison — it's like testing whether a SQL query outperforms full-text search on a database that was designed for SQL.

## The Real Question the Paper Should Answer

The interesting research question is not "Can a DAG beat RAG at retrieving DAG edges?" (obviously yes). The interesting questions are:

1. **For what fraction of real educational queries is structural knowledge sufficient?** If an AI tutor mostly needs prerequisite chains and concept ordering, then the DAG covers most use cases at 13x lower cost. If users mostly ask "explain this to me," the DAG is useless alone.

2. **Can structural context improve explanatory retrieval?** A hybrid approach — use the DAG to identify which concepts are relevant, then retrieve targeted text only for those concepts — could combine CKG's precision with RAG's richness. This would be a genuinely novel contribution.

3. **Is the pedagogical structure itself a form of knowledge that existing systems fail to capture?** RAG discards document structure during chunking. GraphRAG re-derives it imperfectly. The DAG preserves it exactly. This is a real insight, but it needs to be framed as "structural knowledge retrieval" not "general knowledge retrieval."

## Possible Remedies

### Option A: Narrow the Claims
Reframe the paper as a benchmark for **structural/relational knowledge retrieval in educational domains**. Acknowledge that CKG does not compete with RAG for explanatory queries. This is honest and still publishable — the structural query types (T2, T3, T4) are real use cases in tutoring systems, curriculum planners, and adaptive learning platforms.

### Option B: Add Explanatory Queries
Add a T6 query type: "Explain {concept} in the context of its prerequisites." Use the DAG to select relevant concepts, then retrieve targeted text for those concepts. This tests a hybrid CKG+RAG approach and makes the comparison more interesting.

### Option C: Reframe as Efficiency Study
The core insight may not be "CKG is better" but "for queries that have structural answers, using the structure directly is 13x cheaper than inferring it from text." This is a valid efficiency result that doesn't require CKG to be a general-purpose replacement for RAG.

## Impact on Paper

If this concern is not addressed, reviewers will likely raise it as:

- "The benchmark tests retrieval of information that is tautologically present in the CKG system's data source"
- "The comparison is unfair because CKG has direct access to the ground truth"
- "The paper does not demonstrate that CKG is useful for the majority of real-world knowledge queries"

These are survivable objections if the paper is framed correctly (Option A or C), but fatal if the paper continues to claim CKG is a general replacement for RAG.
