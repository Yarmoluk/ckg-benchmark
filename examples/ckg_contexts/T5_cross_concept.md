# CKG Context Example — T5: Cross-Concept Relationship

**Query:** How does Indeterminate Powers relate to L'Hospital's Rule?

**Retrieved context sent to Claude (334 tokens):**

```
KNOWLEDGE GRAPH SUBGRAPH:
  [APPL] Indeterminate Powers | prerequisites: L'Hospital's Rule
  [APPL] L'Hospital's Rule | prerequisites: Indeterminate Form, Zero Over Zero Form, Infinity Over Infinity
  [LIMIT] Indeterminate Form | prerequisites: Direct Substitution
  [LIMIT] Zero Over Zero Form | prerequisites: Indeterminate Form
  [LIMIT] Infinity Over Infinity | prerequisites: Indeterminate Form
```

**Claude's answer:**
> Indeterminate Powers directly depends on L'Hospital's Rule — it is a prerequisite. L'Hospital's Rule is used to evaluate limits of the form 0⁰, ∞⁰, or 1^∞ by converting them into 0/0 or ∞/∞ forms, which L'Hospital's Rule then resolves. The relationship chain is: Indeterminate Form → (Zero Over Zero Form or Infinity Over Infinity) → L'Hospital's Rule → Indeterminate Powers.

**Metrics:**
- Tokens consumed: 334
- F1: 0.326 (improving — BFS depth fix in progress)
- RDS: 0.000976

**Current limitation:** T5 currently uses 1-hop neighbor lookup. The BFS shortest-path fix — traversing intermediate nodes between two arbitrary concepts — will significantly improve T5 F1. Current work shows projected improvement from 0.33 → 0.55–0.70 once full BFS traversal is deployed.

**Why T5 is the novel contribution:** No RAG benchmark measures cross-domain concept relationships. T5 is the first measurable proxy for emergent intelligence — the ability to find connections that span multiple subgraphs. This is what the patent's "compound knowledge graph environment" claim refers to.
