# Metrics

We evaluate 16 metrics organized into six categories. Novel metrics introduced in this paper are marked with a star ($\star$).

## Standard IR Metrics

### Token-Level F1 (SQuAD-style)

Used for T1, T2, and T4 queries:

$$\text{F1} = \frac{2 \cdot P \cdot R}{P + R}, \quad P = \frac{|pred \cap truth|}{|pred|}, \quad R = \frac{|pred \cap truth|}{|truth|}$$

### Edge-Overlap F1

Used for T3 (path) and T5 (cross-concept) queries:

$$\text{Edge\_F1} = \frac{2 \cdot |E_{pred} \cap E_{truth}|}{|E_{pred}| + |E_{truth}|}$$

### Exact Match (EM)

Binary---the full answer must match ground truth exactly.

## Reasoning Density Score $\star$ (RDS)

The core compound metric introduced in this paper:

$$\text{RDS}(s, q) = \frac{\text{F1}(s, q)}{\text{tokens\_consumed}(s, q)}$$

- **Macro-averaged:** $\text{RDS}_{\text{macro}}(s) = \text{mean}(\text{RDS over all queries})$
- **RDS ratio:** $\text{RDS}_{\text{ratio}}(A, B) = \text{RDS}_{\text{macro}}(A) / \text{RDS}_{\text{macro}}(B)$
- **Interpretation:** Higher = more reasoning quality per token spent

## Hop-Depth F1 Degradation $\star$

Measures how F1 degrades as reasoning chain length increases:

$$\text{F1@hop}(s, k) = \text{mean}(\text{F1} \mid \text{hop\_depth} = k)$$

Reported for $k = 1, 2, 3, 4, 5+$.

!!! info "Expected Finding"
    RAG degrades steeply at $k \geq 2$ because embeddings don't encode transitive relationships. CKG remains flat due to explicit edge traversal.

## Tokenomics Metrics

### Context Utilization Rate $\star$ (CUR)

Fraction of retrieved tokens relevant to the answer:

$$\text{CUR} = \frac{\text{relevant\_tokens}}{\text{total\_retrieved\_tokens}}$$

### Cost Per Correct Answer $\star$ (CPCA)

Real-world cost using Claude Sonnet 4.6 pricing ($3/M input, $15/M output):

$$\text{CPCA} = \frac{\text{cost\_per\_query}}{\text{F1}}$$

### Precision at Token Budget (P@T)

Mean F1 over queries where tokens consumed $\leq$ budget $T$.

Reported for $T = 500, 1000, 2000, 5000, 10000$.

### Token Budget Breakeven

Minimum budget where RAG/GraphRAG F1 $\geq$ CKG F1:

$$\text{breakeven} = \min T \text{ such that } \text{F1}_{\text{RAG}}(T) \geq \text{F1}_{\text{CKG}}(500)$$

### Index Build Cost

One-time cost: tokens consumed during indexing + wall-clock time + storage. CKG: **zero** (CSV already exists).

### Update Cost $\star$

Cost to incorporate one new concept. CKG edits one CSV row with zero re-indexing.

## Structural Fidelity Metrics

### Relationship Precision $\star$ (RP)

Of edges returned, what fraction are real DAG edges:

$$\text{RP} = \frac{|E_{pred} \cap E_{truth}|}{|E_{pred}|}$$

### Hub Node Recall $\star$ (HNR)

Recall on high-indegree concepts (top 20% by indegree).

### Boundary Completeness $\star$ (BC)

For T4 queries, fraction of the taxonomy category returned:

$$\text{BC} = \frac{|retrieved \cap members|}{|members|}$$

CKG achieves BC $\approx$ 1.0 by construction.

## Robustness Metrics

### Paraphrase Stability (PS)

F1 variance across 5 paraphrased versions of each query. CKG should be stable (exact concept match); RAG is embedding-sensitive.

### Hallucination Rate (HR)

Fraction of queries returning at least 1 concept not in the corpus. CKG: HR = 0 by construction.

## Summary

| Metric | Type | Novel | Favors |
|--------|------|-------|--------|
| Token F1 | Quality | No | Mixed |
| Edge F1 | Quality | No | CKG |
| Exact Match | Quality | No | CKG |
| RDS | Compound | $\star$ | CKG |
| F1 by Hop Depth | Quality x Structure | $\star$ | CKG |
| CUR | Efficiency | $\star$ | CKG |
| CPCA | Cost | $\star$ | CKG |
| P@T | Cost x Quality | $\star$ | CKG |
| Token Budget Breakeven | Cost | $\star$ | CKG |
| Index Build Cost | Operational | No | CKG |
| Update Cost | Operational | $\star$ | CKG |
| Relationship Precision | Structural | $\star$ | CKG |
| Hub Node Recall | Structural | $\star$ | CKG |
| Boundary Completeness | Structural | $\star$ | CKG |
| Paraphrase Stability | Robustness | No | CKG |
| Hallucination Rate | Robustness | No | CKG |
