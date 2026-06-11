# CHMARL/Tomorrow roadmap

This roadmap describes how the Goose fork should evolve into a CHMARL/Tomorrow research assistant distribution.

## North star

Build a local AI workbench that helps researchers move from CHMARL theory to reproducible experiments, readable results, code maintenance, and public project communication.

The fork should help answer questions like:

- What does the EcoFair-CH-MARL paper claim?
- Where is each claim implemented?
- Which experiments reproduce each result?
- Which ablations are missing?
- How do emission budgets affect return and fairness?
- How do fairness weights affect Gini and max-min ratio?
- What should be published on `chmarl.com`?
- What should be fixed in the core CHMARL repository before release?

## Phase 1: Project-specific assistant layer

Status: in progress.

Goals:

- Rewrite the README for CHMARL/Tomorrow.
- Add CHMARL recipes.
- Add integration documentation.
- Add a starter results-analysis MCP extension.
- Add helper scripts for experiment matrices and CSV summaries.

Deliverables:

```text
README.md
CHMARL_INTEGRATION.md
CUSTOM_CHMARL_DISTRIBUTION.md
recipes/chmarl-*.yaml
extensions/chmarl-results-mcp/
scripts/chmarl/
```

## Phase 2: Reproducible experiment workflows

Goals:

- Standardize experiment directory names.
- Standardize seed handling.
- Add command generators for ablations.
- Add result aggregation utilities.
- Add plot-generation utilities.
- Add experiment metadata files.

Candidate output layout:

```text
EcoFairCHAMRL/results/
  baseline/seed_001/
  emission_cap/seed_001/
  fairness/seed_001/
  emission_fairness/seed_001/
  soto/seed_001/
  fen/seed_001/
  aggregate_summary.csv
  report.md
```

## Phase 3: Paper-to-code traceability

Goals:

- Map paper claims to source files, functions, tests, and experiments.
- Mark each claim as implemented, partially implemented, simplified, missing, or unclear.
- Avoid overstating placeholder baselines.
- Document what is measured directly versus inferred from proxy columns.

Deliverables:

```text
docs/PAPER_TO_CODE_TRACEABILITY.md
scripts/chmarl/create_traceability_stub.py
```

## Phase 4: Rich CHMARL MCP tools

The first MCP extension only summarizes CSV files. A richer extension should provide tools such as:

- `list_experiments`
- `summarize_experiment`
- `compare_experiments`
- `rank_runs_by_fairness`
- `rank_runs_by_return`
- `detect_missing_outputs`
- `generate_markdown_report`
- `prepare_chmarl_site_summary`

The extension should read:

- CSV results
- experiment configuration files
- generated figures
- paper metadata
- README and docs from `EcoFairCHAMRL`

## Phase 5: Custom desktop distribution

Goals:

- Change application metadata from generic Goose to CHMARL/Tomorrow Goose.
- Add CHMARL default recipes.
- Bundle CHMARL MCP extension entries.
- Add icons and splash assets.
- Optionally ship with provider defaults appropriate for the project.

Candidate files to modify:

```text
ui/desktop/package.json
ui/desktop/forge.config.ts
ui/desktop/src/images/
ui/desktop/src/built-in-extensions.json
ui/desktop/src/components/settings/extensions/bundled-extensions.json
crates/goose/src/prompts/system.md
```

## Phase 6: chmarl.com support

Goals:

- Generate project-site summaries from experiment results.
- Draft figure captions.
- Maintain a public-facing explanation of CHMARL.
- Prepare demo walkthroughs.
- Produce reproducibility notes.

Candidate outputs:

```text
site-summary.md
experiment-report.md
figures.md
faq.md
reproducibility.md
```

## Review policy

Because this is a fork, CHMARL-specific changes are allowed. Still, each change should be understandable:

- keep commits focused
- document project-specific defaults
- keep upstream license attribution
- avoid committing large generated results by default
- mark assumptions clearly
- avoid overstating research claims
