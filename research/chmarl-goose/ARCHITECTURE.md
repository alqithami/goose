# CHMARL-Goose architecture

CHMARL-Goose is an agentic constrained-MARL architecture. It treats maritime logistics as a multi-agent operating system rather than a single monolithic simulator loop.

## Architecture overview

```text
CHMARL-Goose

Digital Twin
  ports, vessels, distances, queues, weather, fuel/emission proxy

Agent Layer
  VesselAgent_i
  PortAgent_j
  EmissionGovernor
  FairnessGovernor
  FleetCoordinator

Tool Layer
  estimate_route_cost
  estimate_queue_delay
  estimate_emission_pressure
  estimate_fairness_impact
  inspect_port_capacity
  simulate_candidate_action

Optimization Layer
  policy learning
  constrained reward shaping
  dual-variable updates
  fairness pressure updates
  ablation/evaluation harness

Evidence Layer
  decision traces
  metric summaries
  claim-evidence graph
  artifact report
```

## Agent roles

### VesselAgent

A vessel agent owns local vessel state and proposes actions.

Inputs:

```text
current port
destination
status
remaining distance
fuel used
weather signal
port capacity signal
emission pressure
fairness pressure
```

Tools:

```text
estimate_route_cost(destination, speed)
inspect_port_capacity(port)
estimate_queue_delay(port)
estimate_fairness_impact(action)
estimate_emission_pressure(action)
```

Outputs:

```text
proposed destination
proposed speed
reason code
expected fuel cost
expected queue pressure
expected fairness effect
```

### PortAgent

A port agent owns local capacity and queue state.

Inputs:

```text
arriving vessels
waiting vessels
capacity
service availability
```

Outputs:

```text
capacity availability
queue delay estimate
congestion pressure
admission decision
```

### EmissionGovernor

The emission governor monitors fleet-wide fuel/emission proxy and updates a pressure signal.

State:

```text
emission_budget
cumulative_emissions_or_fuel
dual_variable
learning_rate
```

Update:

```text
lambda_{t+1} = max(0, lambda_t + eta * (emissions_t - budget_t))
```

Outputs:

```text
emission_pressure
violation_flag
budget_slack
```

### FairnessGovernor

The fairness governor monitors inequality of fuel burden across vessels.

Metrics:

```text
Gini coefficient
max-min ratio
fuel variance
```

Outputs:

```text
fairness_pressure
unfairness_flag
most-burdened vessels
least-burdened vessels
```

### FleetCoordinator

The coordinator aggregates proposals and governance signals.

Responsibilities:

```text
collect vessel proposals
query port agents
apply governor pressures
resolve conflicts
step the digital twin
log decision evidence
emit training trajectories
```

## Decision cycle

```text
1. Observe digital-twin state.
2. Port agents publish capacity and congestion signals.
3. Governance agents publish emission/fairness pressure.
4. Vessel agents query tools and propose actions.
5. FleetCoordinator resolves conflicts and applies actions.
6. Digital twin advances one step.
7. Metrics and decision traces are logged.
8. Optimization layer updates policies or governors.
```

## Why this is different from standard CHMARL

Standard CHMARL mostly exposes a policy/environment interface:

```text
observation -> action -> reward -> next observation
```

CHMARL-Goose exposes an auditable agentic interface:

```text
observation -> tool queries -> proposal -> governance feedback -> coordinated action -> evidence trace
```

The evidence trace is essential for top-tier reproducibility and artifact evaluation. It lets a reviewer inspect not only final metrics, but why a fleet decision was made and which constraints influenced it.

## Why this is different from standard Goose

Goose is a general agent framework. CHMARL-Goose adds:

```text
constrained MARL objectives
fairness and emissions governors
maritime digital twin dynamics
fleet-level coordination
metric-aware optimization
paper-claim traceability
```

## Research artifact outputs

A complete CHMARL-Goose run should eventually produce:

```text
episode_trace.jsonl
fleet_metrics.csv
fairness_metrics.csv
emission_budget_trace.csv
claim_evidence_graph.json
artifact_review.md
latex_results_table.tex
```

## Safety and scope boundary

CHMARL-Goose lives inside `alqithami/goose`. It may read from EcoFairCHMARL as an external project reference, but it should not modify EcoFairCHMARL unless explicitly requested.
