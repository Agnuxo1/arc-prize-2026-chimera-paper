# A Holographic Outcome Memory That Learns Local Game Rules While Playing: CHIMERA on ARC-AGI-3

**Subtitle:** Phase-superposition memory and local rule features re-rank a graph explorer: +188 % offline score, CPU only, no pre-training.

**Track:** ARC-AGI-3 · **Documented submission ID:** 57858448 · **Leaderboard score:** 0.26 (public score, S03)
**Team:** Francisco Angulo de Lafuente (Agnuxo1) · **Code:** https://github.com/Agnuxo1/arc3-chimera-explorer · https://github.com/Agnuxo1/arc3-chimera-explorer

## 1. Question

ARC-AGI-3 scores each level by min(115, (human/agent actions)² × 100), so an agent that eventually finds the goal by exhaustive search scores almost nothing. Our question: **can a tiny, training-free associative memory, written online from the agent's own transitions, make exhaustive exploration efficient enough to matter?** We test CHIMERA against an identical explorer without it.

## 2. Method

**Control: complete graph explorer.** States are hashes of the 64×64 frame after masking self-changing pixels (timers, progress bars). In each state the explorer tries every untried action in a fixed salience order (keyboard actions and the 8 most salient click targets first, up to 48 click targets from connected-component segmentation); when a state is exhausted it walks the known graph (BFS) to the nearest state with untried actions. GAME_OVER transitions are marked deadly. It forgets everything at each level.

**CHIMERA: outcome memory over the same explorer.** CHIMERA (Agnuxo1/ARC2_CHIMERA) computes with cellular-automaton (CA) updates and holographic memory in OpenGL shaders; Kaggle has no display, so we port both ingredients to numpy:

1. *Holographic memory.* Every context feature *f* receives a fixed random phase vector *e^{iφ_f}* ∈ ℂ^D (D = 512). An action context is the normalised superposition of its feature vectors. Three complex traces store what followed each action: EFFECT (state changed: +1, no-op: −1), GOAL (level completed) and DEADLY (game over). Reads are Re⟨k, T⟩/D; writes use the delta rule T ← T + 0.5 (y − read(k)) k/(‖k‖²/D).
2. *Local CA rules as features.* For clicks: colour, colour×shape, size bucket, border contact and the 3×3 neighbourhood of the clicked pixel. For keyboard actions (kb-CA): the 7×7 neighbourhood around the place where that key last changed the screen (typically the controlled sprite). A local rule key such as "this 3×3 pattern + this action" therefore carries its outcome to every state and level where the pattern recurs.

The value of an action is EFFECT + 2·GOAL⁺ − 2·DEADLY⁺. CHIMERA only **re-orders** untried candidate actions (priority tier − α·value) and frontier states; it never removes one. The local patterns are ranking features; no automaton is simulated. The three traces persist across levels (the state graph is rebuilt per level).

**Why it should work (theory).** (i) With random phases, ⟨e^{iφ_f}, e^{iφ_g}⟩ ≈ 0 for f ≠ g, so a context key is a dense superposition whose feature components are nearly orthogonal in expectation; the delta rule is then online least squares on a random-feature embedding (LMS on a holographic reduced representation; Widrow & Hoff 1960). Two contexts that share features (same colour, same local pattern) have correlated keys, so one observed outcome generalises to unseen contexts roughly in proportion to their feature overlap (up to O(1/√D) crosstalk). (ii) ARC-AGI-3 games reuse mechanics within and across levels: walls block, a button colour toggles, an avatar moves. These are *local* regularities, which is precisely what a CA-style neighbourhood key captures. (iii) Because the score is quadratic in action efficiency, moving the first successful action earlier is worth far more than finding new states late. (iv) Because every generated candidate is still tried, re-ranking delays rather than forbids; within a finite budget it can still cost levels, and empirically that is rare (§4).

## 3. Experimental protocol

- 25 public ARC-AGI-3 games, offline, official `arc_agi` 0.9.8 scorecard (0–100 scale), 5000 actions per game.
- Games are deterministic, so seeds change only CHIMERA's random phase projection; 5 seeds, 125 episodes per configuration.
- Paired Wilcoxon test over games (seed means).
- All numbers come from the published result files (`results/v2_perception`); a Linux re-run reproduced the control, CHIMERA and keyboard-CA runs exactly (`results/server_replica`).
- Both arms share the perception mask; masking alone raised the control from 0.0013 to 0.147, a larger effect than CHIMERA's.

## 4. Results

| Run | Configuration | Mean score | SD (seeds) | Levels per seed | vs control (games +/−, p) |
|---|---|---|---|---|---|
| L016 | Control (graph explorer) | 0.147 | 0.000 | 14 ×5 | — |
| L017 | CHIMERA (holographic + click-CA) | 0.308 | 0.146 | 18–21 | +15/−2, p = 0.0008 |
| L018 | + keyboard-CA | 0.393 | 0.174 | 18–22 | +14/−3, p = 0.0046 |
| L023 | + keyboard-CA, α = 4 (Kaggle candidate) | **0.422** | 0.196 | 18–21 | +14/−2, p = 0.0034 |

