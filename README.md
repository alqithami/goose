# CHMARL Goose

_An agentic research assistant distribution for EcoFair-CH-MARL, maritime logistics, emission-budgeted reinforcement learning, and fairness-aware multi-agent experimentation._

This repository is a project-specific fork of Goose. It keeps the Goose desktop app, CLI, API, provider ecosystem, and MCP extension architecture, but reorients the fork toward CHMARL research workflows.

## Start here

The current handoff/status document is:

```text
CHMARL_STATUS.md
```

It explains what has been added, which MCP server is preferred, how to validate it, and what should move next to the core `EcoFairCHAMRL` repository.

## Project context

- Project website: https://chmarl.com
- Paper: https://arxiv.org/abs/2603.14625
- Core CHMARL implementation: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose project: https://github.com/aaif-goose/goose

The CHMARL simulator and training logic live in `EcoFairCHAMRL`. This fork is the assistant/workflow layer around that project.

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
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
CHMARL_STATUS.md

docs/
  CHMARL_ROADMAP.md
  CHMARL_WORKFLOWS.md
  NEXT_STEPS_ECOFAIR_CHMARL.md
  PAPER_TO_CODE_TRACEABILITY.md

recipes/
  chmarl-paper-assistant.yaml
  chmarl-experiment-analyst.yaml
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
  Core constrained hierarchical MARL simulator, training scripts,
  fairness metrics, emission-budget logic, and experiment outputs.

alqithami/goose
  CHMARL Goose assistant distribution: recipes, MCP tools,
  experiment analysis, code review, documentation, and workflow automation.

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

Clone the CHMARL implementation next to this fork:

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

- `chmarl-paper-assistant.yaml`: paper explanation, equations, paper-to-code comparison, reproducibility checks.
- `chmarl-experiment-analyst.yaml`: CSV summaries, ablation comparisons, result tables, figure captions.
- `chmarl-repo-maintainer.yaml`: refactoring, packaging, tests, algorithm/fallback clarity.
- `chmarl-project-planner.yaml`: roadmap, demo ideas, next-paper directions, and project planning.

## Next engineering target

The next major engineering work should move to:

```text
https://github.com/alqithami/EcoFairCHAMRL
```

See:

```text
docs/NEXT_STEPS_ECOFAIR_CHMARL.md
```

## Upstream attribution

This fork is based on Goose, an open-source AI agent project now under the Agentic AI Foundation at the Linux Foundation. The upstream project remains available at https://github.com/aaif-goose/goose.

Goose is licensed under Apache License 2.0. This fork preserves upstream license and attribution while adding CHMARL-specific project assets.
