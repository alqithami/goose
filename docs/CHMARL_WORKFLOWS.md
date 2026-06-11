# CHMARL workflows for Goose

This document describes practical workflows for using the CHMARL Goose fork with the EcoFair-CH-MARL project.

## Workflow 1: Understand the paper

Use `recipes/chmarl-paper-assistant.yaml`.

Recommended prompts:

```text
Explain the EcoFair-CH-MARL paper section by section.

Create a table of paper claims and where each claim should appear in code.

Identify which assumptions are maritime-specific and which can generalize to other logistics or resource-allocation settings.
```

Expected outputs:

- section summary
- equations explained in plain language
- implementation checklist
- reproducibility concerns
- reviewer-style critique

## Workflow 2: Plan ablation experiments

Use `recipes/chmarl-experiment-analyst.yaml` and `scripts/chmarl/run_ablation_matrix.sh`.

Recommended experiment groups:

```text
baseline
emission_cap
fairness
emission_fairness
soto
fen
lambda_sweep
scale_sweep
```

Suggested questions:

```text
Generate a 3-seed ablation matrix for CHMARL with baseline, emission cap, fairness, and emission+fairness settings.

Create a naming convention for result directories.

Which metrics should I compare for fairness versus throughput trade-offs?
```

## Workflow 3: Analyze CSV results

Use the MCP extension in `extensions/chmarl-results-mcp/` or the helper script `scripts/chmarl/summarize_results.py`.

The expected CSV files include:

```text
results_<algo>.csv
fairness_metrics_<algo>.csv
training_fairness_metrics_<algo>.csv
ppo_only_test_returns.csv
```

Recommended prompts:

```text
Summarize the CHMARL results in this results directory.

Compare baseline, fairness, and emission-cap runs.

Which setting improves Gini the most, and what happens to average return?
```

## Workflow 4: Maintain the core CHMARL codebase

Use `recipes/chmarl-repo-maintainer.yaml`.

Recommended tasks:

```text
Refactor EcoFairCHMARL.py into modules.

Add tests for compute_gini and compute_minmax_ratio.

Create a deterministic seed plan for experiments.

Separate implemented algorithms from placeholders and fallback logic.
```

## Workflow 5: Prepare chmarl.com content

Use `recipes/chmarl-project-planner.yaml`.

Recommended prompts:

```text
Draft a public-facing explanation of EcoFair-CH-MARL for chmarl.com.

Turn this experiment summary into a website update.

Create figure captions for the fairness and emissions trade-off plots.
```

Expected outputs:

- homepage summary
- method explainer
- result story
- reproducibility note
- demo script
- FAQ

## Workflow 6: Plan CHMARL extensions

Use CHMARL as the first research anchor, then expand the assistant workflow to adjacent domains:

- sustainable maritime logistics
- port congestion management
- fleet routing
- energy-grid dispatch
- warehouse/logistics scheduling
- constrained resource allocation
- fairness-aware public-sector decision systems

Recommended prompts:

```text
How can the CHMARL framework generalize beyond maritime logistics?

Create a CHMARL research roadmap.

Which future demos would make chmarl.com more useful?
```

## Workflow 7: Build a custom desktop distribution

Future steps:

1. Rename the desktop product.
2. Add CHMARL icons and splash assets.
3. Bundle CHMARL recipes.
4. Bundle the CHMARL results MCP extension.
5. Add default project instructions.
6. Prepare a release build with a CHMARL suffix.

Candidate name:

```text
CHMARL Goose
```

## Operating principle

Use Goose as the assistant and orchestration layer. Keep the core algorithmic research code in `EcoFairCHAMRL`. Publish public-facing explanations through `chmarl.com`.
