# CHMARL integration for Goose

This repository can be used as a CHMARL research and workflow assistant around the core EcoFair-CH-MARL implementation.

The goal is not to move the MARL simulator into Goose. Instead, Goose should act as an agentic layer for research support, experiment planning, result analysis, repository maintenance, and public-facing documentation for the CHMARL project.

## Related project assets

- CHMARL project site: https://chmarl.com
- Paper: https://arxiv.org/abs/2603.14625
- Core implementation repository: https://github.com/alqithami/EcoFairCHAMRL

## Recommended architecture

```text
alqithami/EcoFairCHAMRL
  Core simulator, training loop, baselines, fairness metrics, emissions constraints,
  experiment outputs, and reproducibility scripts.

alqithami/goose
  Research assistant, CHMARL-specific recipes, experiment analysis helpers,
  MCP tooling, and workflow automation.

chmarl.com
  Public project website, paper/code gateway, demos, figures, and results narrative.
```

## What Goose should do for CHMARL

### 1. Paper-to-code traceability

Use Goose to inspect whether claims in the paper are represented in code:

- constrained hierarchical MARL structure
- high-level routing decisions
- low-level vessel control decisions
- real-time emission budget logic
- fairness-aware reward transformation
- Gini and max-min fairness metrics
- scalability settings such as ports and vessels
- ablation and baseline experiments

### 2. Experiment planning

Use Goose recipes to generate and run repeatable experiment matrices, for example:

```bash
python EcoFairCHMARL.py --episodes 2000 --outdir results/baseline
python EcoFairCHMARL.py --emission_cap --episodes 2000 --outdir results/emission_cap
python EcoFairCHMARL.py --fairness --episodes 2000 --outdir results/fairness
python EcoFairCHMARL.py --emission_cap --fairness --episodes 2000 --outdir results/emission_fairness
python EcoFairCHMARL.py --algo SOTO --episodes 2000 --outdir results/soto
python EcoFairCHMARL.py --algo FEN --episodes 2000 --outdir results/fen
```

### 3. Result analysis

The EcoFairCHAMRL repository writes CSV files such as:

- `results_<algo>.csv`
- `fairness_metrics_<algo>.csv`
- `training_fairness_metrics_<algo>.csv`

The starter MCP extension in `extensions/chmarl-results-mcp/` is intended to let Goose inspect those files and summarize:

- average return
- Gini coefficient
- max-min fairness ratio
- training trend by episode
- trade-offs between emissions, efficiency, and fairness

### 4. Repository maintenance

Goose can help refactor the core CHMARL implementation into a cleaner research artifact:

```text
chmarl/
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
```

Suggested maintenance priorities:

1. Add `requirements.txt` or `pyproject.toml`.
2. Add deterministic seed handling.
3. Add tests for metrics and environment transitions.
4. Separate implemented baselines from placeholders or fallback behavior.
5. Add a paper-to-code traceability matrix.

## Using the recipes

The `recipes/` directory contains CHMARL-specific Goose recipe drafts:

- `recipes/chmarl-paper-assistant.yaml`
- `recipes/chmarl-experiment-analyst.yaml`
- `recipes/chmarl-repo-maintainer.yaml`

Use them as starting points for Goose sessions focused on paper review, experiment analysis, and repository improvement.

## Using the MCP extension scaffold

The starter extension is intentionally lightweight and external to Goose core:

```bash
cd extensions/chmarl-results-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python chmarl_results_mcp.py --results-dir /path/to/EcoFairCHAMRL/results
```

Then register it as a Goose stdio extension using a configuration similar to:

```yaml
extensions:
  - type: stdio
    name: chmarl-results
    cmd: python
    args:
      - /absolute/path/to/extensions/chmarl-results-mcp/chmarl_results_mcp.py
      - --results-dir
      - /absolute/path/to/EcoFairCHAMRL/results
    description: Analyze EcoFair-CH-MARL experiment CSV outputs.
```

## Scope boundary

Keep CHMARL algorithmic code in `EcoFairCHAMRL`. Keep Goose changes focused on:

- recipes
- documentation
- MCP integration
- workflow automation
- research assistant behavior

This keeps the Goose fork easy to maintain while making it directly useful for the CHMARL project.
