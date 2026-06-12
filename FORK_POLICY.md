# CHMARL Goose fork policy

This repository is the working CHMARL Goose fork:

```text
alqithami/goose
```

All CHMARL-specific Goose integration work belongs in this fork.

## Repository roles

```text
alqithami/goose
  CHMARL assistant distribution, recipes, MCP servers, helper scripts, docs, and project-specific branding.

alqithami/EcoFairCHAMRL
  External CHMARL project reference: MARL environment, training loops, metrics, baselines, and generated experiment outputs.
```

## External project boundary

From the perspective of this Goose fork, `alqithami/EcoFairCHAMRL` is read-only unless the user explicitly asks to modify that repository.

Goose integration work should inspect, summarize, and report on EcoFairCHAMRL artifacts without editing that repository.

See:

```text
docs/ECOFAIR_CHMARL_EXTERNAL_INTEGRATION.md
```

## Upstream relationship

The upstream Goose project is an attribution and sync source. This CHMARL work is maintained in the fork under `alqithami/goose`.

Do not create upstream pull requests for CHMARL-specific work.

## Update policy

Make CHMARL Goose changes in `alqithami/goose`.

Use branches or pull requests inside `alqithami/goose` when review is useful.

For routine project-specific work, direct commits to this fork are acceptable.

## Source of truth

```text
https://github.com/alqithami/goose
```
