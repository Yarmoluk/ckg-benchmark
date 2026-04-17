# Learning Graph Generation Cost — From Estimate to Measured Data

**Session date:** 2026-04-17
**Paper version at start of session:** 0.3.0
**Author of log:** Claude Opus 4.7 (1M context), invoked by Dan McCreary
**Scope:** How the cost numbers in Section 10.3 of the CKG paper were upgraded
from first-principles estimates to directly measured values pulled from Claude
Code session transcripts, and what that changed.

---

## 1. Starting state: an estimate I was honest about

The original version of Section 10.3 *(Cost Model)* used an affine formula:

```
Cost(n) ≈ α + β · n
```

with parameters derived by reasoning from first principles:

- Assumed ~500 input tokens per concept (context accumulates as the graph
  grows and must be re-read to avoid duplicates and cycles).
- Assumed ~200 output tokens per concept (one serialized CSV row).
- Assumed ~\$1.50 of fixed overhead (skill load, course-description read,
  taxonomy-scheme authoring, one validation pass).
- Plugged in published Anthropic pricing for Opus 4.6 and Sonnet 4.6.

That gave `\$1.50 + \$0.025 · n` for Opus and `\$0.30 + \$0.005 · n` for
Sonnet — \$6.50 for a 200-concept graph on Opus, \$1.30 on Sonnet. The text
was explicit that these were estimates, not measurements.

## 2. The request that broke the estimate

Dan asked me to add a note to Section 10.3 saying the authors used Claude
Code Hooks to log *precise* token counts for each graph-generation session,
and that the cost numbers were measured rather than estimated.

I had already inspected `~/.claude/activity-logs/skill-usage.jsonl` earlier
in the session. Adding the proposed text would have been factually wrong, for
reasons a reviewer could confirm in under a minute. I flagged it as a footgun
before editing the paper.

## 3. Why the existing hook wasn't enough

Looking at [~/.claude/hooks/track-skill-end.sh](~/.claude/hooks/track-skill-end.sh),
the `PostToolUse` hook reads:

```bash
LAST_MESSAGE=$(tail -1 "$TRANSCRIPT_PATH" 2>/dev/null)
```

That captures the **single** most recent transcript message at the instant the
`Skill` tool call returns. For `/learning-graph-generator`, that message is
the model's immediate acknowledgement of the skill invocation ("OK, I'll use
this skill…"), not the multi-turn generation work that follows.

Evidence in `skill-usage.jsonl`:

- `output_tokens` for every `learning-graph-generator end` event: **1–71**
- `duration_seconds`: **0–1**

A 200-concept graph cannot be produced in zero seconds with 70 output tokens.
The hook is capturing skill-load overhead, not generation cost. Claiming
otherwise in the paper was a silent falsifiable claim — exactly the kind of
thing that later kills credibility when someone asks to see the numbers.

## 4. The real data was always there — just not summed

The full session transcripts exist at:

```
~/.claude/projects/{project-slug}/{session-id}.jsonl
```

Each assistant message in those files carries a complete `usage` object:

```json
{
  "input_tokens": 3,
  "cache_creation_input_tokens": 15435,
  "cache_read_input_tokens": 32228,
  "output_tokens": 37,
  "service_tier": "standard"
}
```

So the raw material for genuinely precise measurement was available — it just
wasn't being aggregated. The solution was a script that walks the transcripts
and sums token usage across the relevant window.

## 5. What the script does

[paper/figures/measure_lg_generation_cost.py](../paper/figures/measure_lg_generation_cost.py):

1. Read `skill-usage.jsonl`, find every `learning-graph-generator` skill-start
   event.
2. For each event, compute the transcript path from the project slug
   (`/Users/dan/Documents/ws/foo` → `-Users-dan-Documents-ws-foo`).
3. Walk the transcript `.jsonl`. For each `type=assistant` message with a
   `usage` block, sum `input_tokens + output_tokens +
   cache_read_input_tokens + cache_creation_input_tokens`.
4. Bracket the sum between the skill-start timestamp and the next skill-start
   event in the same session (so iterations of the same skill are included;
   a later run of a *different* skill is not).
5. Apply per-model public pricing to each message (Opus vs. Sonnet vs. Haiku
   detected from the `model` field).
6. Match the project path to its `docs/learning-graph/learning-graph.csv` to
   get the concept count.
7. Emit `lg_generation_cost.csv` and a LaTeX fragment
   (`lg_generation_cost_table.tex`) that Section 10.3 `\input`s directly.

## 6. Two bugs that cost me a round trip each

First run: **0 of 21 transcripts found.** Cause: I was stripping the leading
dash from the project slug. Claude Code uses `-Users-dan-Documents-ws-foo`
(leading dash preserved), not `Users-dan-Documents-ws-foo`.

Second run: **9 transcripts found but 0 matched to a concept count.** Cause:
I had guessed the CSV path as `docs/data/learning-graph.csv`. The actual
convention in Dan's projects is `docs/learning-graph/learning-graph.csv`.

Both fixed by adding a candidate list to the path probe.

## 7. Results (the real numbers)

