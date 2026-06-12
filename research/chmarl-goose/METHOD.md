# CHMARL-Goose method

CHMARL-Goose proposes a hybrid agentic-MARL method for fair and emission-constrained maritime optimization.

## Method summary

The method decomposes constrained fleet optimization into five interacting components:

```text
1. Vessel agents propose local actions.
2. Port agents expose service/capacity constraints.
3. Emission governor supplies budget pressure.
4. Fairness governor supplies inequality pressure.
5. Fleet coordinator resolves conflicts and logs decision evidence.
```

The learning objective remains MARL-compatible, but the action-selection process becomes agentic and auditable.

## State

At timestep `t`, the system state includes:

```text
S_t = {
  vessel states,
  port states,
  distance matrix,
  weather state,
  cumulative fuel/emission proxy,
  fairness metrics,
  queue lengths,
  governor pressures
}
```

Each vessel receives local observations plus global governance signals:

```text
o_i^t = {
  vessel_i status,
  current port,
  destination,
  remaining distance,
  local fuel used,
  nearby port congestion,
  emission pressure,
  fairness pressure
}
```

## Agent tools

The first CHMARL-Goose prototype uses deterministic tools. Future versions can learn or calibrate these tools.

```text
estimate_route_cost(vessel, destination, speed)
inspect_port_capacity(port)
estimate_queue_delay(port)
estimate_fairness_impact(vessel, action)
estimate_emission_pressure(action)
```

These tools make the agent decision trace inspectable.

## Action proposal

Each vessel produces a proposal:

```text
proposal_i^t = {
  destination,
  speed,
  expected_fuel,
  expected_queue_delay,
  expected_fairness_delta,
  expected_emission_pressure,
  reason
}
```

The coordinator can accept, reject, or modify proposals.

## Governance

### Emission governor

The emission governor implements a pressure update inspired by primal-dual constrained optimization:

```text
lambda_{t+1} = max(0, lambda_t + eta_e * (E_t - B_t))
```

Where:

```text
E_t = fleet fuel/emission proxy
B_t = budget
lambda_t = emission pressure
eta_e = update rate
```

### Fairness governor

The fairness governor computes inequality pressure using Gini and max-min ratio:

```text
G_t = gini(fuel_usage)
M_t = min(fuel_usage) / max(fuel_usage)
```

A simple pressure update is:

```text
beta_{t+1} = max(0, beta_t + eta_f * (G_t - G_target))
```

Where:

```text
beta_t = fairness pressure
G_target = target Gini threshold
```

## Reward structure

The research objective is:

```text
maximize fleet utility
  - fuel cost
  - queue delay
  - emission violation penalty
  - fairness inequality penalty
```

A prototype per-step reward can be written as:

```text
R_t = throughput_t
      - c_fuel * fuel_t
      - c_queue * queue_delay_t
      - lambda_t * max(0, emissions_t - budget_t)
      - beta_t * gini(fuel_usage_t)
```

## Evidence trace

Each step should produce a trace record:

```json
{
  "step": 3,
  "vessel_id": "vessel_7",
  "observation_summary": "at port_2, low fuel burden, port_5 congested",
  "tool_calls": [...],
  "proposal": {...},
  "governance_feedback": {...},
  "accepted_action": {...},
  "metrics_after_step": {...}
}
```

This is a core novelty: the system makes MARL decisions auditable.

## Claim-evidence graph

The method should connect paper claims to observed evidence:

```text
claim -> expected evidence -> code/tool evidence -> result files -> metrics -> caveats
```

Example:

```text
Claim: full CHMARL-Goose reduces fairness inequality under emission pressure.
Evidence needed:
  - baseline result
  - emission-only result
  - fairness-only result
  - full-governor result
  - multiple seeds
  - Gini and max-min ratios
  - fuel/emission proxy caveat
```

## Comparison against baselines

Compare:

```text
1. Original CHMARL PPO
2. CHMARL with emission cap
3. CHMARL with fairness shaping
4. CHMARL SOTO/FEN wrappers
5. CHMARL-Goose without governors
6. CHMARL-Goose with emission governor only
7. CHMARL-Goose with fairness governor only
8. Full CHMARL-Goose
```

## Top-tier conference angle

The method should be positioned as:

```text
agentic governance for constrained hierarchical MARL
```

not merely as a maritime application.

The contribution should emphasize:

- tool-using multi-agent decomposition,
- explicit constraint governors,
- auditable decision traces,
- claim-evidence graph generation,
- reproducibility support for constrained MARL.
