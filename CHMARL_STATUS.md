# CHMARL Goose status

This is the status handoff for the `alqithami/goose` fork.

## Purpose

This fork is the Goose-based assistant and workflow layer for CHMARL. The core CHMARL simulator and training code remain in `alqithami/EcoFairCHAMRL`.

## Key links

- Project site: https://chmarl.com
- Core code: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose: https://github.com/aaif-goose/goose
- Paper: https://arxiv.org/abs/2603.14625

## Fork update policy

The working CHMARL Goose repository is:

```text
alqithami/goose
```

Policy and operations docs:

```text
FORK_POLICY.md
docs/REPOSITORY_OPERATIONS.md
```

Use this fork for CHMARL Goose updates. Use `alqithami/EcoFairCHAMRL` for core algorithm work.

## Added assets

Documentation:

```text
FORK_POLICY.md
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
CHMARL_STATUS.md
docs/CHMARL_ROADMAP.md
docs/CHMARL_WORKFLOWS.md
docs/PAPER_TO_CODE_TRACEABILITY.md
docs/NEXT_STEPS_ECOFAIR_CHMARL.md
docs/REPOSITORY_OPERATIONS.md
```

Recipes:

```text
recipes/chmarl-paper-assistant.yaml
recipes/chmarl-experiment-analyst.yaml
recipes/chmarl-repo-maintainer.yaml
recipes/chmarl-project-planner.yaml
```

Preferred MCP server:

```text
extensions/chmarl-mcp/
```

Legacy minimal MCP scaffold:

```text
extensions/chmarl-results-mcp/
```

Helper scripts:

```text
scripts/chmarl/run_ablation_matrix.sh
scripts/chmarl/summarize_results.py
```

## Validate the CHMARL MCP server

```bash
cd extensions/chmarl-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
pytest
```

## Boundary

Keep assistant workflows, MCP tools, documentation, reports, and recipes in this Goose fork.

Keep the MARL environment, training loops, baselines, metrics, tests, and real experiment outputs in `EcoFairCHAMRL`.

## Next target

The next major engineering effort should move to:

```text
https://github.com/alqithami/EcoFairCHAMRL
```

See:

```text
docs/NEXT_STEPS_ECOFAIR_CHMARL.md
```
