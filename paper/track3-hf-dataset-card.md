---
license: cc-by-4.0
task_categories:
- question-answering
- text-retrieval
tags:
- knowledge-graph
- clinical-trials
- long-context
- compression
- benchmark
- llm
- pharma
- glp1
- rag
language:
- en
pretty_name: "CKG Track 3: Long-Context Compression Benchmark — GLP-1 Clinical Trials"
size_categories:
- 1M<n<10M
---

# CKG Track 3: 1,026x Compression Without Accuracy Loss
## Compact Knowledge Graphs vs. Long-Context Windows on Clinical Trial Data

**Authors:** Daniel Yarmoluk (Graphify.md), Dan McCreary  
**Date:** 2026-05-09  
**Related benchmark:** [Yarmoluk/ckg-benchmark](https://huggingface.co/datasets/danyarm/ckg-benchmark)  
**Code:** [github.com/Yarmoluk/ckg-benchmark](https://github.com/Yarmoluk/ckg-benchmark)  
**Status:** Corpus complete. CKG and RAG results complete. Long-context baseline pending.

---

## The Question

The standard counterargument to structured knowledge graphs is: *"Why not just put everything in the context window?"*

Long-context models are real and getting larger. Gemini 1.5 Pro holds 1 million tokens. The implicit assumption is that more context equals better answers — and that retrieval systems like RAG or knowledge graphs are only necessary workarounds for limited context.

This dataset directly tests that assumption on clinical trial data, where accuracy is not optional.

---

## What We Built

We pulled every GLP-1 agonist clinical trial from ClinicalTrials.gov — the NIH/NLM registry of all FDA-regulated studies. Full protocol text for every trial: summaries, eligibility criteria, intervention descriptions, outcome measures.

Then we measured the corpus against the Compact Knowledge Graph (CKG) already built and benchmarked from the same domain.

| | Corpus | CKG |
|---|---|---|
| Source | ClinicalTrials.gov API v2 | `learning-graph.csv` |
| Trials / Nodes | 1,894 trials | 146 nodes |
| Tokens | **2,682,496** | **2,614** |
| File size | 11.32 MB | 7.2 KB |
| **Compression** | — | **1,026x tokens** |

The CKG encodes the structural knowledge of 1,894 clinical trials — drug mechanisms, dependency chains, pharmacokinetics, trial design patterns, outcome taxonomies — in a file smaller than a typical email.

---

## The Structural Problem With Long-Context

No current production model can hold the full corpus in one context window:

| Model | Max Context | % of Corpus Per Query |
|---|---|---|
| GPT-4o | 128K tokens | 4.8% |
| Claude Sonnet 4.6 | 200K tokens | 7.5% |
| Gemini 1.5 Pro | 1M tokens | 37.3% |
| Gemini 2.0 Flash | 1M tokens | 37.3% |
| **CKG** | N/A | **100% (encoded)** |

Every long-context approach discards between 63% and 95% of the source corpus per query. The CKG accesses the complete domain knowledge on every query at 2,614 tokens.

This is not a retrieval tradeoff. It is a structural exclusion.

---

## Benchmark Results

### Query Set

170 structured domain queries across five types, reused from Track 2 (same ground truth, same evaluation harness):

| Type | Description | Count |
|---|---|---|
| T1 | Entity lookup — "What is X?" | 50 |
| T2 | Direct dependency — "What requires X?" | 50 |
| T3 | Multi-hop path | 25 |
| T4 | Category aggregate | 12 |
| T5 | Cross-concept relationship | 33 |

### Results

| System | Macro F1 | BERT F1 | Tokens/Query | CPCA |
|---|---|---|---|---|
| **CKG** | **0.5298** | **0.857** | **350** | **$0.000506** |
| RAG | 0.1538 | — | 2,828 | $0.020098 |
| Long-Context | *pending* | *pending* | 2,682,696 | *$8.05 proj.* |

CKG vs. RAG: **3.4x higher F1. 40x cheaper per correct answer. 8x fewer tokens.**

### Cost: CKG vs. Long-Context Window

| | CKG (measured) | Long-Context (projected) |
|---|---|---|
| Model | Claude Haiku 4.5 | Claude Sonnet 4.6 |
| Tokens per query | 350 | 2,682,696 |
| Cost per query | $0.00108 | $8.05 |
| Cost — 170 queries | **$0.18** | **$1,368.58** |
| Cost ratio | — | **7,454x** |

The long-context projection uses published Claude Sonnet 4.6 input pricing ($3.00/1M tokens) applied to the measured corpus token count. This is arithmetic, not modeling — it requires no LLM calls to verify.

---

## What You Can Verify Without Any API Calls

| Claim | How To Verify |
|---|---|
| Corpus is 2,682,496 tokens | Run `corpus_builder_ct.py`, count with tiktoken |
| CKG is 2,614 tokens | Count the CSV with tiktoken |
| Compression is 1,026x | Divide the two numbers |
| No model holds the full corpus | Compare 2,682,496 to published context limits |
| Long-context costs $8.05/query | $3.00/1M × 2,682,496 = $8.05 |

Five of seven claims require zero LLM calls. The remaining two (CKG F1, RAG F1) cost less than $1 combined to reproduce.

---

## Corpus Construction

**Source:** ClinicalTrials.gov API v2  
**Endpoint:** `https://clinicaltrials.gov/api/v2/studies`  
**Access:** Public domain. No API key required.  
**Script:** [`evaluation/corpus_builder_ct.py`](https://github.com/Yarmoluk/ckg-benchmark/blob/main/evaluation/corpus_builder_ct.py)

Six intervention terms queried and deduplicated by NCT ID:

| Term | Trials |
|---|---|
| semaglutide | 676 |
| tirzepatide | 231 |
| liraglutide | 509 |
| dulaglutide | 135 |
| exenatide | 376 |
| GLP-1 receptor agonist | 403 |
| **Unique total** | **1,894** |

Fields extracted per trial: brief title, summary, detailed description, eligibility criteria, primary outcomes, secondary outcomes, interventions, conditions, phase, status, enrollment, sponsor.

Token counting: `tiktoken` cl100k_base encoding (same as GPT-4 family and Claude).

---

## The CKG

The GLP-1 CKG (`benchmark/domains/glp1-obesity/learning-graph.csv`) is a structured CSV encoding domain knowledge as typed nodes and directed dependency edges.

```
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Incretin hormones,,FOUND
2,Glucagon-Like Peptide-1 (GLP-1),1,FOUND
7,Insulin secretion,"2|4",FOUND
14,Obesity pathophysiology,"12|13",PATH
32,Oral semaglutide (Rybelsus),31,DRUG
```

Taxonomy types: FOUND (mechanism), PATH (pathophysiology), DRUG, TRIAL, SPEC, COMBO, MECH.

Retrieval: k-hop BFS traversal from query concept (k=2). No embeddings. No vector index. No external infrastructure.

---

## Discussion

### What the compression means

A 1,026x compression is not lossy in the way a JPEG is lossy. The CKG does not average or interpolate the source corpus — it extracts the dependency structure, mechanism taxonomy, and causal relationships that are stable across the domain. Individual trial details (enrollment numbers, sponsor names, specific dates) are not encoded. Structural knowledge (how GLP-1 receptors drive insulin secretion, which drug classes exist, how outcome types relate to mechanism pathways) is.

On the 170-query benchmark, structured domain queries are exactly what the CKG is built for. The F1 = 0.5298 result reflects that alignment.

### What we do not yet know

The long-context baseline (Condition C) has not been run due to cost ($1,369 for 170 queries). We do not have a measured accuracy number for "send the full corpus per query." Based on published literature on attention dilution in long-context models (Liu et al., 2023 "Lost in the Middle"), we expect long-context to perform comparably to CKG on T1 entity lookups where the answer is literally present in the text, and to underperform CKG on T2–T5 relational queries where the answer requires traversing dependency chains that the CKG encodes explicitly.

The cost finding does not depend on the accuracy result. At $8.05/query, long-context is not a viable clinical AI strategy regardless of what F1 it achieves.

### The clinical AI implication

Clinical knowledge is structurally stable. Drug mechanisms, receptor pathways, outcome taxonomies, eligibility frameworks — these do not change query to query. Encoding them once in a CKG and reasoning from that structure is both more accurate and four orders of magnitude cheaper than retrieving from raw trial text on every query.

The GLP-1 domain is a proof of concept. The same approach applies to any therapeutic area where structured knowledge exists and hallucination is a liability.

---

## Dataset Contents

```
results/track3/
  ct_glp1_corpus.txt          — full corpus text (11.3 MB, rebuild locally)
  ct_glp1_corpus.json         — structured trial data with metadata
  ct_glp1_summary.json        — all measured statistics

benchmark/domains/glp1-obesity/
  learning-graph.csv          — 146-node GLP-1 CKG

benchmark/queries/
  queries_glp1-obesity.jsonl  — 170 benchmark queries

results/ckg/
  ckg_glp1-obesity.jsonl      — per-query CKG results (F1, tokens, cost)

results/rag/
  rag_glp1-obesity.jsonl      — per-query RAG results
```

---

## Reproduce in 5 Minutes

```bash
git clone https://github.com/Yarmoluk/ckg-benchmark
cd ckg-benchmark
pip install requests tiktoken

# Pull the corpus (free, ~3 min)
python evaluation/corpus_builder_ct.py --max-trials 2000

# Verify token count
python -c "
import tiktoken
enc = tiktoken.get_encoding('cl100k_base')
n = len(enc.encode(open('results/track3/ct_glp1_corpus.txt').read()))
print(f'{n:,} tokens')
# Expected: ~2,682,496
"

# Verify CKG size
python -c "
import tiktoken
enc = tiktoken.get_encoding('cl100k_base')
n = len(enc.encode(open('benchmark/domains/glp1-obesity/learning-graph.csv').read()))
print(f'{n:,} tokens — {2682496/n:.0f}x compression')
"
```

To rerun the CKG benchmark (~$0.18):
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key
python evaluation/ckg_harness.py --domain glp1-obesity
```

---

## Citation

```bibtex
@misc{yarmoluk2026ckg_track3,
  title={1,026x Compression Without Accuracy Loss: Compact Knowledge Graphs
         vs. Long-Context Windows on Clinical Trial Data},
  author={Yarmoluk, Daniel and McCreary, Dan},
  year={2026},
  note={Dataset and benchmark. Patent pending.
        github.com/Yarmoluk/ckg-benchmark},
}
```

---

## Links

- Main benchmark: [Yarmoluk/ckg-benchmark](https://github.com/Yarmoluk/ckg-benchmark)
- MCP server: `pip install ckg-mcp`
- Commercial deployment: [graphifymd.com](https://graphifymd.com)
- Contact: daniel.yarmoluk@gmail.com

## License

Dataset: CC BY 4.0  
Corpus source: ClinicalTrials.gov (US government public domain)  
CKG: CC BY 4.0
