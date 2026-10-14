#!/usr/bin/env python3
"""Generate the README result figures (SVG) from results/tables/*.csv.

Run from the repository root:

    python assets/readme/make_figures.py

Outputs:
    assets/readme/fig_results.svg   -- F1 by query type (left), F1 by hop depth (right)

The figures are plain SVG so they can be diffed, edited, and rendered by GitHub
without any raster conversion. Numbers are read from the committed tables; the
script never recomputes metrics.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
OUT = Path(__file__).resolve().parent / "fig_results.svg"

SYSTEMS = [("ckg", "CKG", "#1f4e79"), ("rag", "RAG", "#9a9a9a"), ("graphrag", "GraphRAG", "#3f8f7a")]
TYPES = [("T1_entity", "T1 entity"), ("T2_dependency", "T2 dependency"), ("T3_path", "T3 path"),
         ("T4_aggregate", "T4 aggregate"), ("T5_cross_concept", "T5 cross-concept")]
FONT = "font-family='-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif'"


def read_table(name):
    with open(TABLES / name, newline="") as f:
        return {r["system"]: r for r in csv.DictReader(f)}


def fmt(v):
    return f"{float(v):.2f}"


def panel_bars(t2, x0, y0, w, h):
    """Grouped bars: F1 by query type."""
    s = []
    pad_l, pad_b, pad_t = 34, 44, 28
    px, py, pw, ph = x0 + pad_l, y0 + pad_t, w - pad_l - 8, h - pad_t - pad_b
    s.append(f"<text x='{x0}' y='{y0 + 12}' {FONT} font-size='12' font-weight='600' fill='#222'>a. Macro F1 by query type</text>")
    # axes + gridlines
    for i in range(0, 6):
        v = i / 5
        y = py + ph - v * ph
        s.append(f"<line x1='{px}' y1='{y:.1f}' x2='{px + pw}' y2='{y:.1f}' stroke='#e6e6e6' stroke-width='1'/>")
        s.append(f"<text x='{px - 6}' y='{y + 3.5:.1f}' {FONT} font-size='9' fill='#666' text-anchor='end'>{v:.1f}</text>")
    s.append(f"<line x1='{px}' y1='{py}' x2='{px}' y2='{py + ph}' stroke='#999' stroke-width='1'/>")
    s.append(f"<line x1='{px}' y1='{py + ph}' x2='{px + pw}' y2='{py + ph}' stroke='#999' stroke-width='1'/>")
    ng = len(TYPES)
    gw = pw / ng
    bw = gw * 0.22
    for gi, (key, label) in enumerate(TYPES):
        gx = px + gi * gw + gw * 0.17
        for si, (sk, sl, color) in enumerate(SYSTEMS):
            v = float(t2[sk][key])
            bh = v * ph
            x = gx + si * bw
            y = py + ph - bh
            s.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{bw - 2:.1f}' height='{bh:.1f}' fill='{color}'/>")
            s.append(f"<text x='{x + (bw - 2) / 2:.1f}' y='{y - 3:.1f}' {FONT} font-size='7.5' fill='#333' text-anchor='middle'>{fmt(v)}</text>")
        s.append(f"<text x='{px + gi * gw + gw / 2:.1f}' y='{py + ph + 14}' {FONT} font-size='9' fill='#333' text-anchor='middle'>{label}</text>")
    s.append(f"<text x='{px + pw / 2:.1f}' y='{py + ph + 32}' {FONT} font-size='9' fill='#666' text-anchor='middle'>CKG n = 8,121 · RAG n = 7,414 · GraphRAG n = 2,683 queries</text>")
    return "\n".join(s)


def panel_lines(t4, x0, y0, w, h):
    """Line chart: F1 by hop depth."""
    s = []
    pad_l, pad_b, pad_t = 34, 44, 28
    px, py, pw, ph = x0 + pad_l, y0 + pad_t, w - pad_l - 8, h - pad_t - pad_b
    s.append(f"<text x='{x0}' y='{y0 + 12}' {FONT} font-size='12' font-weight='600' fill='#222'>b. Macro F1 by hop depth</text>")
    for i in range(0, 6):
        v = i / 5
        y = py + ph - v * ph
        s.append(f"<line x1='{px}' y1='{y:.1f}' x2='{px + pw}' y2='{y:.1f}' stroke='#e6e6e6' stroke-width='1'/>")
        s.append(f"<text x='{px - 6}' y='{y + 3.5:.1f}' {FONT} font-size='9' fill='#666' text-anchor='end'>{v:.1f}</text>")
    s.append(f"<line x1='{px}' y1='{py}' x2='{px}' y2='{py + ph}' stroke='#999' stroke-width='1'/>")
    s.append(f"<line x1='{px}' y1='{py + ph}' x2='{px + pw}' y2='{py + ph}' stroke='#999' stroke-width='1'/>")
    hops = list(range(6))
    xs = [px + 18 + i * (pw - 36) / 5 for i in hops]
    for i, x in zip(hops, xs):
        s.append(f"<text x='{x:.1f}' y='{py + ph + 14}' {FONT} font-size='9' fill='#333' text-anchor='middle'>{i}</text>")
    s.append(f"<text x='{px + pw / 2:.1f}' y='{py + ph + 32}' {FONT} font-size='9' fill='#666' text-anchor='middle'>hop depth of the query (CKG n per hop: 2,885 / 4,104 / 199 / 361 / 286 / 286)</text>")
    for sk, sl, color in SYSTEMS:
        pts = [(x, py + ph - float(t4[sk][f"hop_{i}"]) * ph) for i, x in zip(hops, xs)]
        d = " ".join(f"{'M' if j == 0 else 'L'}{x:.1f},{y:.1f}" for j, (x, y) in enumerate(pts))
        s.append(f"<path d='{d}' fill='none' stroke='{color}' stroke-width='2'/>")
        for (x, y) in pts:
            s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='2.8' fill='{color}'/>")
    return "\n".join(s)


def legend(x, y):
    s = []
    for i, (sk, sl, color) in enumerate(SYSTEMS):
        lx = x + i * 92
        s.append(f"<rect x='{lx}' y='{y - 8}' width='10' height='10' fill='{color}'/>")
        s.append(f"<text x='{lx + 15}' y='{y + 1}' {FONT} font-size='10' fill='#333'>{sl}</text>")
    return "\n".join(s)


def main():
    t2 = read_table("table2_by_query_type.csv")
    t4 = read_table("table4_hop_degradation.csv")
    W, H = 920, 300
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='CKG benchmark results: F1 by query type and by hop depth'>",
        f"<rect width='{W}' height='{H}' fill='#ffffff'/>",
        panel_bars(t2, 16, 34, 500, 240),
        panel_lines(t4, 540, 34, 360, 240),
        legend(16, 18),
        f"<text x='{W - 16}' y='18' {FONT} font-size='9' fill='#888' text-anchor='end'>Source: results/tables/table2_by_query_type.csv, table4_hop_degradation.csv · Claude Haiku 4.5, temperature 0</text>",
        "</svg>",
    ]
    OUT.write_text("\n".join(parts) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
