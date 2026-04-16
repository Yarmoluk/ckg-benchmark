# CKG Context Example — T3: Multi-Hop Learning Path

**Query:** What is the prerequisite chain from Function to Derivative of a to x?

**Retrieved context sent to Claude (325 tokens):**

```
KNOWLEDGE GRAPH SUBGRAPH:
  [DRULE] Derivative of a to x | prerequisites: Derivative of e to x
  [DRULE] Derivative of e to x | prerequisites: Derivative Rules, Exponential Function
  [FOUND] Exponential Function | prerequisites: Function, Function Notation
  [FOUND] Function | prerequisites: none
```

**Claude's answer:**
> The prerequisite chain from Function to Derivative of a to x follows this path:
> Function → Exponential Function → Derivative of e to x → Derivative of a to x
> 
> With branching prerequisites: Function also requires Function Notation for the Exponential Function step, and Derivative Rules is needed alongside Exponential Function before reaching Derivative of e to x.

**Metrics:**
- Tokens consumed: 325
- F1: 0.614
- RDS: 0.00189

**Why T3 works:** BFS subgraph extraction finds the exact path. The LLM receives only the nodes on the path — no irrelevant concepts. The structured format makes multi-hop reasoning trivial.
