# `src/` — Source code that generates data used by the paper

This directory holds the scripts that turn raw logs and corpus files into the
numbers and tables published in `paper/`. Each script is self-contained and
writes its outputs into `paper/figures/` (or another location noted below) so
the paper build can `\input` the generated artifacts directly.

Run all scripts from the repository root:

```bash
python src/<script_name>.py
```

---

## `measure_lg_generation_cost.py`

**Purpose.** Produce the precisely-measured token and dollar figures reported
in Section 10.3 ("Cost Model") and Table 10.2
(`tab:lg-cost-measured`) of the paper.

**Why it exists.** An earlier draft of Section 10.3 reported an estimated
cost for generating a learning graph based on first-principles reasoning
(~\$6.50 for a 200-concept graph on Claude Opus 4.6). Reviewers would
reasonably ask *"where did that number come from?"* To replace the estimate
with a defensible measurement, this script walks every Claude Code session
in which the `/learning-graph-generator` skill was invoked, sums the token
usage across the full multi-turn generation window, applies the published
Anthropic API pricing, and emits a per-session table.

The measured numbers turned out to be roughly 2× the original estimate
(\~\$13 per 200-concept graph instead of \~\$6.50). The argument of the paper
survives — graph generation is still economically trivial — but it now rests
on data instead of speculation.

**Inputs (read).**

- `~/.claude/activity-logs/skill-usage.jsonl` — skill start/end events
  recorded by the `track-skill-end.sh` `PostToolUse` hook. Used to find
  every `/learning-graph-generator` invocation with its session ID,
  project path, and timestamp.
- `~/.claude/projects/{project-slug}/{session-id}.jsonl` — the full
  session transcript. Each assistant message carries a complete `usage`
  object (`input_tokens`, `output_tokens`, `cache_read_input_tokens`,
  `cache_creation_input_tokens`), which is what the measurement sums.
- `{project}/docs/learning-graph/learning-graph.csv` — the generated
  graph itself, used to recover the final concept count.

**Outputs (written, into `paper/figures/`).**

- `lg_generation_cost.csv` — one row per measured session with columns:
  `project, session, start, status, messages, models, concepts, in, out,
  cache_read, cache_write, total_tokens, cost_usd`. This is the raw
  artifact a reviewer can inspect.
- `lg_generation_cost_table.tex` — a LaTeX `tabular` body, `\input`'d
  directly by `paper/sections/09b-learning-graph-economics.tex`.
  Regenerating this file is how you refresh the paper's cost table; the
  paper's build picks up the change automatically.

**Measurement window.** For each skill-start event the script sums token
usage across assistant messages from the skill-start timestamp until the
next skill-start event in the same session (for any skill). This captures
iterations and corrections that stay within the generation task and
excludes unrelated work done later in the same session.

**Pricing basis.** Costs are computed from Anthropic's published
pay-as-you-go API prices keyed by the `model` field on each assistant
message (Opus vs. Sonnet vs. Haiku). The current measured sessions all
used Claude Opus 4.6; the Sonnet and Haiku rows exist in the pricing
table so the same script produces correct numbers for future re-runs
under cheaper models.

**Coverage.** Of 21 recorded `/learning-graph-generator` invocations, 9
had surviving full session transcripts at measurement time. The remaining
12 predate Claude Code's current transcript-retention behaviour and
cannot be reconstructed precisely; the script reports them with
`status = no_transcript` in the CSV.

**Subscription note.** The sessions used to calibrate this script were
generated under a Claude Max flat-rate subscription, so no incremental
per-token fees were paid for those specific runs. The costs reported are
API list prices — what a new reader adopting the workflow would be
charged. See the footnote under Table 10.2 in the paper.

---

## Adding new scripts here

Any new data-generation script should follow the same pattern:

1. Live in `src/` with a descriptive filename.
2. Locate inputs and outputs via paths rooted at the repo (the
   `REPO_ROOT = Path(__file__).resolve().parent.parent` idiom).
3. Write artifacts the paper consumes into `paper/figures/` so the paper
   build can `\input` them without needing a separate copy step.
4. Document itself in this README with the same four-bullet block —
   purpose, why it exists, inputs, outputs.
