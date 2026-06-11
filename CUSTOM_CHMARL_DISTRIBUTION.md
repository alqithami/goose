# Custom CHMARL/Tomorrow distribution

This fork is a CHMARL/Tomorrow-specific distribution of Goose.

It keeps the upstream Goose agent platform but adds project-specific defaults, recipes, documentation, and MCP tools for EcoFair-CH-MARL research workflows.

## Distribution goals

The customized distribution should help with:

- EcoFair-CH-MARL paper review
- paper-to-code traceability
- maritime logistics experiment planning
- fairness and emissions result analysis
- CHMARL repository maintenance
- website/demo material for `chmarl.com`
- long-term Tomorrow-facing research planning

## Recommended local workspace

```text
workspace/
  goose/              # this fork
  EcoFairCHAMRL/      # core CHMARL implementation
  chmarl.com/         # website/project material, if local
```

## Default assistant identity

This fork should identify itself as a Goose-based CHMARL/Tomorrow assistant. It should still be able to help with general coding and automation, but its default project context is:

- constrained hierarchical multi-agent reinforcement learning
- maritime logistics
- emission budgets
- fairness-aware reward shaping
- reproducible experiments
- result analysis
- research communication

## Default extensions

Recommended bundled extensions:

```yaml
extensions:
  - type: stdio
    name: chmarl-results
    cmd: python
    args:
      - /absolute/path/to/goose/extensions/chmarl-results-mcp/chmarl_results_mcp.py
      - --results-dir
      - /absolute/path/to/EcoFairCHAMRL/results
    description: Analyze EcoFair-CH-MARL result CSV files.
```

Future extensions can include:

- `chmarl-paper-mcp`: index and query the arXiv paper, notes, and reviewer responses
- `chmarl-code-mcp`: inspect the EcoFairCHAMRL repo structure and run smoke tests
- `chmarl-site-mcp`: draft and publish project-site updates
- `chmarl-experiment-mcp`: create and run experiment matrices from YAML configs

## Recommended recipes

Start with:

- `recipes/chmarl-paper-assistant.yaml`
- `recipes/chmarl-experiment-analyst.yaml`
- `recipes/chmarl-repo-maintainer.yaml`
- `recipes/chmarl-tomorrow-planner.yaml`

## Desktop branding targets

A future PR can rebrand the desktop application more deeply:

- app name: `CHMARL Tomorrow Goose`
- icon assets under `ui/desktop/src/images/`
- application metadata in `ui/desktop/package.json`
- build/package metadata in `ui/desktop/forge.config.ts`
- default extension catalog for CHMARL tools
- default recipes surfaced in the UI

## CLI helper targets

Suggested helper scripts:

```text
scripts/chmarl/run_ablation_matrix.sh
scripts/chmarl/summarize_results.py
scripts/chmarl/create_traceability_stub.py
```

## Maintenance policy

Because this is a fork for project-specific work, changes do not need to be upstream-neutral. However:

- keep upstream license and attribution
- keep upstream merges possible where practical
- isolate CHMARL-specific files under clear directories
- avoid large generated files unless intentionally published
- document all project-specific defaults
- distinguish direct metrics from inferred proxies

## Versioning suggestion

Use a distribution suffix for releases, for example:

```text
goose 1.37.0-chmarl.1
goose 1.37.0-chmarl.2
```

This preserves the upstream version context while identifying CHMARL-specific builds.
