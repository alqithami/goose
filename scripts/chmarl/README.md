# CHMARL helper scripts

This directory contains helper scripts for using the Goose fork with the EcoFair-CH-MARL implementation.

The scripts assume a local workspace similar to:

```text
workspace/
  goose/
  EcoFairCHAMRL/
```

## Scripts

### `run_ablation_matrix.sh`

Runs a standard CHMARL ablation matrix against `EcoFairCHMARL.py`.

Example:

```bash
./scripts/chmarl/run_ablation_matrix.sh ../EcoFairCHAMRL 2000 results/chmarl_ablation
```

Arguments:

```text
1. Path to EcoFairCHAMRL repository
2. Number of episodes
3. Output root directory
```

### `summarize_results.py`

Summarizes CHMARL CSV outputs across result directories.

Example:

```bash
python scripts/chmarl/summarize_results.py --results-root ../EcoFairCHAMRL/results --out summary.csv
```

The summary includes basic descriptive statistics for numeric columns in files matching:

```text
results_*.csv
fairness_metrics_*.csv
training_fairness_metrics_*.csv
ppo_only_test_returns.csv
```

## Notes

These scripts are intentionally lightweight. They do not replace the CHMARL simulator. They help Goose and researchers run, inspect, and summarize experiment outputs more consistently.
