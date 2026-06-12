# CHMARL results MCP extension

This is the original lightweight starter MCP extension for inspecting EcoFair-CH-MARL experiment outputs from Goose.

For new work, prefer the richer CHMARL MCP server at:

```text
extensions/chmarl-mcp/
```

That newer server includes experiment discovery, result summarization, comparison, missing-output checks, ablation planning, markdown reporting, and paper-to-code traceability support.

This lightweight extension remains useful as a minimal reference implementation.

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
- Prefer `extensions/chmarl-mcp/` for the main CHMARL Goose integration path.
