#!/usr/bin/env python3
"""Generate a CHMARL-Goose claim-evidence graph from a runtime trace.

The generator reads JSON produced by `chmarl_goose_runtime.py` and produces:

- a structured claim-evidence graph JSON file
- a reviewer-facing markdown artifact review

This is intentionally conservative: it separates supported evidence from
missing evidence and avoids converting fuel proxy fields into direct emissions
claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED = "supported"
PARTIAL = "partially_supported"
UNSUPPORTED = "unsupported"
NEEDS_VERIFICATION = "needs_verification"
OVERCLAIMED = "overclaimed"


def load_trace(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Trace file does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Expected runtime trace JSON to be an object.")
    return payload


def trace_steps(payload: dict[str, Any]) -> list[dict[str, Any]]:
    steps = payload.get("trace", [])
    if not isinstance(steps, list):
        return []
    return [step for step in steps if isinstance(step, dict)]


def has_complete_trace_steps(steps: list[dict[str, Any]]) -> bool:
    required = {"step", "proposals", "accepted_actions", "emission_governor", "fairness_after", "ports", "vessels"}
    return bool(steps) and all(required.issubset(step.keys()) for step in steps)


def count_governance_interventions(steps: list[dict[str, Any]]) -> int:
    count = 0
    for step in steps:
        emission = step.get("emission_governor", {})
        fairness = step.get("fairness_after", {})
        if float(emission.get("violation", 0.0) or 0.0) > 0.0:
            count += 1
        if float(fairness.get("violation", 0.0) or 0.0) > 0.0:
            count += 1
    return count


def proposal_statistics(steps: list[dict[str, Any]]) -> dict[str, int]:
    proposals = 0
    accepted = 0
    rejected = 0
    with_tool_evidence = 0
    for step in steps:
        for proposal in step.get("proposals", []):
            proposals += 1
            if isinstance(proposal, dict) and "tool_evidence" in proposal:
                with_tool_evidence += 1
        for action in step.get("accepted_actions", []):
            if isinstance(action, dict) and action.get("accepted"):
                accepted += 1
            else:
                rejected += 1
    return {
        "proposals": proposals,
        "accepted_actions": accepted,
        "rejected_actions": rejected,
        "proposals_with_tool_evidence": with_tool_evidence,
    }


def build_claims(payload: dict[str, Any]) -> list[dict[str, Any]]:
    steps = trace_steps(payload)
    complete_trace = has_complete_trace_steps(steps)
    proposal_stats = proposal_statistics(steps)
    governance_interventions = count_governance_interventions(steps)

    metrics = {
        "steps": payload.get("steps"),
        "total_fuel": payload.get("total_fuel"),
        "mean_fuel": payload.get("mean_fuel"),
        "gini": payload.get("gini"),
        "max_min_ratio": payload.get("max_min_ratio"),
        "emission_pressure": payload.get("emission_pressure"),
        "fairness_pressure": payload.get("fairness_pressure"),
        "governance_interventions": governance_interventions,
        **proposal_stats,
    }

    return [
        {
            "claim_id": "CG-001",
            "claim": "CHMARL-Goose produces auditable vessel-level decision traces.",
            "claim_type": "interpretability",
            "status": SUPPORTED if complete_trace and proposal_stats["proposals_with_tool_evidence"] > 0 else PARTIAL,
            "evidence": [
                {
                    "kind": "trace",
                    "description": "Runtime trace contains proposals, accepted actions, governance state, port state, and vessel state per step.",
                    "metric": "complete_trace_steps",
                    "value": len(steps),
                },
                {
                    "kind": "trace",
                    "description": "Move proposals include tool_evidence entries with route-cost candidates and governance pressure.",
                    "metric": "proposals_with_tool_evidence",
                    "value": proposal_stats["proposals_with_tool_evidence"],
                },
            ],
            "missing_evidence": [] if complete_trace else ["Trace schema incomplete for one or more steps."],
            "falsification_tests": [
                "Run the scaffold for longer episodes and verify every action has a complete proposal and governance record.",
                "Check whether rejected proposals preserve enough evidence for reviewer inspection.",
            ],
            "reviewer_note": "This is currently a scaffold trace, not evidence of learned policy performance.",
        },
        {
            "claim_id": "CG-002",
            "claim": "CHMARL-Goose implements explicit emission-governance pressure.",
            "claim_type": "emission",
            "status": PARTIAL,
            "evidence": [
                {
                    "kind": "trace",
                    "description": "Each step logs emission governor budget, violation, pressure, and cumulative violation.",
                    "metric": "emission_pressure",
                    "value": metrics.get("emission_pressure"),
                    "caveat": "Current prototype uses fuel as an emission proxy.",
                }
            ],
            "missing_evidence": [
                "Direct emissions column or validated emissions model.",
                "Comparison against a no-emission-governor baseline.",
                "Multi-seed evaluation under tight, medium, and loose budgets.",
            ],
            "falsification_tests": [
                "Show that emission pressure changes behavior rather than merely logging violations.",
                "Compare fuel/emission proxy under no-governor and governor settings.",
            ],
            "reviewer_note": "Do not claim direct emissions reduction unless direct emissions are logged or modeled.",
        },
        {
            "claim_id": "CG-003",
            "claim": "CHMARL-Goose implements explicit fairness-governance pressure.",
            "claim_type": "fairness",
            "status": PARTIAL,
            "evidence": [
                {
                    "kind": "metric",
                    "description": "Runtime reports Gini and max-min ratio over vessel fuel burden.",
                    "metric": "gini",
                    "value": metrics.get("gini"),
                },
                {
                    "kind": "metric",
                    "description": "Runtime reports max-min ratio over vessel fuel burden.",
                    "metric": "max_min_ratio",
                    "value": metrics.get("max_min_ratio"),
                },
            ],
            "missing_evidence": [
                "Ablation without fairness governor.",
                "Stress tests with unequal fuel curves and port congestion.",
                "Evidence that fairness pressure improves equity without collapse in return or throughput.",
            ],
            "falsification_tests": [
                "Increase fairness pressure and test whether return collapses.",
                "Evaluate whether low-burden and high-burden vessels converge over multiple seeds.",
            ],
            "reviewer_note": "Current evidence supports monitoring and pressure signals, not final fairness guarantees.",
        },
        {
            "claim_id": "CG-004",
            "claim": "CHMARL-Goose improves optimization performance over CHMARL baselines.",
            "claim_type": "optimization",
            "status": NEEDS_VERIFICATION,
            "evidence": [
                {
                    "kind": "metric",
                    "description": "Runtime produces fuel and fairness metrics, but no baseline comparison is included in this trace.",
                    "metric": "total_fuel",
                    "value": metrics.get("total_fuel"),
                }
            ],
            "missing_evidence": [
                "Baseline CHMARL output files.",
                "Multi-seed comparison against PPO, emission-cap, fairness, SOTO, and FEN settings.",
                "Throughput/return metric aligned with the original CHMARL objective.",
            ],
            "falsification_tests": [
                "Compare against original CHMARL PPO with identical ports, vessels, and seed settings.",
                "Check whether agentic governance helps beyond heuristic route selection.",
            ],
            "reviewer_note": "This claim should not be made until baseline comparisons exist.",
        },
        {
            "claim_id": "CG-005",
            "claim": "CHMARL-Goose is an agentic constrained-MARL research scaffold, not a completed learned MARL algorithm.",
            "claim_type": "reproducibility",
            "status": SUPPORTED,
            "evidence": [
                {
                    "kind": "document",
                    "description": "Runtime and docs explicitly identify the current system as an executable scaffold.",
                },
                {
                    "kind": "trace",
                    "description": "Trace provides evidence of agentic proposal/governance/coordinator flow.",
                    "metric": "steps",
                    "value": metrics.get("steps"),
                },
            ],
            "missing_evidence": [
                "Learned policy layer behind vessel proposals.",
                "Formal connection to the CHMARL training loop.",
            ],
            "falsification_tests": [
                "Ask whether the current policy is learned; answer should be no until a learned layer is added.",
            ],
            "reviewer_note": "This distinction protects the paper from overclaiming.",
        },
    ]


def summarize_status(claims: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(claim["status"]) for claim in claims)
    return dict(sorted(counts.items()))


def write_markdown(claims: list[dict[str, Any]], summary: dict[str, int], output_path: Path, trace_path: Path) -> None:
    lines = [
        "# CHMARL-Goose artifact review",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Trace file: `{trace_path}`",
        "",
        "## Status summary",
        "",
    ]
    for status, count in summary.items():
        lines.append(f"- `{status}`: {count}")

    lines.extend(
        [
            "",
            "## Claim-evidence table",
            "",
            "| Claim ID | Status | Claim | Missing evidence | Reviewer note |",
            "|---|---|---|---|---|",
        ]
    )
    for claim in claims:
        missing = "; ".join(claim.get("missing_evidence", [])) or "None listed"
        lines.append(
            f"| {claim['claim_id']} | {claim['status']} | {claim['claim']} | {missing} | {claim.get('reviewer_note', '')} |"
        )

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- The current runtime is a scaffold, not a completed learned MARL algorithm.",
            "- Fuel is treated as an emissions proxy unless a direct emissions model is provided.",
            "- Performance-improvement claims require baseline CHMARL outputs and multi-seed comparisons.",
            "- Fairness claims require ablations without and with the fairness governor.",
            "",
            "## Recommended next experiments",
            "",
            "1. Run the scaffold with and without emission governor pressure.",
            "2. Run the scaffold with and without fairness governor pressure.",
            "3. Compare against at least one CHMARL baseline output file.",
            "4. Add a learned vessel-policy layer and repeat the same claim-evidence generation.",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate CHMARL-Goose claim-evidence graph from a runtime trace.")
    parser.add_argument("--trace", required=True, help="Path to chmarl_goose_runtime.py JSON trace output.")
    parser.add_argument("--out-json", default="reports/chmarl_goose_claim_evidence.json", help="Output claim-evidence graph JSON path.")
    parser.add_argument("--out-md", default="reports/chmarl_goose_artifact_review.md", help="Output artifact-review markdown path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    trace_path = Path(args.trace).expanduser().resolve()
    payload = load_trace(trace_path)
    claims = build_claims(payload)
    summary = summarize_status(claims)

    out_json = Path(args.out_json).expanduser().resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "trace_path": str(trace_path),
                "summary": summary,
                "claims": claims,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    out_md = Path(args.out_md).expanduser().resolve()
    write_markdown(claims, summary, out_md, trace_path)

    print(json.dumps({"claim_evidence": str(out_json), "artifact_review": str(out_md), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
