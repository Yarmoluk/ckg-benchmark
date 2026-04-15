# Discussion

## Where CKG Wins and Why

CKG's advantages are structural:

- **T2/T3 queries**: Explicit edges eliminate multi-hop inference errors. RAG must infer transitive dependencies from unstructured text; CKG traverses them directly via BFS/DFS.
- **T4 queries**: Taxonomy filtering achieves BC $\approx$ 1.0 by construction, as the TaxonomyID field provides exact category membership.
- **Hallucination**: HR = 0 because CKG only returns concepts present in the source CSV. No generative step can introduce phantom entities.
- **RDS**: Near-zero build cost combined with 150--400 tokens per query yields order-of-magnitude efficiency gains.

## Where RAG Is Competitive

RAG remains competitive in specific scenarios:

- T1 entity lookup on large open-domain corpora where rich context aids natural language generation
- Domains without stable taxonomy (rapidly evolving fields)
- When CKG construction cost exceeds the efficiency savings

## GraphRAG's Position

GraphRAG occupies a middle ground: better than RAG on multi-hop reasoning (graph structure helps) but worse than CKG (dynamic extraction introduces noise and hallucinated edges). GraphRAG is the most expensive system (high build cost + high query cost). Its best use case is unstructured corpora with no available expert taxonomy.

## The Structure Premium

We hypothesize that the token efficiency gap between CKG and RAG is proportional to the structural richness of the domain's DAG:

$$\text{dag\_richness}(d) = \frac{\text{edges}}{\text{concepts}} \times \text{mean\_indegree} \times \frac{1}{\text{orphan\_rate}}$$

If the correlation between structure\_premium and dag\_richness exceeds $r = 0.7$, this validates the core theoretical claim: **explicit structure is the source of the efficiency gain, not domain selection bias**.

## Limitations

- The McCreary corpus is educational---results may not generalize to legal, financial, or medical domains.
- CKG requires upfront expert curation investment; this cost is not reflected in the benchmark's zero-build-cost assumption.
- Ground truth derived from DAG edges may not capture all valid natural language answers.
- All systems use the same LLM (Claude Sonnet 4.6); results may differ with other models.
