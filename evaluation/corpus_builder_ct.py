"""
Track 3 Corpus Builder — ClinicalTrials.gov GLP-1 Corpus

Pulls all GLP-1 agonist trials from ClinicalTrials.gov API v2.
Extracts full text fields, saves corpus, and reports token count.

This corpus is the SOURCE from which the GLP-1 CKG (125 nodes, ~15KB) was derived.
The compression ratio demonstrates CKG's core value proposition.

Usage:
    python evaluation/corpus_builder_ct.py
    python evaluation/corpus_builder_ct.py --max-trials 500

Output:
    results/track3/ct_glp1_corpus.json   — structured trial data
    results/track3/ct_glp1_corpus.txt    — flat text for token counting
    results/track3/ct_glp1_summary.json  — token counts, compression stats
"""

import json
import time
import argparse
import requests
from pathlib import Path

try:
    import tiktoken
    TOKENIZER = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(TOKENIZER.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        return len(text.split()) * 4 // 3  # rough estimate

OUTPUT_DIR = Path("results/track3")
CT_API_BASE = "https://clinicaltrials.gov/api/v2/studies"

SEARCH_TERMS = [
    "semaglutide",
    "tirzepatide",
    "liraglutide",
    "dulaglutide",
    "exenatide",
    "GLP-1 receptor agonist",
]

def fetch_trials(search_term: str, max_trials: int = 1000) -> list[dict]:
    trials = []
    next_page = None

    while len(trials) < max_trials:
        params = {
            "query.intr": search_term,
            "pageSize": 100,
            "format": "json",
        }
        if next_page:
            params["pageToken"] = next_page

        try:
            resp = requests.get(CT_API_BASE, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  Error fetching '{search_term}': {e}")
            break

        studies = data.get("studies", [])
        if not studies:
            break

        for study in studies:
            proto = study.get("protocolSection", {})
            id_mod = proto.get("identificationModule", {})
            desc_mod = proto.get("descriptionModule", {})
            elig_mod = proto.get("eligibilityModule", {})
            outcomes_mod = proto.get("outcomesModule", {})
            arms_mod = proto.get("armsInterventionsModule", {})
            status_mod = proto.get("statusModule", {})
            design_mod = proto.get("designModule", {})
            sponsor_mod = proto.get("sponsorCollaboratorsModule", {})

            primary_outcomes = " ".join(
                o.get("description", o.get("measure", ""))
                for o in outcomes_mod.get("primaryOutcomes", [])
            )
            secondary_outcomes = " ".join(
                o.get("description", o.get("measure", ""))
                for o in outcomes_mod.get("secondaryOutcomes", [])
            )
            interventions = " ".join(
                f"{i.get('name', '')}: {i.get('description', '')}"
                for i in arms_mod.get("interventions", [])
            )

            trials.append({
                "nct_id": id_mod.get("nctId", ""),
                "title": id_mod.get("briefTitle", ""),
                "brief_summary": desc_mod.get("briefSummary", ""),
                "detailed_description": desc_mod.get("detailedDescription", ""),
                "eligibility_criteria": elig_mod.get("eligibilityCriteria", ""),
                "primary_outcomes": primary_outcomes,
                "secondary_outcomes": secondary_outcomes,
                "interventions": interventions,
                "conditions": ", ".join(
                    study.get("protocolSection", {})
                    .get("conditionsModule", {})
                    .get("conditions", [])
                ),
                "phase": ", ".join(design_mod.get("phases", [])),
                "status": status_mod.get("overallStatus", ""),
                "enrollment": design_mod.get("enrollmentInfo", {}).get("count", ""),
                "sponsor": sponsor_mod.get("leadSponsor", {}).get("name", ""),
                "search_term": search_term,
            })

        next_page = data.get("nextPageToken")
        print(f"  '{search_term}': {len(trials)} trials fetched...")

        if not next_page or len(studies) < 100:
            break

        time.sleep(0.3)

    return trials


def trial_to_text(trial: dict) -> str:
    parts = [
        f"TRIAL: {trial['nct_id']} | {trial['title']}",
        f"Phase: {trial['phase']} | Status: {trial['status']} | Enrollment: {trial['enrollment']}",
        f"Sponsor: {trial['sponsor']}",
        f"Conditions: {trial['conditions']}",
    ]
    if trial["brief_summary"]:
        parts.append(f"SUMMARY:\n{trial['brief_summary']}")
    if trial["detailed_description"]:
        parts.append(f"DETAILED DESCRIPTION:\n{trial['detailed_description']}")
    if trial["eligibility_criteria"]:
        parts.append(f"ELIGIBILITY:\n{trial['eligibility_criteria']}")
    if trial["interventions"]:
        parts.append(f"INTERVENTIONS:\n{trial['interventions']}")
    if trial["primary_outcomes"]:
        parts.append(f"PRIMARY OUTCOMES:\n{trial['primary_outcomes']}")
    if trial["secondary_outcomes"]:
        parts.append(f"SECONDARY OUTCOMES:\n{trial['secondary_outcomes']}")
    return "\n".join(parts)


def main(max_trials: int = 1000):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_trials = {}
    for term in SEARCH_TERMS:
        print(f"\nFetching: {term}")
        trials = fetch_trials(term, max_trials=max_trials)
        for t in trials:
            all_trials[t["nct_id"]] = t  # deduplicate by NCT ID

    trials = list(all_trials.values())
    print(f"\nTotal unique trials: {len(trials)}")

    # Save structured JSON
    json_path = OUTPUT_DIR / "ct_glp1_corpus.json"
    with open(json_path, "w") as f:
        json.dump(trials, f, indent=2)
    print(f"Saved: {json_path}")

    # Build flat text corpus
    corpus_lines = []
    for trial in trials:
        corpus_lines.append(trial_to_text(trial))
        corpus_lines.append("\n" + "="*80 + "\n")
    corpus_text = "\n".join(corpus_lines)

    txt_path = OUTPUT_DIR / "ct_glp1_corpus.txt"
    with open(txt_path, "w") as f:
        f.write(corpus_text)
    print(f"Saved: {txt_path}")

    # Token counts
    total_tokens = count_tokens(corpus_text)
    char_count = len(corpus_text)
    file_size_kb = txt_path.stat().st_size / 1024

    # CKG reference stats (from existing benchmark)
    ckg_path = Path("benchmark/domains/glp1-obesity/learning-graph.csv")
    ckg_nodes = 0
    ckg_text = ""
    if ckg_path.exists():
        with open(ckg_path) as f:
            rows = f.readlines()
            ckg_nodes = len(rows) - 1
            ckg_text = "".join(rows)
    ckg_tokens = count_tokens(ckg_text) if ckg_text else 1500  # ~15KB estimate
    ckg_size_kb = ckg_path.stat().st_size / 1024 if ckg_path.exists() else 15.0

    compression_ratio = total_tokens / ckg_tokens if ckg_tokens > 0 else 0

    # Cost projections (no LLM calls needed)
    # Claude claude-sonnet-4-6: $3/1M input, $15/1M output
    # Per query: send full corpus + query + get answer
    output_tokens_per_query = 200  # typical answer length
    longctx_cost_per_query = (total_tokens * 3.0 / 1_000_000) + (output_tokens_per_query * 15.0 / 1_000_000)
    longctx_cost_170 = longctx_cost_per_query * 170

    # CKG actual cost from benchmark (Track 2 result)
    ckg_avg_tokens = 350  # from existing benchmark results
    ckg_cost_per_query = (ckg_avg_tokens * 0.80 / 1_000_000) + (output_tokens_per_query * 4.0 / 1_000_000)  # Haiku pricing
    ckg_cost_170 = ckg_cost_per_query * 170

    cost_ratio = longctx_cost_per_query / ckg_cost_per_query if ckg_cost_per_query > 0 else 0

    summary = {
        "corpus": {
            "source": "ClinicalTrials.gov API v2",
            "search_terms": SEARCH_TERMS,
            "unique_trials": len(trials),
            "total_tokens": total_tokens,
            "total_chars": char_count,
            "file_size_kb": round(file_size_kb, 1),
            "file_size_mb": round(file_size_kb / 1024, 2),
        },
        "ckg": {
            "source": "benchmark/domains/glp1-obesity/learning-graph.csv",
            "nodes": ckg_nodes,
            "tokens": ckg_tokens,
            "file_size_kb": round(ckg_size_kb, 1),
            "macro_f1": 0.5298,  # from existing Track 2 benchmark
            "bert_f1": 0.857,
            "cpca_usd": 0.000506,
        },
        "compression": {
            "token_ratio": round(compression_ratio, 1),
            "size_ratio": round(file_size_kb / ckg_size_kb, 1),
        },
        "cost_projection": {
            "longctx_tokens_per_query": total_tokens + output_tokens_per_query,
            "longctx_cost_per_query_usd": round(longctx_cost_per_query, 4),
            "longctx_cost_170_queries_usd": round(longctx_cost_170, 2),
            "ckg_avg_tokens_per_query": ckg_avg_tokens,
            "ckg_cost_per_query_usd": round(ckg_cost_per_query, 6),
            "ckg_cost_170_queries_usd": round(ckg_cost_170, 4),
            "cost_reduction_ratio": round(cost_ratio, 0),
            "note": "Long-context cost uses Claude claude-sonnet-4-6 input pricing ($3/1M tokens). CKG uses Claude Haiku pricing ($0.80/1M input). Projections only — long-context LLM run not executed.",
        },
    }

    summary_path = OUTPUT_DIR / "ct_glp1_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {summary_path}")

    print("\n" + "="*60)
    print("TRACK 3 CORPUS SUMMARY")
    print("="*60)
    print(f"Trials pulled:       {len(trials):,}")
    print(f"Corpus tokens:       {total_tokens:,}")
    print(f"Corpus size:         {file_size_kb:.1f} KB ({file_size_kb/1024:.2f} MB)")
    print(f"CKG nodes:           {ckg_nodes}")
    print(f"CKG tokens:          {ckg_tokens:,}")
    print(f"Token compression:   {compression_ratio:.0f}×")
    print(f"CKG F1 (benchmark):  0.5298")
    print(f"")
    print(f"COST PROJECTION (170 queries):")
    print(f"  Long-context:      ${longctx_cost_170:,.2f}")
    print(f"  CKG (actual):      ${ckg_cost_170:.4f}")
    print(f"  Cost ratio:        {cost_ratio:,.0f}×")
    print("="*60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-trials", type=int, default=1000)
    args = parser.parse_args()
    main(args.max_trials)
