# CKG Context Example — T4: Category Aggregate

**Query:** List all FOUND concepts in this knowledge graph

**Retrieved context sent to Claude (573 tokens):**

```
KNOWLEDGE GRAPH SUBGRAPH:
  [FOUND] Function | prerequisites: none
  [FOUND] Domain and Range | prerequisites: Function
  [FOUND] Function Notation | prerequisites: Function
  [FOUND] Composite Function | prerequisites: Function, Function Notation
  [FOUND] Inverse Function | prerequisites: Function, Domain and Range
  [FOUND] Graphing Functions | prerequisites: Function, Domain and Range
  [FOUND] Piecewise Function | prerequisites: Function, Graphing Functions
  [FOUND] Even and Odd Functions | prerequisites: Function, Graphing Functions
  [FOUND] Function Transformations | prerequisites: Function, Graphing Functions
  [FOUND] Polynomial Function | prerequisites: Function, Function Notation
  [FOUND] Rational Function | prerequisites: Polynomial Function
  [FOUND] Exponential Function | prerequisites: Function, Function Notation
  [FOUND] Logarithmic Function | prerequisites: Exponential Function
  [FOUND] Trigonometric Function | prerequisites: Function
  [FOUND] Unit Circle | prerequisites: Trigonometric Function
  [FOUND] Radian Measure | prerequisites: Unit Circle
  [FOUND] Trigonometric Identities | prerequisites: Trigonometric Function, Unit Circle
  [FOUND] Coordinate System | prerequisites: none
  [FOUND] Number Line | prerequisites: Coordinate System
  [FOUND] Real Numbers | prerequisites: Number Line
```

**Claude's answer:**
> The FOUND (foundational) concepts in this knowledge graph are:
> Function, Domain and Range, Function Notation, Composite Function, Inverse Function, Graphing Functions, Piecewise Function, Even and Odd Functions, Function Transformations, Polynomial Function, Rational Function, Exponential Function, Logarithmic Function, Trigonometric Function, Unit Circle, Radian Measure, Trigonometric Identities, Coordinate System, Number Line, Real Numbers

**Metrics:**
- Tokens consumed: 573
- F1: **0.951** (near-perfect)
- RDS: 0.00166

**Why T4 is near-perfect:** The filter is deterministic. The graph has exactly the nodes the query asks for, labeled explicitly. The LLM does zero reasoning — it reads a list and returns it. This is the ceiling for LLM retrieval tasks.

**Note:** T4's 573-token context is the largest in the benchmark. Even at nearly 3x the typical token count, it still costs 5x less than RAG's 2,983-token mean.
