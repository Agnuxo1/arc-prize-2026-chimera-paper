# ARC Prize 2026 Paper: Holographic Outcome Memory

![Conceptual animated workflow](assets/workflow.gif)

Conceptual architecture illustration only. No figure frame is an experimental recording or a measured score. [Static alternative](assets/workflow.png) and [regeneration source](scripts/generate_workflow_visual.py).

**Competition:** https://arcprize.org/competitions/2026/paper

**Status:** PAPER DRAFT: official Kaggle Paper Track entry NOT verified

## Research question and objective

Examine whether compact local associative memory improves action ordering during interactive ARC-AGI-3 exploration.

## Architecture and hypothesis

Superpose random-phase context features, update signed EFFECT, GOAL and DEADLY traces on transitions, and re-rank untried actions without excluding them; evaluate against the same graph explorer.

## Measured evidence and baselines

Reported 25-game offline control 0.147 versus CHIMERA 0.422 (five-seed protocol). Kaggle ARC3 submission 57858448 COMPLETE scored 0.26 public. Offline and official metrics are different and must not be conflated.

The result above is deliberately phase-labelled. Any held-out competition rank not independently verified remains unknown.

## Reproducibility and source provenance

The following original research files were copied from the owner's local competition workspace on 1 November 2026, without modifying original files:

- paper/WRITEUP.md
- scripts/analyze.py
- scripts/cover.py
- tables/arc3_summary.json
- tables/arc3_first_level.json
- tables/arc3_per_game.md
- tables/arc2_e005_score_copy.json
- figs/cover.png
- figs/fig1_scores.png
- figs/fig2_levels_per_game.png
- figs/fig3_first_level_actions.png

This release intentionally excludes unauthorized organizer data, personal records, signed forms, credentials, external weights and third-party corpora. Install the project's stated dependencies and acquire the authorized input data before running experimental pipelines. The GitHub Actions workflow verifies syntax and regenerates the conceptual animation; it does not claim to reproduce the official challenge evaluation.

To regenerate the animation: install Python 3.11+ and Pillow 10.4.0, then run python scripts/generate_workflow_visual.py.

## Experimental controls and limitations

Paper release is not proof of Kaggle Paper Track submission. Related ARC3 source uses MIT; organizer cites public-domain-style CC0/MIT-0, which needs explicit copyright-owner resolution for prize eligibility.

A prepared archive or notebook is not evidence of an official submission. Keep public, private, warm-up and local scores distinct, and preserve baseline and ablation failures.

## Licenses, references, and AI use

Third-party components retain their upstream licenses; no previously unlicensed source is relicensed by this publication. Licensing of newly curated material is subject to rights review. Competition official URL is linked above. AI assistance was used to produce factual English documentation and conceptual visuals; experimental metrics were not generated.

[Evidence and source manifest](PROVENANCE.md).

## Full scientific manuscript

[Read paper](paper/WRITEUP.md). Publication here is not an official Kaggle Paper Track submission.

![Experiment summary](figs/fig1_scores.png)
