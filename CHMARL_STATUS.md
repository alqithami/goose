# CHMARL Goose status

This document is the handoff/status page for the `alqithami/goose` fork.

## Current purpose

`alqithami/goose` is now a CHMARL-focused Goose fork. It keeps the upstream Goose agent platform while adding CHMARL-specific documentation, recipes, MCP tools, helper scripts, and workflow guidance.

The fork should be used as the assistant and orchestration layer around the EcoFair-CH-MARL project.

## Related repositories and sites

- CHMARL project site: https://chmarl.com
- Core CHMARL code: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose: https://github.com/aaif-goose/goose
- CHMARL paper: https://arxiv.org/abs/2603.14625

## What has been added

### Documentation

```text
README.md
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
CHMARL_STATUS.md
docs/CHMARL_ROADMAP.md
docs/CHMARL_WORKFLOWS.md
docs/PAPER_TO_CODE_TRACEABILITY.md
docs/NEXT_STEPS_ECOFAIR_CHMARL.md
```

### Recipes

```text
recipes/chmarl-paper-assistant.yaml
recipes/chmarl-experiment-analyst.yaml
recipes/chmarl-repo-maintainer.yaml
recipes/chmarl-project-planner.yaml
```

### MCP extensions

Preferred MCP server:

```text
extensions/chmarl-mcp/
```

Legacy/simple scaffold:

```text
extensions/chmarl-results-mcp/
```

### Helper scripts

```text
scripts/chmarl/run_ablation_matrix.sh
scripts/chmarl/summarize_results.py
```

## Preferred MCP server

Use this one for new work:

```text
extensions/chmarl-mcp/chmarl_mcp.py
```

It supports:

- healthcheck
- CHMARL repository inspection
- result-file listing
- experiment grouping
- CSV schema inspection
- file and full-result summarization
- metric comparison and ranking
- missing-output detection
- ablation-plan generation
- markdown report generation
- paper-to-code traceability stubs

The older `extensions/chmarl-results-mcp/` directory remains as a minimal reference, but should not be the main integration path.

## How to validate the MCP server

```bash
cd extensions/chmarl-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
pytest
```

A GitHub Actions workflow also runs the CHMARL MCP tests when relevant files change:

```text
.github/workflows/chmarl-mcp.yml
```

## What belongs in this Goose fork

Keep these in `alqithami/goose`:

- CHMARL assistant recipes
- CHMARL MCP tools
- analysis/reporting helpers
- experiment workflow documentation
- website/demo drafting support
- Goose distribution and branding work

## What belongs in EcoFairCHAMRL

Keep these in `alqithami/EcoFairCHAMRL`:

- MARL environment implementation
- training loops
- fairness metric implementation
- emission-budget mechanics
- baselines
- tests for the simulator
- experiment scripts and real generated outputs
- reproducibility metadata

## Current engineering status

Completed in this fork:

1. Initial CHMARL Goose integration.
2. Rich CHMARL MCP server.
3. MCP test fixtures, pytest coverage, example Goose config, and CI workflow.
4. Repository polish and final handoff docs.

Recommended next repository to improve:

```text
alqithami/EcoFairCHAMRL
```

Recommended next engineering theme:

```text
Make the core CHMARL research code testable, reproducible, and paper-aligned.
```

See:

```text
docs/NEXT_STEPS_ECOFAIR_CHMARL.md
```

## Known caveats

- Fuel-related columns should be described as emissions proxies unless direct emissions columns exist.
- QMIX and MAPPO should not be presented as full baselines unless verified implementations and outputs are present.
- Historical PR #1 contained incorrect `Tomorrow` wording before cleanup. Current `main` branch files are the source of truth and use CHMARL naming.
