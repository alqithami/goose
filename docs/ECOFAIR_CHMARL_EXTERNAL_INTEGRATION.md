# EcoFairCHMARL external integration

This document defines how CHMARL Goose integrates with EcoFairCHMARL.

## Rule

EcoFairCHMARL is an external project from the perspective of this Goose fork.

```text
alqithami/goose
  Update this repository for CHMARL Goose integration.

alqithami/EcoFairCHAMRL
  Treat as an external/read-only CHMARL codebase unless explicitly instructed otherwise.
```

CHMARL Goose should inspect, summarize, and report on EcoFairCHMARL artifacts. It should not modify EcoFairCHMARL source files, tests, workflows, scripts, or README content as part of Goose integration work.

## Intended integration model

The integration is path-based and read-oriented:

```text
workspace/
  goose/
    extensions/chmarl-mcp/
  EcoFairCHAMRL/
    EcoFairCHMARL.py
    results/
```

The Goose fork provides:

- MCP server tools
- recipes
- documentation
- report generation
- experiment-analysis helpers
- paper-to-code traceability helpers
- website/demo drafting support

The EcoFairCHMARL repository provides:

- the CHMARL simulator
- the full Python pipeline
- generated result CSV files
- generated plots
- experiment outputs

## Preferred MCP configuration

Use the richer MCP server:

```text
extensions/chmarl-mcp/chmarl_mcp.py
```

Example:

```yaml
extensions:
  - type: stdio
    name: chmarl
    cmd: python
    args:
      - /absolute/path/to/goose/extensions/chmarl-mcp/chmarl_mcp.py
      - --repo-dir
      - /absolute/path/to/EcoFairCHAMRL
      - --results-dir
      - /absolute/path/to/EcoFairCHAMRL/results
      - --report-dir
      - /absolute/path/to/EcoFairCHAMRL/results/reports
    description: Analyze EcoFair-CH-MARL experiments and repository artifacts.
```

## What Goose may do

Goose may:

- list EcoFairCHMARL result files
- summarize CSV outputs
- compare experiments
- rank runs by metrics
- detect missing output files
- generate markdown reports into a configured report directory
- produce ablation command plans
- generate traceability notes
- draft documentation or website summaries inside Goose or separate output locations

## What Goose should not do by default

Goose should not modify EcoFairCHMARL unless explicitly instructed:

- do not edit `EcoFairCHMARL.py`
- do not rewrite EcoFairCHMARL README files
- do not add tests, workflows, or packaging to EcoFairCHMARL
- do not open pull requests against EcoFairCHMARL
- do not open pull requests against upstream Goose

## Safe output locations

Generated analysis should go to one of these locations:

```text
alqithami/goose/docs/
alqithami/goose/reports/
alqithami/goose/scripts/chmarl/
/local/workspace/reports/
```

If the configured MCP report directory points inside EcoFairCHMARL, the user should intentionally choose that path.

## Source of truth

For CHMARL Goose work, the source of truth is:

```text
https://github.com/alqithami/goose
```

EcoFairCHMARL remains a separate project reference.
