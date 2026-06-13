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
research/chmarl-goose/CLAIM_EVIDENCE_GRAPH.md
research/chmarl-goose/DEMO.md
research/chmarl-goose/chmarl_goose_runtime.py
research/chmarl-goose/chmarl_goose_artifact.py
research/chmarl-goose/generate_claim_evidence.py
research/chmarl-goose/examples/sample_fleet.json
research/chmarl-goose/tests/test_chmarl_goose_runtime.py
```

Run the executable scaffold:

```bash
python research/chmarl-goose/chmarl_goose_runtime.py --steps 5 --out reports/chmarl_goose_trace.json
```

Generate claim-evidence artifacts:

```bash
python research/chmarl-goose/generate_claim_evidence.py \
  --trace reports/chmarl_goose_trace.json \
  --out-json reports/chmarl_goose_claim_evidence.json \
  --out-md reports/chmarl_goose_artifact_review.md
```

Run runtime tests:

```bash
python -m pytest research/chmarl-goose/tests
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

Templates:

```text
templates/chmarl_goose_artifact_review.md
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

Keep assistant workflows, MCP tools, documentation, reports, research prototypes, schemas, templates, and recipes in this Goose fork.

Do not modify EcoFairCHMARL from this Goose integration workflow unless the user explicitly requests changes to that repository.

## Current artifact level

The repo now has:

```text
conceptual method
architecture
evaluation plan
executable runtime scaffold
sample fleet configuration
claim-evidence schemas
claim-evidence generation
runtime tests
reviewer demo
artifact-review template
```

It is still not a completed learned MARL method. The next research step is to compare the scaffold and future learned variant against baseline CHMARL outputs.

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
- generate claim-evidence graphs from real CHMARL experiment outputs,
- add learned policies behind vessel agents,
- produce reviewer-ready artifact reports,
- generate website-ready result summaries,
- evaluate CHMARL-Goose against baseline CHMARL outputs.
