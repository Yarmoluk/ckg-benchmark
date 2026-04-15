# Tokenomics Framework

## Why Tokenomics Matters

Standard IR benchmarks measure quality only. In production LLM systems, token cost is a first-class constraint:

- Enterprise AI budgets are token-denominated
- Latency scales with token count
- Context window limits bound what can be retrieved
- Cost per query determines whether a system is deployable at scale

## Token Profiles

### RAG

| Metric | Value |
|--------|-------|
| Tokens per query | 3,000--5,000 |
| Noise ratio | High (off-topic chunk content) |
| Build cost | Embed all chunks |

### GraphRAG

| Metric | Value |
|--------|-------|
| Tokens per query | 2,000--8,000 (high variance) |
| Noise ratio | Medium (compressed summaries) |
| Build cost | HIGH (full text extraction) |

### CKG

| Metric | Value |
|--------|-------|
| Tokens per query | 150--400 |
| Noise ratio | Near-zero (exact subgraph) |
| Build cost | ZERO (CSV already exists) |

## Pricing Model

All costs computed at Claude Sonnet 4.6 pricing:

- **Input:** $3 per 1M tokens
- **Output:** $15 per 1M tokens

## The Structure Premium Hypothesis

The token efficiency gap between CKG and RAG is proportional to the structural richness of the domain's DAG:

$$\text{dag\_richness}(d) = \frac{\text{edges}}{\text{concepts}} \times \text{mean\_indegree} \times \frac{1}{\text{orphan\_rate}}$$

If structure\_premium correlates with dag\_richness ($r > 0.7$), this validates the core claim: **explicit structure is the source of the efficiency gain**.