The α = 4 configuration nearly triples the control's score (+188 %).

**Where the gain comes from (per game).** Three games gain levels the control never reaches: sc25 (0 → 2.4 levels on average), tu93 (0 → 2.0), g50t (0 → 0.4). Only one game loses levels: lf52 (1.0 → 0.8; one seed misses); in score, cd82 and ls20 also drop. On the 13 games where both solve level 1, CHIMERA needs a geometric mean of **0.63×** the control's actions (averaged over seeds that complete the level) (9 faster, 3 slower, 1 equal; Figure 3): vc33 966 → 32, s5i5 3698 → 706, lp85 165 → 40. The quadratic score makes these gains dominate.

**Ablations against the full model (L018).**

| Removed or changed | Mean | Δ vs L018 | p |
|---|---|---|---|
| click-CA features | 0.404 | +0.011 | 0.50 |
| GOAL/DEADLY traces | 0.396 | +0.003 | 0.89 |
| trace persistence (kb locations kept) | 0.324 | −0.070 | n/a (only 4 games differ) |
| D = 2048 | 0.291 | −0.102 | 0.68 |
| α = 1 | 0.287 | −0.106 | **0.037** |
| α = 4 | 0.422 | +0.028 | 0.46 |

Honest reading: the whole memory beats the control in every variant, and a weak re-ranking (α = 1) is significantly worse (α = 4 was chosen among the tested variants, so its p-value is exploratory), but no ablation removes the EFFECT trace alone, so we cannot isolate it; the keyboard-CA adds levels in tu93 (1.0 → 2.0) and sc25 (2.0 → 2.4) but loses bp35 (1.0 → 0), and its average gain over L017 is not significant; GOAL/DEADLY traces and click-CA are not measurably useful within 5000 actions; removing trace persistence lowers the score in 3 of the 4 games where it changes anything (exploratory p = 0.38).

**Cost.** Elapsed time per episode: control 1.3 ms per action, CHIMERA 3.0 ms (about 15 s per 5000-action game; 4 parallel CPU processes). No GPU, no training data, no language model.

## 5. Same principle on ARC-AGI-2: a negative result

We applied the static version of CHIMERA (DSL search plus induced local CA rules, verified leave-one-out on all training pairs) to ARC-AGI-2. On the public *training* set it is precise (first version: 50 outputs emitted, 44 correct; with extended CA rules: 59 emitted, 53 correct, the new CA rules 11/11). On the 172 public *evaluation* outputs it emits **0 candidates**, so it adds no candidates to a solver on those outputs. Local rule induction from 2–4 static examples does not cover ARC-AGI-2's compositional tasks; on ARC-AGI-3 the same locality bias works because the agent generates thousands of its own labelled transitions per game. Our hypothesis from this contrast: **local associative rules need interaction data, and interactive benchmarks supply it.**

## 6. Limitations

- Absolute scores are very low (0.42/100 offline); 7 of 25 games yield no level in any main configuration.
- Variance across phase projections is large (SD ≈ 0.15–0.2); with α = 4, seed 0 scores 0.73 and seed 1 0.18.
- Offline public games are not the hidden test set; only the leaderboard score of the documented submission is out-of-sample.
- The memory is a linear model on random features; a hashed linear model might match it.
- Offline budget (5000 actions) is smaller than the Kaggle run's.

## 7. Toward a top score

We expect the mechanism to work as an action-ranking prior for other exploration agents, including LLM-driven ones (untested): 3 ms per action, no data, every transition becomes a reusable local rule. Next: object-centric features; GOAL traces for planning.

## Reproducibility

Code (MIT; CC-BY 4.0 granted to the sponsor if awarded): https://github.com/Agnuxo1/arc3-chimera-explorer (commit 746aab3; `arc3chimera/chimera.py`, `scripts/stats.py`, Kaggle notebooks in `kaggle/`); ARC-AGI-2: https://github.com/Agnuxo1/arc2-chimera-2026 (`experiments/LOG.md`). Run `python -m arc3chimera.runner --env-dir <official environments> --policy chimera --kw '{"salt_seed":true,"use_kbca":true,"alpha":4}' --seeds 0,1,2,3,4 --max-actions 5000 --out chimera.json`.

**Use of AI.** AI coding agents (Anthropic Claude, OpenAI Codex as auditor) helped run experiments and draft this text; every number was checked against the logged result files.

**References.** Plate, T. (1995) Holographic reduced representations, *IEEE Trans. Neural Networks* 6(3):623–641, doi:10.1109/72.377968. Kanerva, P. (2009) Hyperdimensional computing, *Cognitive Computation* 1:139–159, doi:10.1007/s12559-009-9009-8. Chollet, F. (2019) On the measure of intelligence, arXiv:1911.01547.
