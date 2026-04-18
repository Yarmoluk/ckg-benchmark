# Claude Desktop App — Idle CPU Bug

**Date observed:** 2026-04-17
**Reporter:** Dan McCreary
**Host:** macOS (Darwin 25.3.0)
**Claude Desktop version:** 1.3109.0
**Claude Code CLI version:** 2.1.111

## Symptom

Activity Monitor shows the Claude **Desktop** app consuming extremely high CPU while the user is idle (not typing, no active generation). Initial suspicion was that Claude Code CLI was the culprit, but `ps aux | grep -i claude` shows the Electron desktop app is responsible.

## Evidence

Snapshot of `ps aux | grep -i claude` at time of report:

| PID   | Process                           | %CPU  | Accumulated CPU | Started |
|-------|-----------------------------------|-------|-----------------|---------|
| 24357 | Claude Helper (**GPU process**)   | 59.4% | 67:38.95        | 8:19 PM |
| 24375 | Claude Helper (**Renderer**)      | 47.2% | 69:22.45        | 8:19 PM |
| 24318 | Claude (main Electron process)    | 6.5%  | 40:34.16        | 8:19 PM |

Three Electron processes together burning **~113% CPU while idle**.

Meanwhile, 8 concurrent `claude` CLI sessions were running, each using 0.0–2.9% CPU with 5–6 min accumulated CPU time — well-behaved and not the source of the load.

## Diagnosis

The GPU-process + Renderer pinned at ~50% CPU each while idle is the classic Electron/Chromium symptom of:
- a stuck `requestAnimationFrame` loop,
- a wedged WebGL/canvas compositor context, or
- a runaway animation in the Claude Desktop UI.

This is a **desktop-app bug**, not a Claude Code CLI bug.

## Mitigation

1. **Quit and relaunch the Claude Desktop app.** A restart typically clears the wedged GPU context. If CPU returns to near-zero after relaunch, this confirms the diagnosis.
2. If it recurs quickly, try disabling hardware acceleration in the desktop-app settings, or check whether an open artifact/canvas view is animating.
3. Unrelated housekeeping: clean up stale CLI sessions left running from earlier in the day (cheap individually but they accumulate).

## Upstream issue references (Claude Code CLI — not this bug, but related idle-CPU discussions)

- https://github.com/anthropics/claude-code/issues/19393 — High idle CPU v2.1.12
- https://github.com/anthropics/claude-code/issues/18280 — Memory allocation thrashing idle CPU
- https://github.com/anthropics/claude-code/issues/10493 — Busy-wait event loop
- https://github.com/anthropics/claude-code/issues/11122 — Multiple processes accumulate

## Follow-up

If the symptom recurs after a clean desktop-app restart, file a bug report against the **Claude Desktop app** (not Claude Code) with the `ps aux` snapshot and a description of what was on screen at the time (artifact view, computer-use session, etc.).
