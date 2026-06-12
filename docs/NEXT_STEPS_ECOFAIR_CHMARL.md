# Next steps for EcoFairCHAMRL

This document lists the next engineering work that belongs in the core CHMARL repository.

Core repository:

```text
https://github.com/alqithami/EcoFairCHAMRL
```

Goose fork:

```text
https://github.com/alqithami/goose
```

## Boundary

Use the Goose fork for assistant workflows, MCP tools, reporting, recipes, and documentation support.

Use `EcoFairCHAMRL` for the actual MARL simulator, environment dynamics, training logic, baselines, metrics, tests, reproducibility, and generated experiment outputs.

## Priority 1: Packaging

Add one of:

```text
requirements.txt
pyproject.toml
```

Expected dependencies include:

```text
gymnasium
numpy
pandas
matplotlib
stable-baselines3
```

Optional dependencies should be clearly marked.

## Priority 2: Metric tests

Add:

```text
tests/test_metrics.py
```

Cover:

```text
compute_gini zero vector
compute_gini equal values
compute_gini skewed values
compute_minmax_ratio zero vector
compute_minmax_ratio equal values
compute_minmax_ratio skewed values
```

## Priority 3: Environment smoke tests

Add:

```text
tests/test_env_step.py
```

Cover:

```text
reset returns a valid observation
step returns the expected Gym/Gymnasium tuple
emission cap penalty applies
fairness penalty applies
queue transition occurs when a port is full
weather-off mode behaves deterministically with a seed
```

## Priority 4: Seed support

Add CLI flags such as:

```bash
--seed 123
--num_seeds 3
```

Each run should save metadata such as:

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

Suggested output layout:

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

## Priority 6: Baseline and fallback clarity

Document each algorithm as one of:

```text
implemented
wrapper or simplified baseline
optional dependency
placeholder or fallback
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

Add a source-of-truth document in EcoFairCHAMRL:

```text
docs/paper_to_code_traceability.md
```

Each row should include:

```text
paper claim
paper section
source file or function
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

## Priority 9: Connect real outputs to Goose

After experiments run, connect the Goose MCP server to the real result directory:

```bash
python extensions/chmarl-mcp/chmarl_mcp.py \
  --repo-dir /path/to/EcoFairCHAMRL \
  --results-dir /path/to/EcoFairCHAMRL/results \
  --report-dir /path/to/EcoFairCHAMRL/results/reports
```

Then use Goose to generate experiment reports, metric comparisons, missing-output checks, fairness rankings, traceability notes, and website summaries.

## Recommended first PR in EcoFairCHAMRL

Start with:

```text
requirements.txt
pytest configuration
tests/test_metrics.py
README test instructions
```

This creates a stable base before larger refactors.
