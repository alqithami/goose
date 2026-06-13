# CHMARL-Goose

**CHMARL-Goose** is the research direction for turning CHMARL from an external simulator into a Goose-like agentic constrained-MARL operating system.

The central idea is:

```text
Ships become tool-using agents.
Ports become service agents.
Emission and fairness constraints become governance agents.
A coordinator resolves conflicts and logs evidence.
MARL provides the learning and optimization backbone.
```

This is different from simply using Goose to summarize CHMARL outputs. The goal is to explore whether a Goose-style agentic orchestration layer can improve constrained hierarchical MARL by making fleet decisions more modular, auditable, and explainable.

## Research question

Can a Goose-like agentic decomposition improve constrained hierarchical MARL for maritime digital twins by combining:

- vessel agents with local tools,
- port agents with capacity/queue state,
- governance agents for emissions and fairness,
- a coordinator for global conflict resolution,
- and a learning/optimization layer for long-term performance?

## Hypothesis

A hybrid agentic-MARL architecture can produce more auditable and constraint-aware decisions than a monolithic policy-only CHMARL runner, while preserving optimization performance under fairness and emissions constraints.

## What this folder contains

```text
research/chmarl-goose/
  README.md
  ARCHITECTURE.md
  METHOD.md
  EVALUATION_PLAN.md
  CLAIM_EVIDENCE_GRAPH.md
  chmarl_goose_runtime.py
  chmarl_goose_artifact.py
  examples/sample_fleet.json
```

The runtime is intentionally lightweight. It is not the final learning algorithm. It is an executable scaffold that models the agent roles and decision traces needed for the next research prototype.

## Run the executable scaffold

```bash
python research/chmarl-goose/chmarl_goose_runtime.py \
  --steps 5 \
  --out reports/chmarl_goose_trace.json
```

The runtime emits a JSON trace containing:

```text
vessel proposals
accepted coordinator actions
emission-governor state
fairness-governor state
port snapshots
vessel snapshots
summary metrics
```

## Generate claim-evidence artifacts

```bash
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

This turns a runtime trace into reviewer-facing evidence:

```text
claim -> trace evidence -> metric support -> missing evidence -> falsification tests
```

## Core components

### Vessel agents

Each vessel agent observes local state and asks structured tools about route cost, queue delay, fairness impact, and emissions pressure before proposing an action.

### Port agents

Each port agent exposes capacity and queue state. This lets vessel agents reason about congestion without directly owning global state.

### Emission governor

The emission governor maintains a budget pressure signal. It is inspired by primal-dual constrained optimization: when fleet fuel/emissions exceed the budget, the governor increases the penalty pressure.

### Fairness governor

The fairness governor monitors inequality across vessel fuel usage and returns a fairness pressure signal based on Gini and max-min behavior.

### Coordinator

The coordinator collects vessel proposals, resolves conflicts, applies governance penalties, steps the digital twin, and logs evidence.

## Why this is more novel

The research contribution is not “Goose plus CHMARL.” The contribution is an **agentic constrained-MARL decomposition**:

```text
observe -> tool query -> proposal -> governance feedback -> coordinated action -> metric evidence
```

This makes each decision auditable. The system can produce not only an action, but also a record of why that action was chosen, how it affected fairness/emissions, and whether the evidence supports a paper claim.

## Intended conference positioning

Possible framing:

```text
CHMARL-Goose: Agentic Constrained Hierarchical Multi-Agent Reinforcement Learning for Maritime Digital Twins
```

or:

```text
Agentic Governance for Fair and Emission-Constrained Multi-Agent Reinforcement Learning
```

Potential tracks:

- multi-agent systems,
- agentic AI,
- constrained reinforcement learning,
- AI for sustainability,
- AI for logistics,
- artifact/reproducibility tooling,
- AI-for-science systems.

## Relationship to EcoFairCHMARL

EcoFairCHMARL remains an external CHMARL simulator and implementation reference. This Goose fork should not modify that repository. CHMARL-Goose lives here as the research layer that can inspect outputs, run scaffolds, and design a stronger agentic-MARL system.

## Next implementation milestones

1. Connect the runtime trace format to `extensions/chmarl-mcp/` tools.
2. Add learned policies behind vessel proposal generation.
3. Add explicit high-level and low-level policy separation.
4. Generate claim-evidence graphs from real CHMARL experiment outputs.
5. Evaluate CHMARL-Goose against baseline CHMARL settings using return, fairness, fuel/emission proxy, queue delay, and violation counts.
