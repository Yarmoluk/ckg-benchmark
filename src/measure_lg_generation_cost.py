"""
Measure precise token consumption for /learning-graph-generator sessions.

Reads:
  - ~/.claude/activity-logs/skill-usage.jsonl  (skill start/end events)
  - ~/.claude/projects/<slug>/<session>.jsonl   (full session transcripts)
  - <project>/docs/data/learning-graph.csv OR
    <project>/learning-graph.csv               (resulting graph, for concept count)

For each session where /learning-graph-generator was invoked, sums the token
usage of every assistant message from the skill-start timestamp forward,
stopping at the earliest of: (a) the next skill-start event in the same
session for a different skill, (b) end of the transcript file.

Produces (written into paper/figures/ relative to the repo root):
  - paper/figures/lg_generation_cost.csv       (per-session rows)
  - paper/figures/lg_generation_cost_table.tex (LaTeX-formatted table body
    included by paper/sections/09b-learning-graph-economics.tex)

Run from anywhere:
  python src/measure_lg_generation_cost.py

Pricing (USD per million tokens, as of 2026-04):
  Claude Opus 4.5 / 4.6:   $15 input, $75 output, $1.50 cache read, $18.75 cache write
  Claude Sonnet 4.5 / 4.6: $3  input, $15 output, $0.30 cache read, $3.75  cache write
  Claude Haiku 4.5:        $0.80 input, $4 output, $0.08 cache read, $1.00 cache write
"""
import csv
import json
import os
from datetime import datetime
from pathlib import Path

HOME = Path.home()
ACTIVITY_LOG = HOME / ".claude" / "activity-logs" / "skill-usage.jsonl"
PROJECTS_DIR = HOME / ".claude" / "projects"
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = REPO_ROOT / "paper" / "figures"

# Pricing in USD per 1M tokens. Keyed by model-family substring match.
PRICING = {
    "opus":   {"in": 15.0,  "out": 75.0, "cache_read": 1.50, "cache_write": 18.75},
    "sonnet": {"in": 3.0,   "out": 15.0, "cache_read": 0.30, "cache_write": 3.75},
    "haiku":  {"in": 0.80,  "out": 4.0,  "cache_read": 0.08, "cache_write": 1.00},
}


def pricing_for(model_id: str) -> dict:
    if not model_id:
        return PRICING["sonnet"]
    m = model_id.lower()
    for key in PRICING:
        if key in m:
            return PRICING[key]
    return PRICING["sonnet"]


def project_slug(project_path: str) -> str:
    # Claude Code uses the full path with slashes replaced by dashes, keeping
    # the leading dash from the absolute path (e.g. "/Users/dan/..." becomes
    # "-Users-dan-...").
    return project_path.replace("/", "-")


def load_skill_events():
    events = []
    with open(ACTIVITY_LOG) as f:
        for line in f:
            events.append(json.loads(line))
    return events


def next_skill_start_in_session(events, session_id, after_epoch):
    """Find the next skill-start event in the same session AFTER the given epoch,
    for any skill (used to bracket the end of the generation window)."""
    best = None
    for e in events:
        if e.get("session") != session_id or e.get("event") != "start":
            continue
        epoch = int(e.get("epoch", 0))
        if epoch > after_epoch:
            if best is None or epoch < int(best.get("epoch", 0)):
                best = e
    return best


