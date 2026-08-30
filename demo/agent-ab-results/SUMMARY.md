# A/B agent experiment: hardware_security_ckg.md

Question: How does a hardware attacker get modified firmware to run past secure boot? Be specific about the attack path, lab tool used, and the countermeasure.

Machine: Daniels-Mac-mini-2 (`964393bf-c38d-460b-a542-a67931548e75`)
When: 2026-08-30 ~08:10–08:25 CT (13:10–13:25 UTC)
CLIs: Claude Code 2.1.250 (`/Users/danielyarmoluk/.local/bin/claude`); Codex 0.151.0 (`/Users/danielyarmoluk/.local/bin/codex`)

CKG file copied (not moved) into `/tmp/ab-agent/claude-ckg/` and `/tmp/ab-agent/codex-ckg/` only. Raw arms had empty dirs (no CKG).

## Auth / flag notes (important)

`--bare` **failed auth** as specified retry path:

- Exact error (Arm B `--bare`): `Failed to authenticate. API Error: 401 API key is invalid.`
- Arm A `--bare`: hung 180s after `Warning: no stdin data received in 3s...` then `[TIMEOUT after 180s]` (exit 124). No answer body.
- `ANTHROPIC_API_KEY` was set (`sk-ant-…`, len 108) but **invalid**. Without `--bare`, Claude warns that the env key takes precedence over claude.ai login.
- Successful Claude arms: **`--bare` dropped**, `--disable-slash-commands` kept, `ANTHROPIC_API_KEY` **unset for the process** so OAuth/claude.ai login worked. Confirmed with a 17s `PING_OK` probe.
- **Confound:** `~/.claude/CLAUDE.md` exists (Graphify.md global rules, CKG-related). cwd was `/tmp/ab-agent/...` so project CLAUDE.md was unlikely. Session JSONL for Arm B shows `hook_success` / `hook_additional_context` because `--bare` was off (hooks ran).
- Arm B also hung at 180s with invalid key still set (connectors warning only). Successful Arm B added `--permission-mode acceptEdits` so Read was not blocked on a prompt. Did **not** use `--dangerously-skip-permissions`.
- Codex `exec --skip-git-repo-check --sandbox read-only --color never` worked as specified. `--color never` only (not a behavior change). Codex also printed `Reading additional input from stdin...` even with stdin closed.

## Arm A — Claude no CKG

- cwd: `/tmp/ab-agent/claude-raw`
- Successful command: `claude -p --disable-slash-commands --output-format text` + expert/question prompt. Env: `ANTHROPIC_API_KEY` unset. stdin DEVNULL.
- Failed first command: `claude -p --bare --disable-slash-commands --output-format text` → timeout 180.017s, exit 124.
- Elapsed: **20.55 s**
- Exit code: **0**
- Read CKG?: **No** (file not present; no Read tool). Session dir: `~/.claude/projects/-private-tmp-ab-agent-claude-raw/`
- Answer style: improvised expert answer. Path = voltage/clock glitch of `verify_signature()` branch; lab = ChipWhisperer (also Riscure/J-Link/CH341A); countermeasure = redundant checks, jitter, glitch detectors, OTP key hash. **No node IDs.**

## Arm B — Claude with CKG (agent Read)

- cwd: `/tmp/ab-agent/claude-ckg` (contains `hardware_security_ckg.md`)
- Successful command: `claude -p --disable-slash-commands --add-dir /tmp/ab-agent/claude-ckg --allowedTools Read --permission-mode acceptEdits --output-format text` + prompt instructing FIRST Read `hardware_security_ckg.md`, then traverse declared edges and cite node IDs. Env: `ANTHROPIC_API_KEY` unset.
- Failed `--bare` command: same plus `--bare`, `--allowedTools Read`, no permission-mode → 176.721s, exit 1, `401 API key is invalid.`
- Elapsed: **26.033 s**
- Exit code: **0**
- Read CKG?: **Yes.** `--output-format text` does not print tool JSON, but session `284b1daa-0f53-47dd-84c9-be06fcc1e740.jsonl` line 13 is `tool_use` name=`Read` `file_path=/private/tmp/ab-agent/claude-ckg/hardware_security_ckg.md`; line 14 `tool_result` id `toolu_01SjDasujDhy9ULv5sj7M3TA` preview starts `## META domain: hardware-security ... nodes: 12`.
- Answer style: **node IDs**. Path FI1 → (LAB4-driven FI2/FI3) → BR14 → BR15 → GA4 → GA5. Lab LAB4 ChipWhisperer. Defense HHC7 → HHC8 blocks BR14; HHC9 complementary. Quotes KEY PATHS wording.

## Arm C — Codex no CKG

- cwd: `/tmp/ab-agent/codex-raw` (empty besides prompt)
- Command: `codex exec --skip-git-repo-check --sandbox read-only --color never` + expert/question prompt.
- Elapsed: **17.11 s**
- Exit code: **0**
- Model logged: `gpt-5.6-sol` session `01a052d8-3317-7102-934f-a4e4b08eced6`
- Read CKG?: **No** (file not in cwd; transcript shows user prompt then answer, no file exec).
- Answer style: improvised. Voltage/clock FI, ChipWhisperer or Riscure EM-FI / laser; also SPI swap, JTAG. Countermeasure: double-verify, sensors, debug lock, OTP keys. **No node IDs.** ~4996 tokens.

## Arm D — Codex with CKG

- cwd: `/tmp/ab-agent/codex-ckg` (contains `hardware_security_ckg.md`)
- Command: `codex exec --skip-git-repo-check --sandbox read-only --color never` + prompt instructing FIRST read the file with file tools, then traverse declared edges and cite node IDs.
- Elapsed: **13.098 s**
- Exit code: **0**
- Model logged: `gpt-5.6-sol` session `01a052d8-8c6e-7ff2-bb01-fbb92aecf943`
- Read CKG?: **Yes — explicit in stdout.** `exec /bin/zsh -lc "sed -n '1,240p' hardware_security_ckg.md" in /private/tmp/ab-agent/codex-ckg` succeeded and dumped the full graph (META/CSV/KEY PATHS/SOURCES).
- Answer style: **node IDs**. FI1 via FI2/FI3 → BR15 and BR14 → GA4. Lab LAB4. Countermeasure HHC7 enforces HHC8 blocks BR14. Compact; does not mention GA5/HHC9. ~10277 tokens.

## Contrast (node IDs vs improvised)

Raw arms (A, C) both independently invent the same industry-standard story (ChipWhisperer voltage/clock glitch of signature check) **without** FI1/BR14/GA4/LAB4/HHC8. They add extra tools (Riscure, J-Link, laser, SPI programmer) not required by the graph.

CKG arms (B, D) both **Read the file** then stay on declared edges: FI1/FI2/FI3, BR14/BR15, GA4, LAB4, HHC7/HHC8. Claude (B) is more complete (GA5, HHC9, LAB5 caveat). Codex (D) is a short traversal of KEY PATHS. Neither CKG arm needed to invent Riscure/laser.

Same factual core appears in all four (glitch → skip signature check → patched image; ChipWhisperer; secure-boot enforcement). The CKG condition changes **citation discipline and path specificity**, not the high-level mechanism.
