# CHMARL Goose status

This is the status handoff for the `alqithami/goose` fork.

## Purpose

This fork is the Goose-based assistant and workflow layer for CHMARL. EcoFairCHMARL remains a separate external project that Goose can inspect and analyze through local files and result outputs.

## Key links

- Project site: https://chmarl.com
- External CHMARL code reference: https://github.com/alqithami/EcoFairCHAMRL
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
docs/ECOFAIR_CHMARL_EXTERNAL_INTEGRATION.md
```

Use this fork for CHMARL Goose updates. Treat `alqithami/EcoFairCHAMRL` as an external/read-only integration target unless explicitly instructed otherwise.

## Added assets

Documentation:

```text
FORK_POLICY.md
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
CHMARL_STATUS.md
docs/CHMARL_ROADMAP.md
docs/CHMARL_WORKFLOWS.md
docs/ECOFAIR_CHMARL_EXTERNAL_INTEGRATION.md
docs/PAPER_TO_CODE_TRACEABILITY.md
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

Do not modify EcoFairCHMARL from this Goose integration workflow unless the user explicitly requests changes to that repository.

## Next target inside this fork

Continue improving the Goose-side integration layer:

```text
extensions/chmarl-mcp/
recipes/
docs/
scripts/chmarl/
```

Possible next additions:

- richer markdown experiment reports
- website-ready result summaries
- CHMARL paper-review recipes
- MCP output templates for chmarl.com
- desktop branding refinements
