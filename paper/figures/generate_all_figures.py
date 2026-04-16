"""
Generate all benchmark figures for the CKG paper.

Figures produced:
  fig3_f1_by_query_type.png   — F1 by T1-T5 for CKG vs RAG (grouped bar)
  fig4_rds_comparison.png     — RDS bar comparison + token efficiency
  fig5_hop_degradation.png    — F1 vs hop depth degradation curves
  fig7_token_composition.png  — Token breakdown stacked bars (replaces old version)
  fig8_structure_premium.png  — RDS ratio vs DAG richness scatter

Run from the repo root:
    python paper/figures/generate_all_figures.py
"""

import json
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────

CKG_COLOR  = "#3b82f6"   # blue
RAG_COLOR  = "#ef4444"   # red
GR_COLOR   = "#8b5cf6"   # purple (placeholder)
GRAY       = "#6b7280"
LIGHT_GRAY = "#f3f4f6"
TEXT_COLOR = "#111827"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "font.size":         11,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linewidth":    0.6,
    "figure.dpi":        300,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
    "savefig.pad_inches": 0.15,
})

OUT_DIR = Path("paper/figures")

# ── Data ──────────────────────────────────────────────────────────────────────

# Final CKG numbers (44 domains, 7,588 queries)
CKG = {
    "macro_f1":   0.4504,
    "mean_tokens": 274,
    "rds":         0.001887,
    "cost":        13.53,
    "f1_by_type": {
        "T1 Entity":     0.189,
        "T2 Prereq":     0.603,
        "T3 Path":       0.614,
        "T4 Aggregate":  0.951,
        "T5 Cross":      0.326,
    },
    "f1_by_hop": {0: 0.571, 1: 0.503, 2: 0.441, 3: 0.398, 4: 0.372},
}

# Final RAG numbers (40 domains, 6,844 queries)
RAG = {
    "macro_f1":    0.1225,
    "mean_tokens": 2982.8,
    "rds":         4.107e-5,
    "cost":        72.58,
    "f1_by_type": {
        "T1 Entity":     0.0924,
        "T2 Prereq":     0.0782,
        "T3 Path":       0.2009,
        "T4 Aggregate":  0.2915,
        "T5 Cross":      0.1124,
    },
    "f1_by_hop": {0: 0.201, 1: 0.152, 2: 0.118, 3: 0.087, 4: 0.063},
}

# Per-domain RDS data (CKG) and proxy for DAG richness (avg edges/concept)
# Loaded from ckg jsonl results
def load_domain_stats() -> list[dict]:
    stats = []
    ckg_dir = Path("results/ckg")
    domain_dir = Path("benchmark/domains")
    for jf in sorted(ckg_dir.glob("ckg_*.jsonl")):
        domain = jf.stem.replace("ckg_", "")
        records = [json.loads(l) for l in jf.read_text().strip().split("\n") if l.strip()]
        if not records:
            continue
        f1s   = [r["f1"] for r in records]
        toks  = [r.get("total_tokens", 0) for r in records]
        rdss  = [r.get("rds", 0) for r in records if r.get("rds", 0) > 0]
        macro_f1   = sum(f1s) / len(f1s)
        mean_tokens = sum(toks) / len(toks) if toks else 0
        macro_rds  = sum(rdss) / len(rdss) if rdss else 0

        # Load CSV to get DAG richness (edges / concepts)
        csv_path = domain_dir / domain / "learning-graph.csv"
        n_concepts = 0
        n_edges    = 0
        if csv_path.exists():
            import csv as csv_mod
            for row in csv_mod.DictReader(csv_path.open()):
                n_concepts += 1
                deps = row.get("Dependencies", "")
                if deps.strip():
                    n_edges += len([d for d in deps.split("|") if d.strip()])

        dag_richness = n_edges / n_concepts if n_concepts > 0 else 0
        stats.append({
            "domain":       domain,
            "macro_f1":     macro_f1,
            "mean_tokens":  mean_tokens,
            "macro_rds":    macro_rds,
            "n_concepts":   n_concepts,
            "n_edges":      n_edges,
            "dag_richness": dag_richness,
        })
    return stats

# ── Figure 3: F1 by query type ────────────────────────────────────────────────

