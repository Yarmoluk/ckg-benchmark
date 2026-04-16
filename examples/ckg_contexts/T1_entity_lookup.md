# CKG Context Example — T1: Entity Lookup

**Query:** What is Integral of a to x?

**Retrieved context sent to Claude (243 tokens):**

```
KNOWLEDGE GRAPH SUBGRAPH:
  [INTEG] Integral of a to x | prerequisites: Integral of e to x
  [INTEG] Integral of e to x | prerequisites: Indefinite Integral, Derivative of e to x
```

**Claude's answer:**
> The integral of a to x (∫aˣ dx) is aˣ/ln(a) + C, where a is a positive constant and ln(a) is the natural logarithm of a. This formula requires knowing the integral of e to x and the rules for exponential functions.

**Metrics:**
- Tokens consumed: 243
- F1: 0.189 (honest — entity lookup is the hardest query type; the answer is definitional, not graph-traversal)
- RDS: 0.000778

**Why T1 underperforms:** Entity lookup requires the LLM to produce a definition from a subgraph that only shows structural position. The graph encodes *relationships*, not raw definitions — this is a known limitation and expected negative control.
