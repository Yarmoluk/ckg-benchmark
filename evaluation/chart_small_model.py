"""
Gap-Closed Chart Generator

Reads summary JSON files from results/small_model/ and produces an interactive
HTML chart showing:
  1. Grouped bar: CKG F1 vs Baseline F1 per model (+ frontier ceiling line)
  2. Gap-Closed % table
  3. Token efficiency comparison

Output: results/small_model/gap_closed_chart.html

Usage:
  python3 evaluation/chart_small_model.py
  python3 evaluation/chart_small_model.py --open   # open in browser after generation
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path

RESULTS_DIR    = Path("results/small_model")
FRONTIER_CKG   = 0.4926
FRONTIER_RAG   = 0.1231
FRONTIER_TOKENS = 263.5

MODEL_LABELS = {
    "qwen3-8b":        "Qwen3 8B",
    "deepseek-r1-8b":  "DeepSeek-R1 8B",
    "phi4-mini":       "Phi-4 Mini (3.8B)",
    "mistral-latest":  "Mistral 7B",
    "mistral-7b":      "Mistral 7B",
    "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
}

MODEL_ORDER = [
    "phi4-mini", "mistral-latest", "mistral-7b",
    "qwen3-8b", "deepseek-r1-8b",
    "claude-haiku-4-5-20251001",
]


def load_summaries():
    data = {}
    for f in RESULTS_DIR.glob("*/summary_*.json"):
        try:
            s = json.loads(f.read_text())
        except Exception:
            continue
        slug = f.parent.name
        mode = s.get("mode", f.stem.replace("summary_",""))
        if slug not in data:
            data[slug] = {}
        data[slug][mode] = s
    return data


def build_chart(data: dict) -> str:
    # Sort models
    slugs = sorted(data.keys(),
                   key=lambda s: MODEL_ORDER.index(s) if s in MODEL_ORDER else 99)

    rows = []
    for slug in slugs:
        modes = data[slug]
        ckg_f1   = modes.get("ckg",      {}).get("macro_f1")
        base_f1  = modes.get("baseline", {}).get("macro_f1")
        ckg_tok  = modes.get("ckg",      {}).get("mean_tokens")
        label    = MODEL_LABELS.get(slug, slug)

        if ckg_f1 is None and base_f1 is None:
            continue

        gap_pct = None
        if ckg_f1 is not None and base_f1 is not None:
            denom = FRONTIER_CKG - base_f1
            gap_pct = (ckg_f1 - base_f1) / denom * 100 if denom else 0.0

        rows.append({
            "slug":     slug,
            "label":    label,
            "ckg_f1":   ckg_f1,
            "base_f1":  base_f1,
            "gap_pct":  gap_pct,
            "ckg_tokens": ckg_tok,
        })

    # Colour palette
    BLUE  = "#3B82F6"
    SLATE = "#94A3B8"
    GREEN = "#22C55E"
    RED   = "#EF4444"

    labels_js   = json.dumps([r["label"]   for r in rows])
    ckg_js      = json.dumps([r["ckg_f1"]  for r in rows])
    base_js     = json.dumps([r["base_f1"] for r in rows])
    gap_js      = json.dumps([r["gap_pct"] for r in rows])

    table_rows = ""
    for r in rows:
        ckg   = f'{r["ckg_f1"]:.4f}'  if r["ckg_f1"]  is not None else "—"
        base  = f'{r["base_f1"]:.4f}' if r["base_f1"] is not None else "—"
        gap   = f'{r["gap_pct"]:.1f}%' if r["gap_pct"] is not None else "—"
        tok   = f'{r["ckg_tokens"]:.0f}' if r["ckg_tokens"] is not None else "—"
        delta = ""
        if r["ckg_f1"] is not None and r["base_f1"] is not None:
            d = r["ckg_f1"] - r["base_f1"]
            colour = "green" if d > 0 else "red"
            delta = f'<span style="color:{colour}">+{d:.4f}</span>'
        table_rows += f"""
        <tr>
          <td><strong>{r["label"]}</strong></td>
          <td>{base}</td>
          <td>{ckg} {delta}</td>
          <td><strong>{gap}</strong></td>
          <td style="color:#64748b">{tok}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Small-Model CKG Benchmark — Gap-Closed Analysis</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         background: #0f172a; color: #e2e8f0; padding: 32px; }}
  h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }}
  .subtitle {{ font-size: 0.9rem; color: #94a3b8; margin-bottom: 32px; }}
  .card {{ background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
  .card h2 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; color: #cbd5e1; }}
  .frontier-line {{ border-left: 4px solid {GREEN};
                    padding: 8px 12px; background: #14532d33; border-radius: 4px;
                    font-size: 0.85rem; margin-bottom: 16px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  th {{ text-align: left; padding: 10px 12px; color: #94a3b8;
        border-bottom: 1px solid #334155; font-weight: 500; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #1e293b; }}
  tr:hover td {{ background: #334155; }}
  .formula {{ font-family: monospace; background: #0f172a; padding: 12px 16px;
              border-radius: 8px; font-size: 0.85rem; color: #7dd3fc;
              margin-top: 16px; }}
  .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 12px; margin-bottom: 24px; }}
  .stat {{ background: #1e293b; border-radius: 10px; padding: 16px; text-align: center; }}
  .stat .val {{ font-size: 1.8rem; font-weight: 700; color: #38bdf8; }}
  .stat .lbl {{ font-size: 0.75rem; color: #94a3b8; margin-top: 4px; }}
  canvas {{ max-height: 360px; }}
</style>
</head>
<body>

<h1>Small-Model CKG Benchmark</h1>
<p class="subtitle">How much does deterministic CKG context close the gap between a 7–8B OSS model and a frontier model?</p>

<div class="stat-grid">
  <div class="stat"><div class="val">{FRONTIER_CKG:.4f}</div><div class="lbl">Frontier + CKG F1 (ceiling)</div></div>
  <div class="stat"><div class="val">{FRONTIER_RAG:.4f}</div><div class="lbl">Frontier + RAG F1</div></div>
  <div class="stat"><div class="val">{FRONTIER_TOKENS:.0f}</div><div class="lbl">Frontier CKG mean tokens</div></div>
</div>

<div class="card">
  <h2>F1 Score: CKG vs Baseline (no context)</h2>
  <div class="frontier-line">
    Frontier CKG ceiling: <strong>{FRONTIER_CKG}</strong> — shown as dashed line
  </div>
  <canvas id="f1Chart"></canvas>
</div>

<div class="card">
  <h2>Gap-Closed % by Model</h2>
  <canvas id="gapChart"></canvas>
</div>

<div class="card">
  <h2>Results Summary</h2>
  <table>
    <thead>
      <tr>
        <th>Model</th>
        <th>Baseline F1 (no ctx)</th>
        <th>CKG F1</th>
        <th>Gap-Closed %</th>
        <th>Mean Tokens (CKG)</th>
      </tr>
    </thead>
    <tbody>{table_rows}
      <tr style="border-top: 2px solid #22c55e; opacity:0.7">
        <td><em>Frontier (Claude Haiku 4.5)</em></td>
        <td>—</td>
        <td><em>{FRONTIER_CKG}</em></td>
        <td><em>100% (ceiling)</em></td>
        <td><em>{FRONTIER_TOKENS:.0f}</em></td>
      </tr>
    </tbody>
  </table>
  <div class="formula">
    Gap-Closed = (small+CKG_F1 − small_baseline_F1) / (frontier_CKG_F1 − small_baseline_F1)
  </div>
</div>

<script>
const labels = {labels_js};
const ckgF1  = {ckg_js};
const baseF1 = {base_js};
const gapPct = {gap_js};

// ── F1 grouped bar chart ───────────────────────────────────────────────────────
new Chart(document.getElementById('f1Chart'), {{
  type: 'bar',
  data: {{
    labels,
    datasets: [
      {{
        label: 'Baseline F1 (no context)',
        data: baseF1,
        backgroundColor: '{SLATE}cc',
        borderRadius: 4,
      }},
      {{
        label: 'CKG F1',
        data: ckgF1,
        backgroundColor: '{BLUE}dd',
        borderRadius: 4,
      }},
    ],
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{ labels: {{ color: '#cbd5e1' }} }},
      annotation: {{ annotations: {{ frontier: {{
        type: 'line', yMin: {FRONTIER_CKG}, yMax: {FRONTIER_CKG},
        borderColor: '{GREEN}', borderWidth: 2, borderDash: [6,3],
        label: {{ content: 'Frontier CKG {FRONTIER_CKG}', display: true,
                  color: '{GREEN}', position: 'end', font: {{ size: 11 }} }},
      }} }} }},
    }},
    scales: {{
      x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }} }},
      y: {{ min: 0, max: 0.6, ticks: {{ color: '#94a3b8' }},
            grid: {{ color: '#334155' }},
            title: {{ display: true, text: 'Macro F1', color: '#64748b' }} }},
    }},
  }},
}});

// ── Gap-closed horizontal bar ──────────────────────────────────────────────────
new Chart(document.getElementById('gapChart'), {{
  type: 'bar',
  data: {{
    labels,
    datasets: [{{
      label: 'Gap-Closed %',
      data: gapPct,
      backgroundColor: gapPct.map(v =>
        v === null ? '#33415580' :
        v >= 60 ? '{GREEN}cc' : v >= 40 ? '#f59e0bcc' : '#ef4444cc'
      ),
      borderRadius: 4,
    }}],
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ callbacks: {{
        label: ctx => ctx.raw !== null ? ctx.raw.toFixed(1) + '%' : 'N/A'
      }} }},
    }},
    scales: {{
      x: {{ min: 0, max: 100,
            ticks: {{ color: '#94a3b8', callback: v => v + '%' }},
            grid: {{ color: '#334155' }} }},
      y: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ color: '#1e293b' }} }},
    }},
  }},
}});
</script>

</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true", help="Open in browser after generating")
    parser.add_argument("--out", default="results/small_model/gap_closed_chart.html")
    args = parser.parse_args()

    data = load_summaries()
    if not data:
        print("No summary files found under results/small_model/. Run the suite first.")
        sys.exit(1)

    html = build_chart(data)
    out  = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"Chart written to {out}")

    if args.open:
        subprocess.run(["open", str(out)])


if __name__ == "__main__":
    main()
