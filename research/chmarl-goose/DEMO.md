# CHMARL-Goose reviewer demo

This demo shows the current CHMARL-Goose research prototype in a small, reproducible way.

The goal is not to claim final MARL performance. The goal is to show the new agentic constrained-MARL structure:

```text
vessel agents -> tool-based proposals -> governance feedback -> coordinated actions -> decision evidence
```

## What the demo produces

The demo produces two artifacts:

```text
reports/chmarl_goose_trace.json
reports/chmarl_goose_claim_evidence.json
reports/chmarl_goose_artifact_review.md
```

The trace records proposals, accepted actions, port state, vessel state, emission-governor state, and fairness-governor state.

The claim-evidence graph separates supported scaffold claims from claims that still need baseline experiments.

## Run the runtime scaffold

From the repository root:

```bash
python research/chmarl-goose/chmarl_goose_runtime.py \
  --steps 5 \
  --out reports/chmarl_goose_trace.json
```

Expected terminal output includes a JSON summary with fields such as:

```text
steps
total_fuel
mean_fuel
gini
max_min_ratio
emission_pressure
fairness_pressure
```

## Generate claim evidence

```bash
python research/chmarl-goose/generate_claim_evidence.py \
  --trace reports/chmarl_goose_trace.json \
  --out-json reports/chmarl_goose_claim_evidence.json \
  --out-md reports/chmarl_goose_artifact_review.md
```

Expected terminal output includes paths to the generated claim-evidence graph and artifact review.

## Inspect the trace

The trace should contain records like:

```text
trace[i].proposals
trace[i].accepted_actions
trace[i].emission_governor
trace[i].fairness_before
trace[i].fairness_after
trace[i].ports
trace[i].vessels
```

For a move proposal, inspect:

```text
proposal.tool_evidence.route_cost_candidates
proposal.tool_evidence.emission_pressure
proposal.tool_evidence.fairness_pressure
```

These fields are the first version of CHMARL-Goose decision evidence.

## Inspect the artifact review

Open:

```text
reports/chmarl_goose_artifact_review.md
```

The review should distinguish:

```text
supported scaffold evidence
partially supported governance evidence
claims needing baseline verification
unsupported claims that should not be made yet
```

## Run tests

```bash
python -m pytest research/chmarl-goose/tests
```

The tests check:

```text
PortAgent congestion and capacity
VesselAgent auditable proposal generation
EmissionGovernor pressure update
FairnessGovernor Gini/max-min behavior
FleetCoordinator decision trace generation
runtime trace tool-evidence fields
```

## Reviewer interpretation

A reviewer should conclude:

```text
CHMARL-Goose is currently an executable agentic constrained-MARL scaffold.
It demonstrates auditable proposal/governance/coordinator flow.
It does not yet prove learned-policy superiority over CHMARL baselines.
```

## What would make this stronger

Next evidence needed:

```text
1. Compare against real CHMARL baseline outputs.
2. Add no-governor, emission-governor, fairness-governor, and full-governor ablations.
3. Add learned vessel policies behind the proposal generator.
4. Run multiple seeds.
5. Report return, fuel/emission proxy, Gini, max-min ratio, queue delay, and trace completeness.
```
