# CHMARL-Goose artifact report template

## Run metadata

```text
trace_path:
output_directory:
runtime_commit:
steps:
ports:
vessels:
seed:
```

## Summary metrics

```text
total_fuel:
mean_fuel:
gini:
max_min_ratio:
emission_pressure:
fairness_pressure:
trace_completeness:
governance_interventions:
```

## Claim-evidence table

| Claim ID | Claim | Status | Evidence | Missing evidence | Reviewer note |
|---|---|---|---|---|---|
| C1 |  |  |  |  |  |
| C2 |  |  |  |  |  |

## Falsification tests

```text
1.
2.
3.
```

## Caveats

- This artifact reviews CHMARL-Goose scaffold behavior, not final learned policy performance.
- Fuel is an emissions proxy unless direct emissions are logged.
- Optimization superiority requires matched baselines and multi-seed evaluation.
- Governance pressure improving a metric is not enough; it must not collapse return or throughput.

## Reviewer quick commands

```bash
python research/chmarl-goose/chmarl_goose_runtime.py --steps 5 --out reports/chmarl_goose_trace.json
python research/chmarl-goose/chmarl_goose_artifact.py \
  --trace reports/chmarl_goose_trace.json \
  --out-dir reports/chmarl_goose_artifact
```
