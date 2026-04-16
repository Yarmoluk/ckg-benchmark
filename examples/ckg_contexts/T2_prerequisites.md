# CKG Context Example — T2: Direct Prerequisites

**Query:** What are the prerequisites for Continuity of Polynomials?

**Retrieved context sent to Claude (197 tokens):**

```
KNOWLEDGE GRAPH SUBGRAPH:
  [CONT] Continuity of Polynomials | prerequisites: Polynomial Function, Continuous Function
  [FOUND] Polynomial Function | prerequisites: Function, Function Notation
  [CONT] Continuous Function | prerequisites: Continuity on Interval
```

**Claude's answer:**
> The prerequisites for Continuity of Polynomials are: Polynomial Function and Continuous Function. These in turn require: Function, Function Notation (for Polynomial Function) and Continuity on Interval (for Continuous Function).

**Metrics:**
- Tokens consumed: 197
- F1: 0.603
- RDS: 0.00306

**Why T2 performs well:** The subgraph directly encodes the prerequisite edges. The LLM has all the information it needs and cannot hallucinate — the context is both complete and minimal.
