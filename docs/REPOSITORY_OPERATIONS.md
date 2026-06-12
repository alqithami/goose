# CHMARL Goose repository operations

This document explains how this fork should be updated.

## Working repository

The working repository is:

```text
alqithami/goose
```

This is the source of truth for CHMARL Goose.

## Related repositories

```text
alqithami/goose
  Goose-based CHMARL assistant distribution.

alqithami/EcoFairCHAMRL
  Core CHMARL simulator, training, metrics, baselines, and experiment outputs.

aaif-goose/goose
  Upstream Goose source used for attribution and future syncs.
```

## Update model

For CHMARL Goose work, commit changes to `alqithami/goose`.

Use direct commits for small documentation, recipe, helper-script, or MCP updates.

Use branches inside `alqithami/goose` when a review checkpoint is useful.

The upstream Goose repository is not the work target for CHMARL-specific changes.

## Recommended change categories

Keep these in `alqithami/goose`:

- CHMARL documentation
- CHMARL recipes
- CHMARL MCP servers
- helper scripts
- reporting tools
- Goose distribution guidance
- website/demo drafting support

Keep these in `alqithami/EcoFairCHAMRL`:

- MARL environment code
- training loops
- fairness metric implementation
- emission-budget logic
- baselines
- simulator tests
- real experiment outputs
- reproducibility metadata

## Syncing upstream Goose later

If the fork needs new upstream Goose features, sync upstream into this fork as a maintenance activity. Review conflicts carefully and keep CHMARL-specific files isolated under clear paths such as:

```text
docs/
recipes/
extensions/chmarl-mcp/
scripts/chmarl/
```

## Current preferred MCP path

Use:

```text
extensions/chmarl-mcp/
```

The older scaffold remains at:

```text
extensions/chmarl-results-mcp/
```

Use the richer `extensions/chmarl-mcp/` server for normal CHMARL workflows.
