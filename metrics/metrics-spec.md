# Complete Metrics Specification

## 1. Standard IR Metrics

### 1.1 Token-Level F1 (SQuAD-style)
Used for T1 (entity), T2 (dependency), T4 (aggregate) queries.

```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2·P·R / (P + R)

TP = tokens in both prediction and ground truth
FP = tokens in prediction not in ground truth
FN = tokens in ground truth not in prediction
```

### 1.2 Edge-Overlap F1
Used for T3 (path) and T5 (cross-concept) queries.

```
Edge_F1 = 2 · |predicted_edges ∩ truth_edges| /
              (|predicted_edges| + |truth_edges|)
```

### 1.3 Exact Match (EM)
Binary — full answer must match ground truth exactly.
Reported alongside F1 as secondary metric.

---

## 2. Reasoning Density Score (RDS)
*Novel metric introduced in this paper.*

```
RDS(system, query) = F1(system, query) / tokens_consumed(system, query)

RDS_macro(system) = mean(RDS over all queries)

RDS_ratio(A vs B) = RDS_macro(A) / RDS_macro(B)
```

**Interpretation:** Higher = more reasoning quality per token spent.
**Units:** F1 per token (dimensionless ratio for comparisons)

---

## 3. Hop-Depth F1 Degradation
*Novel metric — measures how F1 degrades as reasoning chain length increases.*

### Definition
For each query, compute the minimum hop distance from query concept to answer concept(s) in the DAG.

```
hop_depth(query) = shortest_path_length(query_node, answer_node) in DAG

F1_at_hop(system, k) = mean F1 over all queries where hop_depth = k
```

### Expected Findings
- RAG: steep degradation at hop ≥ 2 (embeddings don't encode transitive relationships)
- GraphRAG: moderate degradation (dynamic extraction misses some edges)
- CKG: flat or minimal degradation (explicit edges, BFS traversal)

### Reporting
Plot: F1 vs hop depth (k=1,2,3,4,5+) for all 3 systems.
This is the key figure showing where CKG structurally wins.

---

## 4. Tokenomics Metrics

### 4.1 Context Utilization Rate (CUR)
*What fraction of retrieved tokens were actually relevant to the answer?*

```
CUR(system, query) = relevant_tokens_in_context / total_tokens_in_context

relevant_tokens = tokens from retrieved context that appear in ground truth answer
```

- RAG: low CUR (retrieves noisy chunks)
- GraphRAG: medium CUR (entity summaries have some noise)
- CKG: high CUR (retrieves exact subgraph, minimal noise)

### 4.2 Cost Per Correct Answer (CPCA)
*Real-world cost metric using current API pricing.*

```
CPCA(system, query) = tokens_consumed × $/token × (1 / F1)
                    = cost_per_query / F1

# Aggregate
CPCA_macro = mean(CPCA over all queries)
```

Report in USD at Claude Sonnet 4.6 pricing ($3/M input, $15/M output).
Makes the efficiency argument concrete and actionable.

### 4.3 Precision at Token Budget (P@T)
*What F1 can each system achieve within a fixed token budget?*

```
P@T(system, budget) = mean F1 over all queries where tokens_consumed ≤ budget
```

Report for budgets: T=500, T=1000, T=2000, T=5000, T=10000

Expected finding: CKG achieves near-peak F1 at T=500; RAG needs T=3000+ for equivalent quality.

### 4.4 Token Budget Breakeven
*At what token budget does RAG/GraphRAG catch up to CKG F1?*

```
breakeven(RAG vs CKG) = min budget where F1_RAG(budget) ≥ F1_CKG(500)
```

This produces a single number that summarizes the efficiency gap.

### 4.5 Index Build Cost
*One-time cost to prepare each system.*

```
build_cost(system) = tokens consumed during indexing/extraction phase
                   + wall-clock time
                   + storage bytes
```

- RAG: embedding all chunks
- GraphRAG: entity extraction + community detection (expensive)
- CKG: zero (CSV already exists in McCreary corpus)

**CKG advantage: $0 build cost for domains already in McCreary format.**

### 4.6 Update Cost
*Cost to incorporate one new concept or relationship.*

```
update_cost(system, delta) = tokens/time to reflect one change in the knowledge base
```

- RAG: re-embed affected chunks (~proportional to chunk count)
- GraphRAG: full re-extraction of affected community (~expensive)
- CKG: edit one CSV row, zero re-indexing

---

## 5. Structural Fidelity Metrics

### 5.1 Relationship Precision (RP)
*Of the edges the system returns, what fraction are real edges in the DAG?*

```
RP = |predicted_edges ∩ ground_truth_edges| / |predicted_edges|
```

GraphRAG's dynamic extraction invents edges not in the ground truth DAG.
CKG returns only real edges. This metric quantifies that gap.

### 5.2 Hub Node Recall (HNR)
*Are the most important concepts (highest indegree) reliably retrieved?*

```
hub_nodes = top-20% concepts by indegree in DAG
HNR(system) = recall over queries where answer is a hub node
```

Hypothesis: CKG > RAG on HNR because hubs are explicitly encoded.

### 5.3 Boundary Completeness (BC)
*For taxonomy category queries (T4), what fraction of the category is returned?*

```
BC(system, category) = |retrieved ∩ category_members| / |category_members|
```

CKG: trivial (filter by TaxonomyID), BC ≈ 1.0
RAG: depends on whether all members appeared in retrieved chunks
GraphRAG: depends on community detection alignment with taxonomy

---

## 6. Robustness Metrics

### 6.1 Paraphrase Stability (PS)
*Does F1 hold when the same question is asked 5 different ways?*

```
PS(system, concept) = 1 - std(F1 over 5 paraphrased queries)
                      ─────────────────────────────────────
                           mean(F1 over 5 paraphrased queries)

# Lower variance = higher stability
```

Generate paraphrases with temperature=1, evaluate at temperature=0.
CKG should be stable (exact concept match); RAG is embedding-sensitive.

### 6.2 Hallucination Rate (HR)
*How often does the system return concepts not in the ground truth DAG?*

```
HR(system) = queries where prediction contains ≥1 concept not in corpus
             ─────────────────────────────────────────────────────────
                              total queries
```

GraphRAG's entity extraction can hallucinate relationships.
CKG: HR = 0 by construction (only returns concepts in the CSV).

---

## 7. Summary Table

| Metric | Type | Novel | Favors |
|--------|------|-------|--------|
| Token F1 | Quality | No | Mixed |
| Edge F1 | Quality | No | CKG |
| Exact Match | Quality | No | CKG |
| RDS | Compound | **Yes** | CKG |
| F1 by Hop Depth | Quality×Structure | **Yes** | CKG |
| Context Utilization Rate | Efficiency | **Yes** | CKG |
| Cost Per Correct Answer | Cost | **Yes** | CKG |
| Precision@Token Budget | Cost×Quality | **Yes** | CKG |
| Token Budget Breakeven | Cost | **Yes** | CKG |
| Index Build Cost | Operational | No | CKG |
| Update Cost | Operational | **Yes** | CKG |
| Relationship Precision | Structural | **Yes** | CKG |
| Hub Node Recall | Structural | **Yes** | CKG |
| Boundary Completeness | Structural | **Yes** | CKG |
| Paraphrase Stability | Robustness | No | CKG |
| Hallucination Rate | Robustness | No | CKG |
