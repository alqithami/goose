# CHMARL MCP server

This is the richer CHMARL Model Context Protocol server for the `alqithami/goose` fork.

It is designed to connect Goose to the EcoFair-CH-MARL research workspace and help with:

- experiment discovery
- CSV result summarization
- experiment comparison
- missing-output detection
- markdown report generation
- ablation command planning
- CHMARL repository inspection
- paper-to-code traceability support

The server does **not** train models or execute arbitrary experiment commands. It reads local project files and generates summaries/plans that Goose can use.

## Recommended workspace

```text
workspace/
  goose/
    extensions/chmarl-mcp/
  EcoFairCHAMRL/
    EcoFairCHMARL.py
    results/
```

## Install

```bash
cd extensions/chmarl-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For development and tests:

```bash
pip install -r dev-requirements.txt
```

## Run

```bash
python chmarl_mcp.py \
  --repo-dir /absolute/path/to/EcoFairCHAMRL \
  --results-dir /absolute/path/to/EcoFairCHAMRL/results \
  --report-dir /absolute/path/to/EcoFairCHAMRL/results/reports
```

## Test

This directory includes small sample CHMARL result fixtures under:

```text
examples/sample_results/
```

Run tests locally with:

```bash
cd extensions/chmarl-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
pytest
```

The tests exercise repository inspection, experiment discovery, CSV schema inspection, metric summaries, experiment comparisons, ranking, missing-output detection, ablation planning, traceability stubs, and markdown report generation.

## Example Goose extension configuration

An example configuration is available at:

```text
example_goose_extension.yaml
```

Equivalent inline configuration:

```yaml
extensions:
  - type: stdio
    name: chmarl
    cmd: python
    args:
      - /absolute/path/to/goose/extensions/chmarl-mcp/chmarl_mcp.py
      - --repo-dir
      - /absolute/path/to/EcoFairCHAMRL
      - --results-dir
      - /absolute/path/to/EcoFairCHAMRL/results
      - --report-dir
      - /absolute/path/to/EcoFairCHAMRL/results/reports
    description: Analyze EcoFair-CH-MARL experiments and repository artifacts.
```

## Tools

### `chmarl_healthcheck`

Returns configured paths and whether they exist.

### `inspect_chmarl_repo`

Inspects the CHMARL repository for key files such as `EcoFairCHMARL.py`, README, packaging files, tests, and result directories.

### `list_chmarl_result_files`

Lists detected CHMARL CSV result files under the configured result directory.

### `list_chmarl_experiments`

Groups result files into experiment-like directories.

### `inspect_chmarl_schema`

Returns row count, columns, and numeric columns for a selected CSV file.

### `summarize_chmarl_file`

Returns numeric descriptive statistics for a selected CSV file.

### `summarize_chmarl_results`

Summarizes all detected result files, or files under a selected experiment directory.

### `compare_chmarl_experiments`

Compares experiments using a selected metric such as `return`, `gini`, or `max_min_ratio`.

### `rank_chmarl_runs`

Ranks files/runs by a selected metric.

### `detect_missing_chmarl_outputs`

Checks expected experiment directories and expected output files.

### `create_chmarl_ablation_plan`

Generates a reproducible shell command matrix for baseline, emission cap, fairness, SOTO, and FEN runs.

### `generate_chmarl_markdown_report`

Writes a markdown summary report to the configured report directory.

### `paper_to_code_traceability_stub`

Returns a starter traceability matrix connecting CHMARL paper claims to implementation checks.

## Relationship to `chmarl-results-mcp`

`extensions/chmarl-results-mcp/` is the earlier lightweight scaffold. It can remain as a simple example, but this `extensions/chmarl-mcp/` server is the preferred CHMARL integration path going forward.

## Notes

- If a CSV file does not contain direct emissions columns, Goose should describe fuel as a proxy rather than direct emissions measurement.
- QMIX and MAPPO should not be reported as implemented unless the CHMARL repository contains verified implementations and generated outputs.
- The MCP server is designed for analysis and reporting first; keep execution/training in the EcoFairCHAMRL repository or explicit scripts.
