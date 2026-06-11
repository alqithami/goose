# CHMARL results MCP extension

This is a starter MCP extension for inspecting EcoFair-CH-MARL experiment outputs from Goose.

It is intentionally small and external to Goose core. The CHMARL simulator and training code should remain in the `EcoFairCHAMRL` repository; this extension helps Goose summarize generated result files.

## Expected inputs

Point the extension at a directory containing CHMARL output files such as:

- `results_<algo>.csv`
- `fairness_metrics_<algo>.csv`
- `training_fairness_metrics_<algo>.csv`

## Install

```bash
cd extensions/chmarl-results-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python chmarl_results_mcp.py --results-dir /path/to/EcoFairCHAMRL/results
```

## Example Goose extension configuration

```yaml
extensions:
  - type: stdio
    name: chmarl-results
    cmd: python
    args:
      - /absolute/path/to/goose/extensions/chmarl-results-mcp/chmarl_results_mcp.py
      - --results-dir
      - /absolute/path/to/EcoFairCHAMRL/results
    description: Analyze EcoFair-CH-MARL experiment CSV outputs.
```

## Tools provided

### `list_chmarl_result_files`

Lists CSV files found in the configured results directory.

### `summarize_chmarl_results`

Reads CHMARL CSV outputs and returns compact descriptive statistics for numeric columns.

## Notes

- This scaffold summarizes numeric CSV data only.
- It does not train CHMARL models.
- It treats available CSV columns literally; if emissions are not stored as a direct column, the assistant should not claim direct emissions analysis.
- It is a starting point for a richer CHMARL-specific MCP server.
