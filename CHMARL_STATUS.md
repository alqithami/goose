# CHMARL Goose status

This is the status handoff for the `alqithami/goose` fork.

## Purpose

This fork is now the Goose-based assistant, workflow, and research-prototype layer for CHMARL. EcoFairCHMARL remains a separate external project that Goose can inspect and analyze through local files and result outputs.

## Current research direction

The primary research direction is now:

```text
CHMARL-Goose: agentic constrained hierarchical MARL for maritime digital twins.
```

This direction treats:

```text
vessels as tool-using agents,
ports as service/capacity agents,
emission budgets as governance agents,
fairness objectives as governance agents,
MARL as the optimization backbone.
```

Research files:

```text
research/chmarl-goose/README.md
research/chmarl-goose/ARCHITECTURE.md
research/chmarl-goose/METHOD.md
research/chmarl-goose/EVALUATION_PLAN.md
research/chmarl-goose/chmarl_goose_runtime.py
research/chmarl-goose/examples/sample_fleet.json
```

Run the executable scaffold:

```bash
python research/chmarl-goose/chmarl_goose_runtime.py --steps 5 --out reports/chmarl_goose_trace.json
```

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

Research prototype:

```text
research/chmarl-goose/
```

Schemas:

```text
schemas/chmarl_goose_agent.schema.json
schemas/chmarl_goose_episode.schema.json
schemas/chmarl_goose_claim_evidence.schema.json
```

Recipes:

```text
recipes/chmarl-goose-researcher.yaml
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

Keep assistant workflows, MCP tools, documentation, reports, research prototypes, schemas, and recipes in this Goose fork.

Do not modify EcoFairCHMARL from this Goose integration workflow unless the user explicitly requests changes to that repository.

## Next target inside this fork

Continue improving CHMARL-Goose as a research prototype:

```text
research/chmarl-goose/
extensions/chmarl-mcp/
recipes/
docs/
scripts/chmarl/
```

Possible next additions:

- connect the runtime scaffold to the MCP server,
- generate claim-evidence graphs from traces,
- add learned policies behind vessel agents,
- produce reviewer-ready artifact reports,
- generate website-ready result summaries,
- evaluate CHMARL-Goose against baseline CHMARL outputs.