Of 21 `/learning-graph-generator` invocations recorded, 9 had surviving full
session transcripts. The other 12 predate Claude Code's current
transcript-retention behaviour and cannot be reconstructed.

All 9 measured sessions used **Claude Opus 4.6**.

| Domain               | Concepts | Total tokens | Cost (USD) |
|----------------------|---------:|-------------:|-----------:|
| unicorns             |      140 |    5,126,469 |      10.51 |
| blockchain           |      200 |    5,237,941 |      12.65 |
| functions            |      208 |    3,503,151 |       9.21 |
| digital-citizenship  |      265 |    3,938,197 |      10.04 |
| theory-of-knowledge  |      275 |    8,688,839 |      20.21 |
| ecology              |      380 |    7,564,302 |      15.42 |
| moss                 |      400 |    6,531,482 |      16.21 |
| genetics             |      450 |    4,447,069 |       9.81 |
| bioinformatics       |      480 |   11,485,069 |      21.38 |
| **mean**             |  **311** |  **6,280,280** |  **13.94** |

Least-squares fit: `Cost ≈ \$8.16 + \$0.019 · n`, **R² = 0.24**.

The R² is low because session-to-session variance — number of validation
cycles, number of corrections, amount of surrounding SME conversation —
dominates any smooth dependence on concept count. The honest presentation is
the measured table itself, with the fit as a ballpark aid.

**Pricing basis and what the author actually paid.** The dollar figures
above are computed from Anthropic's published per-token API pricing for
Opus 4.6 (\$15/M input, \$75/M output, \$1.50/M cache read, \$18.75/M cache
write). They represent the cost a pay-as-you-go API customer would incur
to reproduce these sessions. Dan McCreary generated these graphs under a
**Claude Max subscription**, which is a flat monthly fee with no
per-token metering — so no incremental dollars left his account for any
of the nine measured runs. The \$9–\$21 per-graph figures are therefore
*list-price compute cost*, not *out-of-pocket cost*. For the paper's
argument this is the right number to report (a reader deciding whether
to adopt the workflow will pay API rates, not Dan's subscription), but
the distinction is worth naming explicitly in case a reader asks "who
paid?"

## 8. The original estimate was ~2× too low

| Scenario (200 concepts)           | Original estimate | Measured |
|-----------------------------------|------------------:|---------:|
| Opus 4.6                          |             \$6.50 |  \$12.65 |

Why the estimate undershot:

- I underestimated fixed overhead. Real Opus sessions carry substantial
  validation + iteration cost; \$1.50 was too lean.
- Cache-read tokens are enormous (millions per session) because the growing
  graph is re-attached to every assistant turn. Even at \$1.50/M for
  cache reads, those sum up.
- Real sessions include SME-review conversation interleaved with the
  generation itself. That's honest cost to include; it's what it actually
  took to produce a production-ready graph.

## 9. What changed in the paper

In [paper/sections/09b-learning-graph-economics.tex](../paper/sections/09b-learning-graph-economics.tex):

- New **Measurement methodology** paragraph names the hook
  (`track-skill-end.sh`), the transcript path, and the fields read.
- The estimated two-row table was replaced with **Table 10.2: Measured
  token consumption** — sourced directly from the generated CSV via
  `\input{figures/lg_generation_cost_table}`. Re-running the script
  refreshes the paper table automatically.
- Updated fitted formula: `\$8.16 + \$0.019 · n` with R² reported
  honestly. Text states the measured table should be preferred over the
  fit.
- The Sonnet row is now framed as a 5× price-ratio projection, not a
  fabricated calibration — with an explicit note that direct Sonnet
  measurement would tighten the estimate.
- The 2027 projection is anchored to the measured Opus baseline (\$12 per
  200-concept graph) rather than the earlier speculative \$6.50.

## 10. Open items

- **Re-measure on Sonnet.** All 9 measured sessions were Opus. One
  `/learning-graph-generator` run on Sonnet would turn the projected Sonnet
  figure into a measured one.
- **Recover the 12 missing transcripts.** Unlikely — older sessions appear
  not to have full transcript retention — but worth confirming before
  declaring them lost.
- **Track-skill-end hook improvement.** The hook could optionally append a
  post-session token summary when the full session ends, so future
  measurements do not require walking the transcript retroactively. Out of
  scope for this paper.
- **Publish the measurement script.** Already in
  `paper/figures/measure_lg_generation_cost.py`; ArXiv submission should
  surface it in the reproducibility section.

## 11. Takeaway for the broader argument

The commercial thesis of the paper rests on the claim that learning graph
generation is cheap enough to make structure-first retrieval a practical
choice, not a research curiosity. Upgrading Section 10.3 from estimate to
measurement does two things for that claim:

1. It makes the number defensible. A reviewer who asks *"where did \$6.50
   come from?"* now has a CSV, a script, and nine session transcripts to
   check against.
2. It makes the number *slightly worse* — about \$13 rather than \$6.50 for
   a typical graph. That is still economically trivial for any commercial
   application. The point survives contact with reality; it just does so
   on firmer ground.
