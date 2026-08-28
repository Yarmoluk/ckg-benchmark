"""
Full-Context Harness — the no-retrieval control arm.

Why this exists
---------------
Every published comparison in this repository (CKG vs RAG vs GraphRAG) pits a
retrieval system against another retrieval system. None of them answers the
question a reviewer asks first:

    "What happens if you skip retrieval entirely and put the whole corpus in
     the context window?"

That omission is not hypothetical. It is the exact flaw that collapsed the
agent-memory literature in 2025-2026:

  * Zep reported 84% on LOCOMO; an independent reproduction got 58.44%.
  * Mem0 self-reported 93.4% on LongMemEval; Bench'd measured 32.4%.
  * In that same independent run, an LLM with NO memory scored 57.6% — beating
    almost every dedicated memory system.
  * Zep's own rebuttal concedes LOCOMO conversations are "easily within the
    context window capabilities of modern LLMs."

Any benchmark whose corpus fits in the context window is measuring retrieval
overhead, not retrieval value, unless it reports the no-retrieval control.

This harness is that control. It changes exactly one variable against
rag_harness.py — the retrieval step is removed. Same corpus loader, same model,
same temperature, same system prompt, same token_f1 scorer, same result schema,
so the arms are directly comparable and any difference is attributable to
retrieval rather than to harness drift.

Honest-failure contract
-----------------------
If a domain's corpus exceeds the usable context budget, this harness does NOT
silently truncate and report a score. Silent truncation is how a partial answer
gets reported as a complete one — the same failure this benchmark exists to
measure. Oversized domains are recorded with coverage="truncated" and the
dropped token count, or skipped entirely under --no-truncate.

Usage:
    python evaluation/fullcontext_harness.py --domain calculus
    python evaluation/fullcontext_harness.py --all
    python evaluation/fullcontext_harness.py --all --dry-run     # cost estimate, no API calls
    python evaluation/fullcontext_harness.py --all --no-truncate
    python evaluation/fullcontext_harness.py --measure-only      # corpus sizes, no queries
"""

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path

import anthropic

# Reuse the RAG harness verbatim for everything except retrieval. Importing
# rather than reimplementing is deliberate: a divergent corpus loader or scorer
# would make the arms incomparable, and that difference would be invisible in
# the results table.
from rag_harness import (
    CLAUDE_MODEL,
    PRICE_INPUT,
    PRICE_OUTPUT,
    SYSTEM_PROMPT,
    QUERIES_DIR,
    count_tokens,
    load_corpus_docs,
    summarize,
    token_f1,
)

RESULTS_DIR = Path("results/fullcontext")

# Usable context budget for the corpus itself, leaving headroom for the system
# prompt, the question, and the completion. Claude's window is far larger; this
# is the honest working ceiling, not a model limit.
CONTEXT_BUDGET_TOKENS = 150_000
MAX_COMPLETION_TOKENS = 512


def build_full_context(domain: str, budget: int = CONTEXT_BUDGET_TOKENS) -> dict:
    """Concatenate every document in a domain. No chunking, no ranking, no cutoff
    unless the corpus genuinely exceeds the budget.

    Returns a dict carrying its own coverage claim so downstream analysis can
    never mistake a truncated context for a complete one.
    """
    docs = load_corpus_docs(domain)
    if not docs:
        return {"context": "", "n_docs": 0, "corpus_tokens": 0,
                "context_tokens": 0, "coverage": "empty", "dropped_tokens": 0}

    blocks = [f"[Source: {d['source']}]\n{d['text']}" for d in docs]
    full = "\n\n---\n\n".join(blocks)
    corpus_tokens = count_tokens(full)

    if corpus_tokens <= budget:
        return {"context": full, "n_docs": len(docs), "corpus_tokens": corpus_tokens,
                "context_tokens": corpus_tokens, "coverage": "complete",
                "dropped_tokens": 0}

    # Over budget: keep whole documents in order until the budget is reached, and
    # report exactly what was dropped. Whole documents rather than a token slice,
    # so the model never sees a sentence cut mid-clause.
    kept, used = [], 0
    for b in blocks:
        t = count_tokens(b)
        if used + t > budget:
            break
        kept.append(b)
        used += t
    return {"context": "\n\n---\n\n".join(kept), "n_docs": len(kept),
            "corpus_tokens": corpus_tokens, "context_tokens": used,
            "coverage": "truncated", "dropped_tokens": corpus_tokens - used}


