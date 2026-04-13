# Tokenomics Framework

## Why Tokenomics Matters

Standard IR benchmarks (BEIR, RAGAS, MTEB) measure quality only.
In production LLM systems, token cost is a first-class constraint:

- Enterprise AI budgets are token-denominated
- Latency scales with token count
- Context window limits bound what can be retrieved
- Cost per query determines whether a system is deployable at scale

**This paper argues: a retrieval system that achieves F1=0.85 at 300 tokens
is strictly better than one achieving F1=0.87 at 4,000 tokens for most
real-world deployments.**

---

## Token Accounting Methodology

All token counts use the Anthropic `count_tokens()` API at `temperature=0`.

For each query, we track:

```python
@dataclass
class TokenAccount:
    query_tokens: int          # The question itself
    retrieval_tokens: int      # Context retrieved (chunks / graph / edges)
    prompt_tokens: int         # System prompt + query + context
    completion_tokens: int     # Generated answer
    total_tokens: int          # prompt + completion

    # Derived
    @property
    def cost_usd(self) -> float:
        # Claude Sonnet 4.6: $3/M input, $15/M output
        return (self.prompt_tokens * 3 + self.completion_tokens * 15) / 1_000_000
```

---

## The Tokenomics Stack

Each system has a different token profile:

### RAG Token Profile
```
Query → Embed query (small, ~100 tokens)
      → Retrieve top-5 chunks (~512 × 5 = 2,560 tokens)
      → LLM prompt = system + query + 2,560 context + answer
      
Typical total: 3,000–5,000 tokens per query
Noise ratio: high (chunks contain off-topic content)
```

### GraphRAG Token Profile
```
Query → Entity extraction → community lookup → summarization
      → LLM prompt = system + query + community summary + answer
      
Typical total: 2,000–8,000 tokens per query (high variance)
Noise ratio: medium (summaries are compressed but lossy)
Build cost: HIGH — full text extraction once per corpus
```

### CKG Token Profile
```
Query → Concept match in CSV → subgraph extraction (BFS/DFS)
      → LLM prompt = system + query + subgraph edges + answer
      
Typical total: 150–400 tokens per query
Noise ratio: near-zero (exact subgraph, no off-topic content)
Build cost: ZERO — CSV already exists
```

---

## Efficiency Curves

We plot three efficiency curves per system:

### Curve 1: F1 vs Token Budget
```
For each token budget B in [100, 250, 500, 1000, 2000, 5000, 10000]:
  score(system, B) = mean F1 over queries where tokens ≤ B
```

Expected shape:
- CKG: reaches plateau at ~400 tokens
- RAG: rises slowly, plateaus at ~4,000 tokens
- GraphRAG: variable, expensive queries hurt average

### Curve 2: RDS vs Hop Depth
```
For each hop depth k in [1, 2, 3, 4, 5+]:
  RDS_at_hop(system, k) = mean(F1/tokens) for queries at depth k
```

CKG's RDS should be flat across hop depths.
RAG's RDS should collapse at k≥3.

### Curve 3: Cost Per Correct Answer vs Domain Complexity
```
domain_complexity = mean_hop_depth × concept_count / 200
CPCA(system, domain) = mean(cost_usd / F1) over domain queries
```

---

## Practical Deployment Scenarios

We model three deployment scenarios to contextualize results:

| Scenario | Queries/day | Annual cost (RAG) | Annual cost (CKG) | Savings |
|----------|-------------|-------------------|-------------------|---------|
| Small team | 1,000 | ~$X | ~$Y | ~Zx |
| Mid-market | 10,000 | ~$X | ~$Y | ~Zx |
| Enterprise | 100,000 | ~$X | ~$Y | ~Zx |

*(Fill with actual token counts post-experiment)*

---

## The "Structure Premium" Hypothesis

**Hypothesis:** The token efficiency gap between CKG and RAG is not random —
it is proportional to the structural richness of the domain's DAG.

```
structure_premium(domain) = RDS_ratio(CKG/RAG, domain)
dag_richness(domain) = edges / concepts × mean_indegree × (1 / orphan_rate)
```

If `structure_premium` correlates with `dag_richness` (r > 0.7),
this validates the core theoretical claim: **explicit structure is the
source of the efficiency gain, not domain selection bias.**

This is testable across 25 McCreary domains and would be a strong
theoretical contribution beyond the empirical benchmark.
