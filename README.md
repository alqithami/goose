# CHMARL Goose

_An agentic research assistant distribution for EcoFair-CH-MARL, maritime logistics, emission-budgeted reinforcement learning, and fairness-aware multi-agent experimentation._

This repository is a project-specific fork of Goose. It keeps the Goose desktop app, CLI, API, provider ecosystem, and MCP extension architecture, but reorients the fork toward CHMARL research workflows.

The goal is to make this fork useful for the CHMARL project rather than merely mirror upstream Goose.

## Project context

CHMARL Goose is designed to support the broader CHMARL ecosystem:

- Project website: https://chmarl.com
- Paper: https://arxiv.org/abs/2603.14625
- Core CHMARL implementation: https://github.com/alqithami/EcoFairCHAMRL
- Upstream Goose project: https://github.com/aaif-goose/goose

The CHMARL simulator and training logic live in `EcoFairCHAMRL`. This fork is the assistant/workflow layer around that project.

## What this fork is for

Use this fork as a local AI research workbench for:

- explaining the EcoFair-CH-MARL paper
- checking paper-to-code alignment
- designing ablation studies
- generating experiment matrices
- reading CHMARL result CSV files
- summarizing Gini, max-min fairness ratio, returns, and fuel/emission proxies
- preparing reproducibility notes
- maintaining the CHMARL codebase
- drafting website/demo copy for `chmarl.com`
- planning future CHMARL research extensions

## Repository additions

This fork adds CHMARL-specific assets on top of Goose:

```text
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md

docs/
  CHMARL_ROADMAP.md
  CHMARL_WORKFLOWS.md
  PAPER_TO_CODE_TRACEABILITY.md

recipes/
  chmarl-paper-assistant.yaml
  chmarl-experiment-analyst.yaml
  chmarl-repo-maintainer.yaml
  chmarl-project-planner.yaml

extensions/
  chmarl-results-mcp/
    README.md
    requirements.txt
    chmarl_results_mcp.py

scripts/
  chmarl/
    README.md
    run_ablation_matrix.sh
    summarize_results.py
```

## Recommended project architecture

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

## Quick start for CHMARL work

Install or run Goose using the standard upstream development flow, then use the CHMARL recipes and MCP extension in this fork.

### 1. Run the Goose desktop app from source

```bash
git clone https://github.com/alqithami/goose.git
cd goose
source ./bin/activate-hermit
cd ui/desktop
pnpm install
pnpm run start
```

### 2. Clone the CHMARL implementation next to this fork

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

### 3. Run CHMARL experiments

From the CHMARL repository:

```bash
python EcoFairCHMARL.py --episodes 2000 --outdir results/baseline
python EcoFairCHMARL.py --emission_cap --episodes 2000 --outdir results/emission_cap
python EcoFairCHMARL.py --fairness --episodes 2000 --outdir results/fairness
python EcoFairCHMARL.py --emission_cap --fairness --episodes 2000 --outdir results/emission_fairness
python EcoFairCHMARL.py --algo SOTO --episodes 2000 --outdir results/soto
python EcoFairCHMARL.py --algo FEN --episodes 2000 --outdir results/fen
```

### 4. Connect Goose to CHMARL results

Use the starter MCP extension:

```bash
cd goose/extensions/chmarl-results-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python chmarl_results_mcp.py --results-dir ../../EcoFairCHAMRL/results
```

Then register the extension in Goose as a stdio MCP extension.

## CHMARL recipes

The recipes are intended to create repeatable assistant modes.

### `chmarl-paper-assistant.yaml`

Use this for paper explanation, related-work synthesis, equation walkthroughs, paper-to-code comparison, reviewer-style critique, and reproducibility checks.

### `chmarl-experiment-analyst.yaml`

Use this for reading CSV outputs, summarizing returns and fairness metrics, comparing ablation settings, and preparing result tables and figure captions.

### `chmarl-repo-maintainer.yaml`

Use this for refactoring `EcoFairCHMARL.py`, adding tests, improving packaging, creating reproducible experiment scripts, and separating implemented algorithms from placeholders.

### `chmarl-project-planner.yaml`

Use this for roadmap planning, website/demo ideas, next-paper directions, future extensions beyond maritime logistics, and deployment-oriented research planning.

## Fork strategy

Because this repository is now a project-specific fork, we do not need to keep every change minimal or upstream-neutral. We can safely add:

- CHMARL branding
- custom README content
- project-specific docs
- Goose recipes
- MCP extensions
- helper scripts
- default workflows
- future custom UI/desktop branding

We should still keep a clear boundary between:

- **Goose platform code**: Rust/Electron/CLI/API framework inherited from upstream.
- **CHMARL assistant layer**: project-specific recipes, docs, MCP tools, and workflows.
- **CHMARL algorithm code**: the simulator and training code in `EcoFairCHAMRL`.

## Next engineering targets

1. Build a richer CHMARL MCP server that can read experiment configs, CSV files, generated plots, and paper metadata.
2. Add result comparison tools for baseline versus fairness/emission-cap runs.
3. Add a traceability matrix from paper claims to implementation files and tests.
4. Add a custom Goose distribution profile for CHMARL providers, recipes, and extensions.
5. Rebrand desktop icons, default prompts, and bundled extensions for a CHMARL Goose distribution.
6. Add documentation workflows for publishing summaries to `chmarl.com`.

## Upstream attribution

This fork is based on Goose, an open-source AI agent project now under the Agentic AI Foundation at the Linux Foundation. The upstream project remains available at https://github.com/aaif-goose/goose.

Goose is licensed under Apache License 2.0. This fork preserves upstream license and attribution while adding CHMARL-specific project assets.
