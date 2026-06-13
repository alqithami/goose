# CHMARL-Goose claim-evidence graph

The CHMARL-Goose research direction is only useful if it can connect claims to evidence.

This document defines the claim-evidence graph used by the runtime and artifact generator.

## Graph structure

```text
claim
  -> evidence required
  -> observed runtime traces
  -> metric summaries
  -> missing evidence
  -> falsification tests
  -> reviewer note
```

## Claim statuses

```text
supported
partially_supported
unsupported
overclaimed
needs_verification
```

## Example claim

```text
Claim:
  CHMARL-Goose produces auditable vessel proposals and coordinated actions.

Evidence:
  - proposal_count > 0
  - accepted_action_count > 0
  - trace_completeness = 1.0
  - each step includes proposals, accepted actions, emission governor, and fairness governor fields

Missing evidence:
  - larger fleet trace
  - multi-seed trace stability

Falsification test:
  Run a congested fleet with 50 vessels and verify trace completeness remains high.
```

## Why this matters

Top-tier AI submissions need more than aggregate metrics. For constrained MARL, reviewers need to see:

- what claim is being made,
- what evidence is required,
- what evidence exists,
- what evidence is missing,
- what result would weaken or falsify the claim.

CHMARL-Goose should generate this structure automatically from runtime traces and experiment outputs.

## Current generator

Use:

```bash
python research/chmarl-goose/chmarl_goose_runtime.py --steps 5 --out reports/chmarl_goose_trace.json
python research/chmarl-goose/chmarl_goose_artifact.py \
  --trace reports/chmarl_goose_trace.json \
  --out-dir reports/chmarl_goose_artifact
```

Expected outputs:

```text
reports/chmarl_goose_artifact/summary_metrics.json
reports/chmarl_goose_artifact/claim_evidence_graph.json
reports/chmarl_goose_artifact/artifact_review.md
```

## Review discipline

Do not mark a claim as supported only because the method exists in prose. Mark it supported only if the runtime trace or experiment output contains the required evidence.
