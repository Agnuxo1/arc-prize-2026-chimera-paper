"""Cover image (schematic of the CHIMERA world model over a graph explorer)."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 6.75))
ax.set_xlim(0, 12); ax.set_ylim(0, 6.75); ax.axis("off")
fig.patch.set_facecolor("#0e1726")
def box(x, y, w, h, text, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec="white", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=12)
def arrow(a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, color="white", lw=1.4))
ax.text(6, 6.15, "CHIMERA outcome memory for ARC-AGI-3", ha="center", color="white", fontsize=24, weight="bold")
ax.text(6, 5.6, "holographic phase memory + local cellular-automaton rules, re-ranking a complete graph explorer",
        ha="center", color="#b8c7e0", fontsize=13)
box(0.4, 2.6, 2.2, 1.3, "game frame\n64x64, 16 colours", "#2d3e5c")
box(3.3, 3.6, 2.6, 1.2, "context features\naction, colour, shape,\n3x3 / 7x7 CA patch", "#3b6fb6")
box(3.3, 1.6, 2.6, 1.2, "graph explorer\n(state hash, BFS frontier)", "#555f70")
box(6.6, 3.6, 2.6, 1.2, "phase superposition\n3 traces: EFFECT,\nGOAL, DEADLY", "#1f4e8c")
box(6.6, 1.6, 2.6, 1.2, "rank untried actions\nand frontier states", "#1f4e8c")
box(9.8, 2.6, 1.9, 1.3, "action", "#2d3e5c")
arrow((2.6, 3.4), (3.3, 4.1)); arrow((2.6, 3.1), (3.3, 2.3))
arrow((5.9, 4.2), (6.6, 4.2)); arrow((7.9, 3.6), (7.9, 2.8)); arrow((5.9, 2.2), (6.6, 2.2))
arrow((9.2, 2.2), (9.8, 3.0))
ax.annotate("", xy=(7.9, 4.8), xytext=(10.7, 3.9),
            arrowprops=dict(arrowstyle="-|>", color="#f2b134", lw=1.4, connectionstyle="arc3,rad=0.35"))
ax.text(10.2, 4.85, "delta-rule write\nafter every step", color="#f2b134", fontsize=11, ha="center")
ax.text(6, 0.6, "offline scorecard (0-100), 25 public games, 5 seeds: control 0.147 -> CHIMERA 0.422 (Wilcoxon p = 0.003) | CPU only",
        ha="center", color="white", fontsize=13)
fig.savefig(sys.argv[1], dpi=100, facecolor=fig.get_facecolor())