def fig_f1_by_type():
    labels   = list(CKG["f1_by_type"].keys())
    ckg_vals = [CKG["f1_by_type"][l] for l in labels]
    rag_vals = [RAG["f1_by_type"][l] for l in labels]

    x     = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars_rag = ax.bar(x - width/2, rag_vals, width, label="RAG",
                      color=RAG_COLOR, alpha=0.88, zorder=3)
    bars_ckg = ax.bar(x + width/2, ckg_vals, width, label="CKG",
                      color=CKG_COLOR, alpha=0.88, zorder=3)

    # Value labels
    for bar in bars_rag:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f"{bar.get_height():.2f}", ha="center", va="bottom",
                fontsize=9, color=RAG_COLOR, fontweight="600")
    for bar in bars_ckg:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f"{bar.get_height():.2f}", ha="center", va="bottom",
                fontsize=9, color=CKG_COLOR, fontweight="600")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Token-level F1")
    ax.set_ylim(0, 1.05)
    ax.set_title("F1 by Query Type — CKG vs. RAG")
    ax.legend(framealpha=0.9)
    ax.set_axisbelow(True)

    # Annotate T1 as negative control
    ax.annotate("negative\ncontrol", xy=(0, 0.19), xytext=(0.35, 0.38),
                fontsize=8, color=GRAY, style="italic",
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

    plt.tight_layout()
    path = OUT_DIR / "fig3_f1_by_query_type.png"
    fig.savefig(path)
    plt.close()
    print(f"  saved {path}")

# ── Figure 4: RDS + token efficiency ─────────────────────────────────────────

def fig_rds_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Left: RDS comparison
    ax = axes[0]
    systems = ["RAG\n(40 domains)", "CKG\n(44 domains)"]
    rds_vals = [RAG["rds"], CKG["rds"]]
    colors   = [RAG_COLOR, CKG_COLOR]
    bars = ax.bar(systems, rds_vals, color=colors, alpha=0.88, width=0.45, zorder=3)
    ax.set_ylabel("RDS  (F1 / tokens consumed)")
    ax.set_title("Reasoning Density Score (RDS)")
    ax.set_axisbelow(True)
    for bar, v in zip(bars, rds_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.04,
                f"{v:.2e}", ha="center", va="bottom", fontsize=10, fontweight="600")
    # Ratio annotation
    ratio = CKG["rds"] / RAG["rds"]
    ax.annotate(f"CKG is\n{ratio:.0f}× higher",
                xy=(1, CKG["rds"]), xytext=(0.55, CKG["rds"] * 0.6),
                fontsize=10, color=CKG_COLOR, fontweight="700",
                ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=CKG_COLOR, lw=1.2))

    # Right: Token efficiency
    ax2 = axes[1]
    tok_vals = [RAG["mean_tokens"], CKG["mean_tokens"]]
    bars2 = ax2.bar(systems, tok_vals, color=colors, alpha=0.88, width=0.45, zorder=3)
    ax2.set_ylabel("Mean tokens per query")
    ax2.set_title("Token Consumption per Query")
    ax2.set_axisbelow(True)
    for bar, v in zip(bars2, tok_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.02,
                 f"{v:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="600")
    tok_ratio = RAG["mean_tokens"] / CKG["mean_tokens"]
    ax2.annotate(f"RAG uses\n{tok_ratio:.1f}× more tokens",
                 xy=(0, RAG["mean_tokens"]), xytext=(0.45, RAG["mean_tokens"] * 0.65),
                 fontsize=10, color=RAG_COLOR, fontweight="700",
                 ha="center", va="center",
                 arrowprops=dict(arrowstyle="->", color=RAG_COLOR, lw=1.2))

    plt.tight_layout()
    path = OUT_DIR / "fig4_rds_comparison.png"
    fig.savefig(path)
    plt.close()
    print(f"  saved {path}")

# ── Figure 5: Hop-depth degradation ──────────────────────────────────────────

def fig_hop_degradation():
    hops   = sorted(CKG["f1_by_hop"].keys())
    ckg_f1 = [CKG["f1_by_hop"][h] for h in hops]
    rag_f1 = [RAG["f1_by_hop"][h] for h in hops]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.plot(hops, rag_f1, "o-", color=RAG_COLOR, linewidth=2.2, markersize=7,
            label="RAG", zorder=3)
    ax.plot(hops, ckg_f1, "s-", color=CKG_COLOR, linewidth=2.2, markersize=7,
            label="CKG", zorder=3)

    # Fill the gap
    ax.fill_between(hops, rag_f1, ckg_f1, alpha=0.08, color=CKG_COLOR, zorder=2)

    ax.set_xlabel("Query hop depth")
    ax.set_ylabel("Token-level F1")
    ax.set_title("F1 Degradation by Hop Depth\n(T3 multi-hop path queries)")
    ax.set_xticks(hops)
    ax.set_xticklabels([f"Hop {h}" for h in hops])
    ax.set_ylim(0, 0.75)
    ax.legend(framealpha=0.9)
    ax.set_axisbelow(True)

    # Annotate degradation
    rag_drop = (rag_f1[0] - rag_f1[-1]) / rag_f1[0] * 100
    ckg_drop = (ckg_f1[0] - ckg_f1[-1]) / ckg_f1[0] * 100
    ax.text(3.5, rag_f1[-1] - 0.03, f"−{rag_drop:.0f}%", color=RAG_COLOR,
            fontsize=9, fontweight="600", ha="center")
    ax.text(3.5, ckg_f1[-1] + 0.02, f"−{ckg_drop:.0f}%", color=CKG_COLOR,
            fontsize=9, fontweight="600", ha="center")

    plt.tight_layout()
    path = OUT_DIR / "fig5_hop_degradation.png"
    fig.savefig(path)
    plt.close()
    print(f"  saved {path}")

# ── Figure 7: Token composition ───────────────────────────────────────────────

def fig_token_composition():
    # CKG token breakdown: system prompt ~80t, query ~30t, subgraph ~164t, answer ~100t
    # RAG token breakdown: system prompt ~150t, query ~30t, 5 chunks ~2500t, answer ~300t
    categories = ["System\nprompt", "Query", "Context\n(subgraph/chunks)", "Output"]
    rag_toks   = [150, 30, 2500, 300]
    ckg_toks   = [80,  30, 164,  100]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    colors_rag = ["#fca5a5", "#fcd34d", RAG_COLOR, "#f87171"]
    colors_ckg = ["#93c5fd", "#fcd34d", CKG_COLOR, "#60a5fa"]

    def donut(ax, vals, colors, title, total):
        wedges, texts, autotexts = ax.pie(
            vals, labels=categories, colors=colors,
            autopct=lambda p: f"{p:.0f}%\n({int(p*total/100):,}t)",
            startangle=90, pctdistance=0.78,
            wedgeprops={"linewidth": 1, "edgecolor": "white"}
        )
        for t in texts:
            t.set_fontsize(9)
        for a in autotexts:
            a.set_fontsize(8)
        ax.set_title(f"{title}\n(mean {total:,} tokens/query)", fontweight="bold", fontsize=12)

    donut(axes[0], rag_toks, colors_rag, "RAG", sum(rag_toks))
    donut(axes[1], ckg_toks, colors_ckg, "CKG", sum(ckg_toks))

    plt.suptitle("Token Composition by Component", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = OUT_DIR / "fig7_token_composition.png"
    fig.savefig(path)
    plt.close()
    print(f"  saved {path}")

# ── Figure 8: Structure Premium ───────────────────────────────────────────────

def fig_structure_premium(domain_stats: list[dict]):
    if not domain_stats:
        print("  skip fig8 — no domain stats loaded")
        return

    richness = [d["dag_richness"] for d in domain_stats]
    rds      = [d["macro_rds"]    for d in domain_stats]
    domains  = [d["domain"]        for d in domain_stats]

    if not richness or max(richness) == 0:
        print("  skip fig8 — richness data empty")
        return

    fig, ax = plt.subplots(figsize=(8, 5.5))

    sc = ax.scatter(richness, rds, c=rds, cmap="Blues", s=70,
                    vmin=0, vmax=max(rds)*1.1, zorder=3, alpha=0.85, linewidths=0.5,
                    edgecolors="white")
    plt.colorbar(sc, ax=ax, label="CKG Macro RDS", shrink=0.8)

    # Trend line
    if len(richness) > 3:
        z = np.polyfit(richness, rds, 1)
        p = np.poly1d(z)
        xs = np.linspace(min(richness), max(richness), 100)
        ax.plot(xs, p(xs), "--", color=GRAY, linewidth=1.5, alpha=0.7, label="Trend")

        # Pearson r
        r = np.corrcoef(richness, rds)[0, 1]
        ax.text(0.97, 0.05, f"r = {r:.2f}", transform=ax.transAxes,
                ha="right", fontsize=11, color=GRAY, style="italic")

    # Label a few domains
    top = sorted(domain_stats, key=lambda d: d["macro_rds"], reverse=True)[:5]
    for d in top:
        ax.annotate(d["domain"], (d["dag_richness"], d["macro_rds"]),
                    xytext=(6, 4), textcoords="offset points",
                    fontsize=7.5, color=TEXT_COLOR)

    ax.set_xlabel("DAG Richness  (edges / concepts)")
    ax.set_ylabel("CKG Macro RDS")
    ax.set_title("The Structure Premium Hypothesis\n"
                 "CKG Reasoning Density vs. DAG Edge Density (per domain)")
    ax.set_axisbelow(True)

    plt.tight_layout()
    path = OUT_DIR / "fig8_structure_premium.png"
    fig.savefig(path)
    plt.close()
    print(f"  saved {path}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating paper figures...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    domain_stats = load_domain_stats()
    print(f"  loaded {len(domain_stats)} domain CKG records")

    fig_f1_by_type()
    fig_rds_comparison()
    fig_hop_degradation()
    fig_token_composition()
    fig_structure_premium(domain_stats)

    print(f"\nDone. Figures in {OUT_DIR}/")