def run_domain(domain: str, ant_client, dry_run: bool = False,
               no_truncate: bool = False) -> list[dict]:
    queries_file = QUERIES_DIR / f"queries_{domain}.jsonl"
    if not queries_file.exists():
        print(f"  ✗ no queries file for {domain}")
        return []

    ctx = build_full_context(domain)
    if ctx["coverage"] == "empty":
        print(f"  ✗ no corpus content for {domain}")
        return []

    if ctx["coverage"] == "truncated":
        pct = 100 * ctx["dropped_tokens"] / ctx["corpus_tokens"]
        if no_truncate:
            print(f"  ⊘ {domain}: corpus {ctx['corpus_tokens']:,} tok exceeds budget "
                  f"— SKIPPED (--no-truncate)")
            return []
        print(f"  ⚠ {domain}: corpus {ctx['corpus_tokens']:,} tok > budget "
              f"{CONTEXT_BUDGET_TOKENS:,}; dropped {ctx['dropped_tokens']:,} ({pct:.1f}%)")

    queries = [json.loads(line) for line in open(queries_file)]
    print(f"  {domain}: {len(queries)} queries · {ctx['n_docs']} docs · "
          f"{ctx['context_tokens']:,} context tokens · {ctx['coverage']}")

    results = []
    for i, q in enumerate(queries):
        user_message = f"Context:\n{ctx['context']}\n\nQuestion: {q['query']}"

        if dry_run:
            est_in = ctx["context_tokens"] + count_tokens(q["query"]) + 40
            results.append({**q, "system": "fullcontext",
                            "predicted_answer": "[DRY RUN]",
                            "prompt_tokens": est_in, "completion_tokens": 0,
                            "total_tokens": est_in, "retrieved_tokens": ctx["context_tokens"],
                            "corpus_tokens": ctx["corpus_tokens"],
                            "coverage": ctx["coverage"],
                            "dropped_tokens": ctx["dropped_tokens"],
                            "f1": 0.0, "precision": 0.0, "recall": 0.0,
                            "rds": 0.0,
                            "cost_usd": round(est_in * PRICE_INPUT, 6),
                            "latency_ms": 0})
            continue

        t0 = time.time()
        try:
            response = ant_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=MAX_COMPLETION_TOKENS,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            latency_ms = int((time.time() - t0) * 1000)
            answer = response.content[0].text
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
        except Exception as e:
            print(f"    ✗ API error on {q.get('id', q.get('query_id', '?'))}: {e}")
            continue

        scores = token_f1(answer, q.get("ground_truth", []))
        total_tokens = prompt_tokens + completion_tokens
        rds = scores["f1"] / total_tokens if total_tokens > 0 else 0.0
        cost = prompt_tokens * PRICE_INPUT + completion_tokens * PRICE_OUTPUT

        results.append({
            **q,
            "system": "fullcontext",
            "predicted_answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "retrieved_tokens": ctx["context_tokens"],
            "corpus_tokens": ctx["corpus_tokens"],
            "coverage": ctx["coverage"],
            "dropped_tokens": ctx["dropped_tokens"],
            "f1": scores["f1"],
            "precision": scores["precision"],
            "recall": scores["recall"],
            "rds": round(rds, 8),
            "cost_usd": round(cost, 6),
            "latency_ms": latency_ms,
        })

        if (i + 1) % 25 == 0:
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            print(f"    [{i+1}/{len(queries)}] avg F1={avg_f1:.3f}")

        time.sleep(0.2)

    return results


def measure_only(domains: list[str]) -> None:
    """Report corpus size per domain without spending a token.

    This is the number that determines whether the benchmark's retrieval arms
    were ever solving a real problem. If corpora fit comfortably in context,
    the retrieval comparison is measuring overhead, not value.
    """
    print(f"  {'domain':<30}{'docs':>6}{'corpus_tok':>12}  fits?")
    rows = []
    for d in domains:
        ctx = build_full_context(d)
        if ctx["coverage"] == "empty":
            print(f"  {d:<30}{'—':>6}{'no corpus':>12}")
            continue
        fits = "yes" if ctx["coverage"] == "complete" else f"NO (-{ctx['dropped_tokens']:,})"
        print(f"  {d:<30}{ctx['n_docs']:>6}{ctx['corpus_tokens']:>12,}  {fits}")
        rows.append(ctx["corpus_tokens"])
    if rows:
        rows.sort()
        print(f"\n  domains={len(rows)}  median={rows[len(rows)//2]:,} tok  "
              f"max={rows[-1]:,} tok  budget={CONTEXT_BUDGET_TOKENS:,}")
        print(f"  fit in context: {sum(1 for r in rows if r <= CONTEXT_BUDGET_TOKENS)}/{len(rows)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--domain", help="Single domain to run")
    p.add_argument("--all", action="store_true", help="Run every domain with queries")
    p.add_argument("--dry-run", action="store_true", help="Estimate cost, no API calls")
    p.add_argument("--no-truncate", action="store_true",
                   help="Skip domains whose corpus exceeds the context budget")
    p.add_argument("--measure-only", action="store_true",
                   help="Report corpus sizes and exit")
    args = p.parse_args()

    if args.all or args.measure_only:
        domains = sorted(f.stem.replace("queries_", "")
                         for f in QUERIES_DIR.glob("queries_*.jsonl"))
    elif args.domain:
        domains = [args.domain]
    else:
        p.error("specify --domain, --all, or --measure-only")

    if args.measure_only:
        measure_only(domains)
        return

    client = None if args.dry_run else anthropic.Anthropic()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    all_summaries = {}
    for d in domains:
        res = run_domain(d, client, dry_run=args.dry_run, no_truncate=args.no_truncate)
        if not res:
            continue
        out = RESULTS_DIR / f"{d}.jsonl"
        with open(out, "w") as f:
            for r in res:
                f.write(json.dumps(r) + "\n")
        s = summarize(res)
        s["coverage"] = res[0].get("coverage")
        s["corpus_tokens"] = res[0].get("corpus_tokens")
        all_summaries[d] = s
        print(f"  → {d}: F1={s['macro_f1']} mean_tokens={s['mean_tokens']} "
              f"cost=${s['total_cost_usd']}")

    if all_summaries:
        with open(RESULTS_DIR / "_summary.json", "w") as f:
            json.dump(all_summaries, f, indent=2)
        tot = sum(s["total_cost_usd"] for s in all_summaries.values())
        macro = sum(s["macro_f1"] for s in all_summaries.values()) / len(all_summaries)
        trunc = [d for d, s in all_summaries.items() if s.get("coverage") == "truncated"]
        print(f"\n  domains={len(all_summaries)}  macro_F1={macro:.4f}  total_cost=${tot:.2f}")
        if trunc:
            print(f"  ⚠ truncated (do not report as complete): {', '.join(trunc)}")


if __name__ == "__main__":
    main()
