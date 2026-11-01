"""Figures and tables for the ARC Prize 2026 Paper Track writeup.

Reads only measured result files of the ARC-AGI-3 and ARC-AGI-2 runs (read-only)
and writes figures/ and tables/ next to this script's parent folder.
Usage: python analyze.py <arc-agi-3 resultados dir> <arc-agi-2 score.json> <out dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

R3, A2, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
(OUT / "figs").mkdir(parents=True, exist_ok=True)
(OUT / "tables").mkdir(parents=True, exist_ok=True)

RUNS = [
    ("L016", "L016_p2_explorer.json", "Control (graph explorer)"),
    ("L017", "L017_p2_chimera.json", "CHIMERA (holographic + click-CA)"),
    ("L018", "L018_p2_kbca.json", "CHIMERA + keyboard-CA"),
    ("L019", "L019_p2_kbca_noca.json", "  - click-CA"),
    ("L020", "L020_p2_kbca_nogd.json", "  - GOAL/DEADLY traces"),
    ("L021", "L021_p2_kbca_nopersist.json", "  - cross-level persistence"),
    ("L022", "L022_p2_kbca_dim2048.json", "  dim 2048"),
    ("L023", "L023_p2_kbca_alpha4.json", "  alpha 4 (submission config)"),
    ("L024", "L024_p2_kbca_alpha1.json", "  alpha 1"),
]


def load(fn):
    d = json.load(open(R3 / fn))
    games = sorted({r["game"] for r in d["results"]})
    seeds = sorted({r["seed"] for r in d["results"]})
    S = np.zeros((len(games), len(seeds)))
    L = np.zeros_like(S)
    first = {}
    for r in d["results"]:
        i, j = games.index(r["game"]), seeds.index(r["seed"])
        S[i, j], L[i, j] = r["score"], r["levels"]
        if r["level_actions"]:
            first.setdefault(r["game"], []).append(r["level_actions"][0])
    return d["summary"], games, S, L, first


data = {k: load(fn) for k, fn, _ in RUNS}
games = data["L016"][1]
for k in data:
    assert data[k][1] == games, k
ctrl_S = data["L016"][2]

rows = []
for k, fn, label in RUNS:
    summ, _, S, L, _ = data[k]
    gm = S.mean(1)
    row = {
        "id": k, "label": label.strip(), "mean": float(S.mean()),
        "sd_seeds": float(S.mean(0).std(ddof=0)),
        "levels_per_seed": [int(x) for x in L.sum(0)],
        "games_with_level": int((L.max(1) > 0).sum()),
        "wall_s": summ["wall_seconds"],
    }
    if k != "L016":
        diff = gm - ctrl_S.mean(1)
        nz = diff[diff != 0]
        row["p_vs_control"] = float(wilcoxon(nz).pvalue) if len(nz) > 0 else None
        row["games_up"], row["games_down"] = int((diff > 0).sum()), int((diff < 0).sum())
    rows.append(row)
json.dump(rows, open(OUT / "tables" / "arc3_summary.json", "w"), indent=1)

with open(OUT / "tables" / "arc3_summary.md", "w", encoding="utf-8") as f:
    f.write("| run | config | mean score (0-100) | sd over 5 seeds | levels per seed | games with >=1 level | vs control: games +/- , Wilcoxon p | CPU s (125 episodes) |\n|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        cmp = "reference" if r["id"] == "L016" else f"+{r['games_up']}/-{r['games_down']}, p={r['p_vs_control']:.4f}"
        f.write(f"| {r['id']} | {r['label']} | {r['mean']:.4f} | {r['sd_seeds']:.4f} | {r['levels_per_seed']} | {r['games_with_level']} | {cmp} | {r['wall_s']:.0f} |\n")

# per-game levels: which component solves what
with open(OUT / "tables" / "arc3_per_game.md", "w", encoding="utf-8") as f:
    f.write("| game | control levels (mean) | CHIMERA | +kb-CA | +kb-CA a4 |\n|---|---|---|---|---|\n")
    for i, g in enumerate(games):
        vals = [data[k][3][i].mean() for k in ("L016", "L017", "L018", "L023")]
        if max(vals) > 0:
            f.write(f"| {g} | " + " | ".join(f"{v:.1f}" for v in vals) + " |\n")

# Fig 1: mean score with seed spread
fig, ax = plt.subplots(figsize=(8, 4.2))
labels = [lab.strip() for _, _, lab in RUNS]
means = [r["mean"] for r in rows]
seedm = [data[k][2].mean(0) for k, _, _ in RUNS]
colors = ["#888888", "#3b6fb6", "#1f4e8c"] + ["#9bb7dd"] * 6
ax.barh(range(len(RUNS))[::-1], means, color=colors)
for y, sm in zip(range(len(RUNS))[::-1], seedm):
    ax.scatter(sm, [y] * len(sm), s=10, color="black", zorder=3)
ax.set_yticks(range(len(RUNS))[::-1])
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("Official scorecard (0-100), 25 public games, 5000 actions; dots = 5 seeds")
ax.set_title("ARC-AGI-3 offline: CHIMERA outcome memory vs graph-explorer control")
fig.tight_layout()
fig.savefig(OUT / "figs" / "fig1_scores.png", dpi=160)

# Fig 2: levels per game, control vs submission config
fig, ax = plt.subplots(figsize=(8, 3.6))
c = data["L016"][3].mean(1)
s = data["L023"][3].mean(1)
idx = [i for i in range(len(games)) if max(c[i], s[i]) > 0]
x = np.arange(len(idx))
ax.bar(x - 0.2, c[idx], 0.4, label="control", color="#888888")
ax.bar(x + 0.2, s[idx], 0.4, label="CHIMERA + kb-CA (alpha 4)", color="#1f4e8c")
ax.set_xticks(x)
ax.set_xticklabels([games[i].split("-")[0] for i in idx], rotation=60, fontsize=7)
ax.set_ylabel("levels completed (mean of 5 seeds)")
ax.set_title(f"Per-game levels ({len(idx)} of {len(games)} games with any level)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "figs" / "fig2_levels_per_game.png", dpi=160)

# Fig 3: actions to first level (sample efficiency) where both solve level 1
fc, fs = data["L016"][4], data["L023"][4]
both = sorted(set(fc) & set(fs))
fig, ax = plt.subplots(figsize=(4.6, 4.2))
xs = [np.mean(fc[g]) for g in both]
ys = [np.mean(fs[g]) for g in both]
ax.scatter(xs, ys, color="#1f4e8c")
m = max(xs + ys + [10]) * 1.1
ax.plot([1, m], [1, m], "--", color="#888888")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("control: actions to first level")
ax.set_ylabel("CHIMERA: actions to first level")
ax.set_title(f"Sample efficiency ({len(both)} games solved by both)", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "figs" / "fig3_first_level_actions.png", dpi=160)
json.dump({g: {"control": float(np.mean(fc[g])), "chimera_a4": float(np.mean(fs[g]))} for g in both},
          open(OUT / "tables" / "arc3_first_level.json", "w"), indent=1)

# ARC-AGI-2 negative result
a2 = json.load(open(A2))
json.dump(a2, open(OUT / "tables" / "arc2_e005_score_copy.json", "w"), indent=1)
print(json.dumps(rows, indent=1))
print("games solved-by-both:", len(both), "control-only:", sorted(set(fc) - set(fs)), "chimera-only:", sorted(set(fs) - set(fc)))
