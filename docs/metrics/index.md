# Metrics Overview

The CKG Benchmark evaluates 16 metrics organized into six categories.

## Why New Metrics?

Standard IR benchmarks (BEIR, RAGAS, MTEB) measure **quality only**. In production LLM systems, token cost is a first-class constraint. A system achieving F1=0.85 at 300 tokens is strictly better than one achieving F1=0.87 at 4,000 tokens for most deployments.

This benchmark introduces metrics that jointly measure quality and efficiency.

## Metric Categories

| Category | Metrics | Novel |
|----------|---------|-------|
| **Standard IR** | Token F1, Edge F1, Exact Match | 0 |
| **Compound** | RDS (Reasoning Density Score) | 1 |
| **Structural** | Hop-Depth F1, Relationship Precision, Hub Node Recall, Boundary Completeness | 4 |
| **Tokenomics** | CUR, CPCA, P@T, Token Budget Breakeven, Index Build Cost, Update Cost | 4 |
| **Robustness** | Paraphrase Stability, Hallucination Rate | 0 |

**10 of 16 metrics are novel** to this paper.

## The Key Metric: RDS

$$\text{RDS} = \frac{\text{F1}}{\text{tokens\_consumed}}$$

Higher RDS = more reasoning quality per token spent.

For detailed definitions of all 16 metrics, see [Metrics Specification](metrics-spec.md).

For the token cost framework, see [Tokenomics](tokenomics.md).
