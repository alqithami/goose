# CHMARL/Tomorrow integration strategy

This repository is now treated as a CHMARL/Tomorrow fork of Goose, not merely a small upstream patch.

The fork should evolve into an agentic research workbench around EcoFair-CH-MARL: a place where we can add project-specific documentation, recipes, MCP tools, analysis scripts, assistant modes, and eventually custom desktop branding.

## Related project assets

- CHMARL project site: https://chmarl.com
- Paper: https://arxiv.org/abs/2603.14625
- Core implementation repository: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose: https://github.com/aaif-goose/goose

## Architecture

```text
alqithami/EcoFairCHAMRL
  Research code: constrained hierarchical MARL environment, training loop,
  emission-budget logic, fairness metrics, baselines, experiments, outputs.

alqithami/goose
  CHMARL/Tomorrow assistant distribution: project-specific Goose recipes,
  documentation, MCP extensions, experiment analysis, repo-maintenance helpers,
  and future custom UI/desktop branding.

chmarl.com
  Public communication layer: paper gateway, demos, figures, tutorials,
  implementation notes, and result summaries.
```

## What this fork should become

### 1. CHMARL paper assistant

The fork should help explain and validate the EcoFair-CH-MARL paper:

- summarize sections and equations
- check claims against code
- identify implementation gaps
- prepare reviewer responses
- generate related-work notes
- maintain a paper-to-code traceability table

### 2. Experiment planner

The fork should generate and maintain reproducible experiment matrices:

```bash
python EcoFairCHMARL.py --episodes 2000 --outdir results/baseline
python EcoFairCHMARL.py --emission_cap --episodes 2000 --outdir results/emission_cap
python EcoFairCHMARL.py --fairness --episodes 2000 --outdir results/fairness
python EcoFairCHMARL.py --emission_cap --fairness --episodes 2000 --outdir results/emission_fairness
python EcoFairCHMARL.py --algo SOTO --episodes 2000 --outdir results/soto
python EcoFairCHMARL.py --algo FEN --episodes 2000 --outdir results/fen
```

The long-term target is a Goose recipe that can ask for a study design and produce:

- command matrix
- output directory naming convention
- seed plan
- expected CSV files
- comparison table template
- result interpretation checklist

### 3. Result analyst

The fork should analyze outputs from `EcoFairCHAMRL`, including:

- `results_<algo>.csv`
- `fairness_metrics_<algo>.csv`
- `training_fairness_metrics_<algo>.csv`
- generated figures and convergence plots

The MCP extension in `extensions/chmarl-results-mcp/` is the first step. It should grow from simple descriptive statistics into a CHMARL-aware result analyst that understands returns, Gini, max-min ratio, fuel/emissions proxies, ablations, and seed variance.

### 4. Repository maintainer

The fork should help improve the CHMARL codebase itself. Recommended target structure for the core implementation:

```text
chmarl/
  __init__.py
  env.py
  metrics.py
  baselines.py
  train.py
  convergence.py
  cli.py

tests/
  test_metrics.py
  test_env_step.py
  test_cli.py

docs/
  paper_to_code_traceability.md
  experiments.md
```

Suggested priorities:

1. Add `requirements.txt` or `pyproject.toml`.
2. Add deterministic seed handling.
3. Add tests for fairness metrics.
4. Add environment smoke tests for reset/step.
5. Add CLI smoke tests.
6. Separate implemented baselines from placeholders or fallback behavior.
7. Add result aggregation scripts.
8. Add a paper-to-code traceability matrix.

### 5. Tomorrow planner

The fork should also serve as a planning layer for future Tomorrow-facing work:

- broader sustainable logistics beyond maritime
- energy-grid experiments
- policy-facing dashboards
- explainable fairness/emissions trade-off summaries
- public demo narratives for `chmarl.com`
- integration with data portals and experiment artifacts

## Custom distribution direction

Because this is our fork, we can customize it beyond minimal integration:

- rewrite the README for CHMARL/Tomorrow
- add CHMARL docs under `docs/`
- add recipes under `recipes/`
- add MCP tools under `extensions/`
- add CHMARL-specific scripts under `scripts/chmarl/`
- eventually rebrand the desktop app and default prompts
- eventually ship a preconfigured distribution with CHMARL extensions enabled

## Engineering guardrails

We can modify the fork freely, but changes should still be reviewable:

- keep generated experiment outputs out of git unless intentionally published
- keep upstream license and attribution
- avoid claiming an algorithm is fully implemented when it is a wrapper, placeholder, or fallback
- distinguish direct emissions data from fuel/emission proxies
- prefer small, named tools and recipes over one large opaque assistant mode

## Current files added by this fork

```text
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md

docs/
  CHMARL_TOMORROW_ROADMAP.md
  TOMORROW_WORKFLOWS.md
  PAPER_TO_CODE_TRACEABILITY.md

recipes/
  chmarl-paper-assistant.yaml
  chmarl-experiment-analyst.yaml
  chmarl-repo-maintainer.yaml
  chmarl-tomorrow-planner.yaml

extensions/
  chmarl-results-mcp/
    README.md
    requirements.txt
    chmarl_results_mcp.py

scripts/
  chmarl/
    README.md
    run_ablation_matrix.sh
    summarize_results.py
```
