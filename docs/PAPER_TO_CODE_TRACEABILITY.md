# EcoFair-CH-MARL paper-to-code traceability

This document tracks how paper claims should map to implementation artifacts in `alqithami/EcoFairCHAMRL` and assistant workflows in this Goose fork.

Use this as a living document. Every major paper claim should eventually point to source files, tests, experiment commands, and result artifacts.

## Status labels

| Status | Meaning |
|---|---|
| Implemented | Clear implementation exists and is testable. |
| Partially implemented | Main idea exists, but there are limitations or missing pieces. |
| Simplified prototype | A simplified version exists, but it is not yet the full research claim. |
| Placeholder/fallback | The interface exists but falls back to another method or is not a true implementation. |
| Missing | No clear implementation found yet. |
| Needs verification | Requires manual review or author confirmation. |

## Traceability matrix

| Paper/project claim | Expected implementation location | Current evidence to check | Status | Next action |
|---|---|---|---|---|
| Constrained hierarchical MARL framework | `EcoFairCHMARL.py`, future `chmarl/env.py`, `chmarl/train.py` | High-level directive interval plus low-level speed action | Partially implemented | Separate hierarchy into explicit high-level and low-level modules. |
| Real-time emission budget | Environment reward logic | `emission_cap_enabled`, `emission_cap_value`, `gamma_emis` | Partially implemented | Add tests for cap violation and penalty scaling. |
| Fairness-aware reward shaping | Metrics and reward wrapper code | Gini and max-min ratio functions, SOTO/FEN wrappers | Partially implemented | Add tests and document whether each wrapper matches paper equations. |
| Gini coefficient metric | Metrics helper | `compute_gini` | Implemented | Add unit tests for zero, equal, skewed, and random vectors. |
| Max-min fairness ratio | Metrics helper | `compute_minmax_ratio` | Implemented | Add unit tests for zero, equal, and skewed vectors. |
| Maritime digital twin | Environment dynamics | ports, vessels, distance matrix, queues, weather, fuel curves | Simplified prototype | Document assumptions and compare against real maritime operations. |
| Dynamic port congestion | Environment step logic | port capacity and queuing state | Partially implemented | Add tests for full-port behavior and queue transitions. |
| Stochastic weather | Environment step logic | storm probability, speed penalty, fuel factor | Partially implemented | Add deterministic seed tests for weather-off and weather-on modes. |
| Scalability to ports and vessels | CLI/config | `--num_ports`, `--num_vessels` | Needs verification | Add benchmark script and runtime/memory notes. |
| PPO baseline | Training code | Stable-Baselines3 PPO usage | Implemented | Add reproducible config and seed handling. |
| SOTO baseline | Wrapper code | reward wrapper applying fairness penalty | Simplified prototype | Document if wrapper fully matches cited SOTO method. |
| FEN baseline | Wrapper code | reward wrapper applying `1 - max_min_ratio` | Simplified prototype | Document if wrapper fully matches cited FEN method. |
| QMIX baseline | Optional dependency discovery | May fall back to PPO | Placeholder/fallback | Avoid claiming full QMIX results unless true implementation is verified. |
| MAPPO baseline | Optional dependency discovery | May fall back to PPO | Placeholder/fallback | Avoid claiming full MAPPO results unless true implementation is verified. |
| Convergence approximation | Toy convergence script | `run_convergence_approx` | Simplified prototype | Label as conceptual demonstration, not full convergence proof. |
| Experiment CSV outputs | Training/evaluation code | `results_*.csv`, `fairness_metrics_*.csv`, `training_fairness_metrics_*.csv` | Implemented | Add schema documentation and aggregation utilities. |
| chmarl.com result story | Website/public docs | Future generated summaries | Missing | Add workflow to generate website-ready result summaries. |

## Required tests

Suggested minimum tests for the core CHMARL repository:

```text
tests/test_metrics.py
  test_gini_zero_vector
  test_gini_equal_values
  test_gini_skewed_values
  test_minmax_zero_vector
  test_minmax_equal_values
  test_minmax_skewed_values

tests/test_env_step.py
  test_reset_observation_shape
  test_step_returns_expected_tuple
  test_emission_cap_penalty_applies
  test_fairness_penalty_applies
  test_queue_transition_when_port_full

tests/test_cli.py
  test_default_args
  test_convergence_flag
  test_algorithm_choices
```

## Experiment traceability

Each published result should eventually include:

```text
claim_id: short identifier
paper_section: section or paragraph
code_version: commit SHA
command: exact command used
seed: integer seed
output_dir: result path
metrics: CSV files and columns
figure: generated plot path
status: reproduced / partial / failed / pending
notes: assumptions and caveats
```

## Goose fork responsibilities

This Goose fork should help maintain this document by:

- reading paper claims
- inspecting repository files
- generating missing traceability rows
- checking whether output files exist
- summarizing metric trends
- drafting reproducibility notes
- preparing public summaries for `chmarl.com`

## Review rule

Do not mark a claim as implemented because it appears in the README or paper. Mark it implemented only when source code, tests, and reproducible experiment outputs support it.
