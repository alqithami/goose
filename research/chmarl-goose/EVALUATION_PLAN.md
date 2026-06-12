# CHMARL-Goose evaluation plan

This document defines the evaluation needed to make CHMARL-Goose credible for a top-tier AI venue.

## Evaluation goal

Demonstrate that an agentic constrained-MARL decomposition can improve or clarify fleet optimization under fairness and emissions constraints.

The evaluation should test not only reward performance, but also constraint satisfaction, fairness, robustness, and auditability.

## Baselines

Minimum baselines:

```text
B0: Original CHMARL PPO
B1: PPO + emission cap
B2: PPO + fairness shaping
B3: PPO + emission cap + fairness shaping
B4: SOTO wrapper
B5: FEN wrapper
```

CHMARL-Goose ablations:

```text
G0: CHMARL-Goose heuristic agents, no governors
G1: CHMARL-Goose + emission governor
G2: CHMARL-Goose + fairness governor
G3: CHMARL-Goose + both governors
G4: CHMARL-Goose + both governors + learned policy layer
```

## Metrics

### Optimization metrics

```text
average return
return standard deviation
throughput proxy
travel completion rate
queue delay
route efficiency
```

### Sustainability metrics

```text
fuel usage
emission proxy
emission-budget violation count
emission-budget violation magnitude
budget slack
```

### Fairness metrics

```text
Gini coefficient
max-min ratio
fuel-usage variance
worst-vessel burden
```

### Robustness metrics

```text
performance under storms
performance under high port congestion
performance under tight emission budget
performance across vessel-count and port-count scaling
```

### Auditability metrics

```text
percentage of actions with complete decision trace
number of governance interventions
number of rejected/modified vessel proposals
claim-evidence coverage score
artifact readiness score
```

## Experiment matrix

Start with:

```text
ports:      8, 16
vessels:    20, 50
seeds:      5 minimum
episodes:   1000, 2000, 5000 depending on compute
weather:    on/off
budgets:    loose, medium, tight
fairness:   low, medium, high pressure
```

## Falsification tests

The system should be evaluated with adversarial or difficult cases:

```text
1. Tight emission budget with high vessel count.
2. Port congestion spike.
3. Unequal vessel fuel curves.
4. Storm-heavy weather regime.
5. Fairness pressure set too high.
6. Emission pressure set too high.
```

A claim should be weakened if:

```text
- fairness improves only by a trivial margin,
- returns collapse under fairness pressure,
- emission improvements are only fuel proxies with no direct emission field,
- results fail across seeds,
- governance agents only improve metrics by hard-coding behavior,
- trace logs are incomplete or not connected to actions.
```

## Artifact outputs

Each run should produce:

```text
episode_trace.jsonl
fleet_metrics.csv
fairness_metrics.csv
emission_budget_trace.csv
proposal_log.jsonl
governance_interventions.jsonl
claim_evidence_graph.json
artifact_review.md
```

## Reviewer-facing checklist

A top-tier artifact should answer:

```text
Can the reviewer run a small demo in under 30 minutes?
Can the reviewer inspect one complete decision trace?
Can the reviewer reproduce at least one metric table?
Can the reviewer see which claims are supported or unsupported?
Can the reviewer distinguish fuel proxies from direct emissions?
Can the reviewer identify whether QMIX/MAPPO are real baselines or placeholders?
```

## Minimum publishable prototype

A minimum credible CHMARL-Goose prototype should include:

```text
- executable agentic runtime scaffold,
- sample fleet configuration,
- governance pressure updates,
- decision trace logs,
- claim-evidence graph schema,
- reviewer quickstart,
- comparison against at least one CHMARL baseline output,
- clear limitations.
```

## Stronger top-tier target

A stronger version should evaluate the method on multiple constrained MARL settings, not only maritime logistics:

```text
- maritime fleet routing,
- port congestion control,
- energy-grid dispatch,
- warehouse/logistics scheduling,
- constrained resource allocation.
```

That would make the contribution more general and less dependent on one domain.
