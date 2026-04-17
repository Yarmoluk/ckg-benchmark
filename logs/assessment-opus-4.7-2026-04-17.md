# CKG Benchmark — Independent Assessment

**Reviewer:** Claude Opus 4.7 (1M context), invoked by Dan McCreary
**Date:** 2026-04-17
**Scope:** Full repository audit — methodology, execution, framing, and commercial thesis
**Audience:** Daniel Yarmoluk (co-author), Dan McCreary (co-author)

---

## Executive summary

The repository contains real engineering, real experimental runs across 44 domains, and a useful novel metric (RDS). It is not vaporware. However, in its current form it will not survive peer review on cs.IR, and the headline "45.9× RDS advantage" claim is not defensible as written. The three issues that must be fixed before ArXiv submission are: 

- (1) a circular benchmark design
- (2) incomplete and asymmetric baseline execution, and
- (3) a misleading name ("Compressed" Knowledge Graph, where no compression occurs — the authors' own internal notes concede this).

The commercial thesis is stronger than the paper suggests, but for a different reason than currently framed. The value is not the CKG inference pattern (which is well-known schema-in-context prompting). The value is the **DAG-curation pipeline** — `/generate-learning-graph` plus SME review — combined with low per-query inference cost. That is a real, sellable offering. The paper should be repositioned to match.

This assessment is candid. It is written to help the work land, not to discourage it.

---

## What is genuinely strong

- **Real experimental infrastructure.** `evaluation/ckg_harness.py` and `evaluation/rag_harness.py` are implemented, runnable, and produce per-query output. This is not a proposal-stage project.
- **The McCreary corpus as a benchmark artifact.** 44 domains with a uniform schema (`ConceptID, Label, Dependencies, TaxonomyID`) is a genuinely useful contribution to the community regardless of the paper's other claims.
- **The RDS metric** (F1 per token consumed) is a modest but defensible contribution. Cost-aware retrieval metrics are underused and this one is cleanly defined.
- **Intellectual honesty in internal logs.** `paper/logs/not-compression-just-a-dag.md` and `paper/logs/major-concern-dag-is-not-search.md` show the author identified the project's methodological weaknesses and wrote them down. That is the right instinct. These concerns now need to be acted on, not archived.

---

## The three blockers

### 1. The benchmark is circular by construction

Every query type (T1 through T5) has ground-truth labels derived from the same CSV columns that CKG reads directly at inference time. `evaluation/generate_queries.py` pulls dependency labels from the `Dependencies` column, computes paths by BFS over the DAG, and filters taxonomy members from `TaxonomyID`. RAG and GraphRAG are asked to reconstruct, from narrative prose, a structure that CKG is handed in source form.

The 45.9× RDS ratio is arithmetically correct. But it measures **"direct access beats reconstruction"** — which is tautological. A reviewer will say: "Of course a system that reads the answer key scores higher than one that must infer it from prose." This is the single largest risk to the paper and it was flagged internally but never resolved.

### 2. Baselines are incomplete and asymmetric

- **RAG ran on approximately 3,499 of ~7,588 queries.** Per-domain counts are uneven (e.g., calculus: CKG 180 queries, RAG 3). The commit log says "40/44 domains" but the per-domain distribution tells a different story.
- **GraphRAG is absent from final results.** Early commits mention a GraphRAG harness; the final summary files contain no GraphRAG numbers. Either it was dropped silently or it failed.
- **Placeholder numbers remain in `paper/outline.md`** ("F1 of X.XX").
- **The 5% human-annotator validation promised in the outline is not evident in the results.**

Any reviewer who compares the two summary files will spot this in under a minute.

### 3. The name "Compressed Knowledge Graph" is misleading

There is no compression algorithm and no compression step. The CSV is authored (or agent-generated) directly. The project's own log `not-compression-just-a-dag.md` concedes this. Keeping the name invites dismissal in a reviewer's first paragraph. Candidate replacements: **Structured Context Retrieval**, **Schema-Grounded Retrieval**, **DAG-in-Context Retrieval**. Pick one that doesn't make a false claim on the cover page.

---

## The commercial thesis, honestly framed

Daniel's core commercial intuition — that structured knowledge representations can dramatically lower the cost of enterprise retrieval — is correct. The current paper just isn't the evidence for it.

The strongest version of the pitch is not "CKG beats RAG 45×." That claim rides on a benchmark designed to favor CKG and will be challenged. The defensible version is:

> **"If you invest in curating a domain DAG — which is now a one-day agentic-skill workflow plus SME review — you get per-query retrieval that is dramatically cheaper and structurally hallucination-free. Here is the benchmark that quantifies that payoff."**

That is sellable, true, and doesn't overclaim. It also positions the actual product correctly: the valuable thing Daniel would be selling is the **DAG-curation process** (agent + SME review loop), not the inference-time trick. The inference-time cost savings are how the DAG pays for itself; they are not the novelty.

### The schema-fit caveat that needs to be said out loud

Learning graphs encode one relationship type: *prerequisite*. Teaching is prerequisite-structured, so textbook domains fit naturally. Many enterprise domains do not. Tax code, clinical guidelines, contract clauses, regulatory corpora — these need richer shapes (*supersedes*, *conflicts with*, *applies to jurisdiction X*, *is subtype of*, temporal validity, authority hierarchy). A prereq DAG is the wrong primitive for most of them.

The footgun: `/generate-learning-graph` will confidently produce a plausible-looking DAG for a domain where a DAG isn't the right structure. The SME may not catch it because the output *looks* reasonable. The damage shows up later as confident wrong answers at query time. Before this goes commercial, the schema needs to be extensible or the target domain needs to be chosen for structural fit.

---

## Recommended next steps, in priority order

### P0 — Do before any further paper work

1. **Rename the method.** Drop "Compressed." Decide on a replacement now, and rename in code, paper, README, and dataset card in one pass. Every week this stays is additional rework and additional reviewer ammunition.
2. **Finish the RAG run.** Bring RAG to query-count parity with CKG across all 44 domains. Re-compute the macro RDS. The headline number will change and that is fine — a smaller, honest number beats a larger, challenged one.
3. **Resolve GraphRAG.** Either complete the run and report it, or explicitly state in the paper why GraphRAG is out of scope. Silent omission will be noticed.

### P1 — The single experiment that would elevate the paper

4. **Run `/generate-learning-graph` on one non-textbook, non-prerequisite domain**, then evaluate CKG vs RAG on it. Suggested candidates: a slice of a regulatory corpus, a clinical guideline set, or a contract-clause library. This is the only experiment that answers the generalization question reviewers will ask. If CKG still wins on an agent-generated DAG in a domain nobody hand-designed, the paper's claims are defensible. If it doesn't, you have learned the real boundary of the technique before betting a company on it — which is also valuable.

### P2 — Methodological fixes for the benchmark itself

5. **Add a fair structured-prompting baseline.** Feed RAG the same `Dependencies` information formatted as prose, or let GraphRAG's entity extractor run to completion on the chapter text. If CKG still wins, you have isolated the advantage from the trivial "direct-access" effect. This directly addresses the circularity objection.
6. **Add one partial-DAG condition.** Take an existing domain, remove 30% of edges, and re-run. This demonstrates behavior under realistic DAG-quality assumptions — the regime any enterprise customer will actually operate in.
7. **Execute the 5% human-annotator validation** promised in `paper/outline.md`, or remove the claim.

### P3 — Framing changes for submission

8. **Reposition the paper from "novel architecture" to "benchmark + metric."** The McCreary corpus and RDS metric are the defensible contributions. The CKG technique is a straightforward application of schema-in-context prompting — say so plainly and the reviewer has nothing to attack.
9. **Add a Related Work subsection on schema-in-context / structured prompting.** Treating this as novel is the fastest path to desk rejection. Citing it honestly is the fastest path to acceptance.
10. **Add an explicit Limitations section.** State: the benchmark assumes a curated DAG exists; the query types are structural and favor structured retrieval; generalization to domains without prerequisite structure is untested except for the P1 experiment above.

---

## Bottom line

The work is real. The numbers, as currently presented, promise more than the experiment proves. The fixes above are not cosmetic — several of them will change headline numbers — but none of them require starting over. With P0 and P1 done, this becomes a credible ArXiv submission and a defensible commercial story. Without P0 and P1, it is neither.

The repository's greatest strength is that its authors already wrote down the objections a reviewer would raise. The next step is to answer them.
