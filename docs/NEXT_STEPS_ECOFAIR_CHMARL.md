# Next steps for EcoFairCHAMRL

This document identifies the next engineering work that belongs in the core CHMARL repository rather than the Goose fork.

Core CHMARL repository:

```text
https://github.com/alqithami/EcoFairCHAMRL
```

Goose fork:

```text
https://github.com/alqithami/goose
```

## Boundary

Use `alqithami/goose` for assistant workflows, MCP tools, reporting, recipes, and documentation support.

Use `alqithami/EcoFairCHAMRL` for the actual MARL simulator, environment dynamics, training logic, baselines, metrics, reproducibility, and generated experiment outputs.

## Priority 1: Packaging and installation

Add one of:

```text
requirements.txt
pyproject.toml
```

Minimum expected dependencies based on the current single-file implementation:

```text
gymnasium
numpy
pandas
matplotlib
stable-baselines3
```

Optional dependencies should be clearly marked, especially if they affect baseline availability.

## Priority 2: Unit tests for metrics

Add:

```text
tests/test_metrics.py
```

Cover:

```text
compute_gini([] or zero vector)
compute_gini(equal values)
compute_gini(skewed values)
compute_minmax_ratio(zero vector)
compute_minmax_ratio(equal values)
compute_minmax_ratio(skewed values)
```

These tests are low-cost and high-value because fairness claims rely on these functions.

## Priority 3: Environment smoke tests

Add:

```text
tests/test_env_step.py
```

Cover:

```text
environment reset returns valid observation
environment step returns expected Gym/Gymnasium tuple
emission cap penalty applies when budget is exceeded
fairness penalty applies when fairness is enabled
queue transition occurs when a port is full
weather-off mode behaves deterministically given a seed
```

## Priority 4: Deterministic seed support

Add CLI flags such as:

```bash
--seed 123
--num_seeds 3
```

Each experiment output directory should store metadata such as:

```text
seed
algorithm
episodes
num_ports
num_vessels
emission_cap_enabled
fairness_enabled
lambda_fair
hl_update_interval
commit_sha
created_at
```

Suggested metadata file:

```text
experiment_config.json
```

## Priority 5: Result directory convention

Adopt a consistent output layout:

```text
results/
  baseline/seed_001/
  emission_cap/seed_001/
  fairness/seed_001/
  emission_fairness/seed_001/
  soto/seed_001/
  fen/seed_001/
  aggregate_summary.csv
  report.md
```

This structure works well with the CHMARL MCP server in the Goose fork.

## Priority 6: Baseline/fallback clarification

Document each algorithm as one of:

```text
implemented
wrapper/simplified baseline
optional dependency
placeholder/fallback
not yet implemented
```

Be especially careful with:

```text
QMIX
MAPPO
SOTO
FEN
```

Do not publish full baseline claims unless the code contains verified implementations and generated outputs.

## Priority 7: Paper-to-code traceability

Move from the stub in the Goose fork to a source-of-truth document in EcoFairCHAMRL:

```text
docs/paper_to_code_traceability.md
```

Each row should include:

```text
paper claim
paper section
source file/function
status
repro command
result artifact
test coverage
caveats
```

## Priority 8: Modularization

Refactor the single-file implementation into a package:

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
```

Suggested migration order:

1. Move metric functions first.
2. Add tests for metrics.
3. Move data generation helpers.
4. Move environment class.
5. Move wrappers and training functions.
6. Move CLI last.

## Priority 9: Real outputs for Goose MCP

Once experiments run, connect the Goose MCP server to the real output directory:

```bash
python extensions/chmarl-mcp/chmarl_mcp.py \
  --repo-dir /path/to/EcoFairCHAMRL \
  --results-dir /path/to/EcoFairCHAMRL/results \
  --report-dir /path/to/EcoFairCHAMRL/results/reports
```

Then use Goose to generate:

```text
experiment reports
missing-output checks
metric comparisons
fairness rankings
paper-to-code notes
website summaries for chmarl.com
```

## Recommended first PR in EcoFairCHAMRL

Create a small first PR with:

```text
requirements.txt
pytest configuration
tests/test_metrics.py
README test instructions
```

This creates a stable base before larger refactors.