def iter_assistant_messages(transcript_path: Path):
    """Yield (timestamp_epoch, model, usage_dict) from assistant messages."""
    with open(transcript_path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            ts = d.get("timestamp", "")
            try:
                epoch = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
            except Exception:
                continue
            msg = d.get("message", {})
            if not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            if not usage:
                continue
            model = msg.get("model", "")
            yield epoch, model, usage


def count_concepts(project_path: str) -> int | None:
    project = Path(project_path)
    for candidate in [
        project / "docs" / "learning-graph" / "learning-graph.csv",
        project / "docs" / "data" / "learning-graph.csv",
        project / "learning-graph.csv",
        project / "data" / "learning-graph.csv",
    ]:
        if candidate.exists():
            with open(candidate) as f:
                return max(0, sum(1 for _ in f) - 1)
    return None


def measure():
    events = load_skill_events()
    lg_starts = [
        e for e in events
        if e.get("skill") == "learning-graph-generator" and e.get("event") == "start"
    ]

    rows = []
    for start in lg_starts:
        session_id = start["session"]
        project = start["project"]
        start_epoch = int(start["epoch"])
        slug = project_slug(project)
        transcript = PROJECTS_DIR / slug / f"{session_id}.jsonl"
        if not transcript.exists():
            rows.append({
                "project": project, "session": session_id,
                "start": start["timestamp"], "status": "no_transcript",
            })
            continue

        next_start = next_skill_start_in_session(events, session_id, start_epoch)
        end_epoch = int(next_start["epoch"]) if next_start else float("inf")

        tokens = {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
        cost = 0.0
        models_seen = set()
        n_messages = 0

        for epoch, model, usage in iter_assistant_messages(transcript):
            if epoch < start_epoch or epoch > end_epoch:
                continue
            n_messages += 1
            price = pricing_for(model)
            if model:
                models_seen.add(model)

            in_tok = int(usage.get("input_tokens", 0) or 0)
            out_tok = int(usage.get("output_tokens", 0) or 0)
            cr_tok = int(usage.get("cache_read_input_tokens", 0) or 0)
            cw_tok = int(usage.get("cache_creation_input_tokens", 0) or 0)

            tokens["in"] += in_tok
            tokens["out"] += out_tok
            tokens["cache_read"] += cr_tok
            tokens["cache_write"] += cw_tok

            cost += (in_tok * price["in"] +
                     out_tok * price["out"] +
                     cr_tok * price["cache_read"] +
                     cw_tok * price["cache_write"]) / 1_000_000

        rows.append({
            "project": project,
            "session": session_id,
            "start": start["timestamp"],
            "status": "measured" if n_messages else "empty_window",
            "messages": n_messages,
            "models": ",".join(sorted(models_seen)) or "unknown",
            "concepts": count_concepts(project),
            **tokens,
            "total_tokens": sum(tokens.values()),
            "cost_usd": round(cost, 4),
        })
    return rows


def write_csv(rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "lg_generation_cost.csv"
    fields = ["project", "session", "start", "status", "messages", "models",
              "concepts", "in", "out", "cache_read", "cache_write",
              "total_tokens", "cost_usd"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"Wrote {out}")


def write_latex_table(rows):
    usable = [r for r in rows
              if r.get("status") == "measured"
              and r.get("concepts")
              and r.get("cost_usd", 0) > 0.05]
    usable.sort(key=lambda r: r["concepts"])

    lines = []
    lines.append("% AUTO-GENERATED by paper/figures/measure_lg_generation_cost.py")
    lines.append("% Do not edit by hand; re-run the script to refresh.")
    lines.append(r"\begin{tabular}{lrrrrr}")
    lines.append(r"\toprule")
    lines.append(r"Domain & Concepts & Input & Output & Cached & Cost (USD) \\")
    lines.append(r" & & (k tok) & (k tok) & (k tok) & \\")
    lines.append(r"\midrule")

    total_c = 0
    total_in = 0
    total_out = 0
    total_cache = 0
    total_cost = 0.0
    for r in usable:
        domain = os.path.basename(r["project"])
        cached = r["cache_read"] + r["cache_write"]
        lines.append(
            f"{domain.replace('_','-')} & "
            f"{r['concepts']} & "
            f"{r['in']/1000:.1f} & "
            f"{r['out']/1000:.1f} & "
            f"{cached/1000:.1f} & "
            f"\\${r['cost_usd']:.2f} \\\\"
        )
        total_c += r["concepts"]
        total_in += r["in"]
        total_out += r["out"]
        total_cache += cached
        total_cost += r["cost_usd"]

    if usable:
        lines.append(r"\midrule")
        mean_c = total_c / len(usable)
        lines.append(
            f"\\textbf{{Mean}} & "
            f"{mean_c:.0f} & "
            f"{total_in/len(usable)/1000:.1f} & "
            f"{total_out/len(usable)/1000:.1f} & "
            f"{total_cache/len(usable)/1000:.1f} & "
            f"\\${total_cost/len(usable):.2f} \\\\"
        )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    out = OUTPUT_DIR / "lg_generation_cost_table.tex"
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out}  ({len(usable)} usable rows)")


def summarize(rows):
    measured = [r for r in rows if r["status"] == "measured"]
    print()
    print(f"Total events:    {len(rows)}")
    print(f"  measured:      {len(measured)}")
    print(f"  no_transcript: {sum(1 for r in rows if r['status']=='no_transcript')}")
    print(f"  empty_window:  {sum(1 for r in rows if r['status']=='empty_window')}")
    if measured:
        with_concepts = [r for r in measured if r.get("concepts")]
        print(f"\nMeasured sessions with concept counts: {len(with_concepts)}")
        for r in sorted(with_concepts, key=lambda x: x["concepts"] or 0):
            print(f"  {os.path.basename(r['project']):<30} "
                  f"concepts={r['concepts']:>4} "
                  f"total_tok={r['total_tokens']:>9,} "
                  f"cost=${r['cost_usd']:>6.2f} "
                  f"msgs={r['messages']}")


def main():
    rows = measure()
    write_csv(rows)
    write_latex_table(rows)
    summarize(rows)


if __name__ == "__main__":
    main()
