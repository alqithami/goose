# CHMARL Goose

_An agentic research assistant distribution for EcoFair-CH-MARL, maritime logistics, emission-budgeted reinforcement learning, and fairness-aware multi-agent experimentation._

This repository is a project-specific fork of Goose. It keeps the Goose desktop app, CLI, API, provider ecosystem, and MCP extension architecture, but reorients the fork toward CHMARL research workflows.

## Research direction

The most novel direction in this fork is now:

```text
CHMARL-Goose: agentic constrained hierarchical MARL for maritime digital twins.
```

Instead of merely using Goose to summarize CHMARL outputs, CHMARL-Goose treats:

```text
vessels as tool-using agents,
ports as service/capacity agents,
emission budgets as governance agents,
fairness objectives as governance agents,
and MARL as the optimization backbone.
```

Start with:

```text
research/chmarl-goose/README.md
research/chmarl-goose/ARCHITECTURE.md
research/chmarl-goose/METHOD.md
research/chmarl-goose/EVALUATION_PLAN.md
research/chmarl-goose/chmarl_goose_runtime.py
```

Run the executable scaffold:

```bash
python research/chmarl-goose/chmarl_goose_runtime.py --steps 5 --out reports/chmarl_goose_trace.json
```

## Start here

The current handoff/status document is:

```text
CHMARL_STATUS.md
```

Repository update policy and operating guidance live here:

```text
FORK_POLICY.md
docs/REPOSITORY_OPERATIONS.md
docs/ECOFAIR_CHMARL_EXTERNAL_INTEGRATION.md
```

These documents define `alqithami/goose` as the CHMARL Goose source of truth and define EcoFairCHMARL as an external/read-only project reference unless explicitly instructed otherwise.

## Project context

- Project website: https://chmarl.com
- Paper: https://arxiv.org/abs/2603.14625
- Core CHMARL implementation: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose project: https://github.com/aaif-goose/goose

The CHMARL simulator and training logic live in `EcoFairCHAMRL`. This fork is the assistant/workflow layer around that project. Goose should integrate with EcoFairCHMARL by reading local files, results, and metadata; it should not modify EcoFairCHMARL unless explicitly requested.

## Preferred MCP server

Use this for new work:

```text
extensions/chmarl-mcp/
```

It supports repository inspection, experiment discovery, CSV result summarization, metric comparison, run ranking, missing-output checks, ablation planning, markdown report generation, and paper-to-code traceability stubs.

The older minimal scaffold remains here for reference:

```text
extensions/chmarl-results-mcp/
```

## Validate the CHMARL MCP server

```bash
cd extensions/chmarl-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
pytest
```

## Repository additions

```text
FORK_POLICY.md
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
CHMARL_STATUS.md

docs/
  CHMARL_ROADMAP.md
  CHMARL_WORKFLOWS.md
  ECOFAIR_CHMARL_EXTERNAL_INTEGRATION.md
  NEXT_STEPS_ECOFAIR_CHMARL.md
  PAPER_TO_CODE_TRACEABILITY.md
  REPOSITORY_OPERATIONS.md

research/
  chmarl-goose/

schemas/
  chmarl_goose_agent.schema.json
  chmarl_goose_episode.schema.json
  chmarl_goose_claim_evidence.schema.json

recipes/
  chmarl-paper-assistant.yaml
  chmarl-experiment-analyst.yaml
  chmarl-goose-researcher.yaml
  chmarl-repo-maintainer.yaml
  chmarl-project-planner.yaml

extensions/
  chmarl-mcp/
  chmarl-results-mcp/

scripts/
  chmarl/
```

## Recommended architecture

```text
alqithami/EcoFairCHAMRL
  External CHMARL project reference: core simulator, training scripts,
  fairness metrics, emission-budget logic, and experiment outputs.

alqithami/goose
  CHMARL-Goose research prototype plus assistant distribution: recipes,
  MCP tools, agentic constrained-MARL scaffolds, experiment analysis,
  documentation, and workflow automation.

chmarl.com
  Public project site: paper, code, explanations, figures, demos,
  tutorials, and result summaries.
```

## Quick start

Run Goose using the standard upstream development flow:

```bash
git clone https://github.com/alqithami/goose.git
cd goose
source ./bin/activate-hermit
cd ui/desktop
pnpm install
pnpm run start
```

Clone the CHMARL implementation next to this fork as a local external project reference:

```bash
cd ..
git clone https://github.com/alqithami/EcoFairCHAMRL.git
```

A convenient local layout is:

```text
workspace/
  goose/
  EcoFairCHAMRL/
```

## CHMARL recipes

- `chmarl-goose-researcher.yaml`: develop the agentic constrained-MARL research direction.
- `chmarl-paper-assistant.yaml`: paper explanation, equations, paper-to-code comparison, reproducibility checks.
- `chmarl-experiment-analyst.yaml`: CSV summaries, ablation comparisons, result tables, figure captions.
- `chmarl-repo-maintainer.yaml`: repository review and proposed improvements, without modifying EcoFairCHMARL unless explicitly requested.
- `chmarl-project-planner.yaml`: roadmap, demo ideas, next-paper directions, and project planning.

## Next engineering target in this fork

Continue improving CHMARL-Goose as a research prototype:

- connect the runtime scaffold to `extensions/chmarl-mcp/`,
- generate claim-evidence graphs from decision traces,
- add learned policies behind vessel agents,
- add artifact-review reports for top-tier conference evaluation,
- generate website-ready result summaries for `chmarl.com`,
- evaluate against CHMARL baseline outputs.

## Upstream attribution

This fork is based on Goose, an open-source AI agent project now under the Agentic AI Foundation at the Linux Foundation. The upstream project remains available at https://github.com/aaif-goose/goose.

Goose is licensed under Apache License 2.0. This fork preserves upstream license and attribution while adding CHMARL-specific project assets.
