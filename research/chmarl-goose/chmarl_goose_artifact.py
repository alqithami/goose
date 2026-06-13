#!/usr/bin/env python3
"""Generate CHMARL-Goose claim-evidence artifacts from runtime traces.

Input:
  A JSON trace produced by `chmarl_goose_runtime.py`.

Outputs:
  - claim_evidence_graph.json
  - artifact_review.md
  - summary_metrics.json

The goal is to turn a simulation trace into reviewer-facing evidence:
claim -> observed trace evidence -> metric support -> caveats.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass
class ClaimEvidence:
    claim_id: str
    claim: str
    claim_type: str
    status: str
    evidence: list[dict[str, Any]]
    missing_evidence: list[str]
    falsification_tests: list[str]
    reviewer_note: str


def load_trace(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Expected runtime output JSON object.")
    if "trace" not in payload:
        raise ValueError("Trace file does not contain a 'trace' field.")
    return payload


def summarize_trace(payload: dict[str, Any]) -> dict[str, Any]:
    trace = payload.get("trace", [])
    if not trace:
        return {
            "steps": 0,
            "proposal_count": 0,
            "accepted_count": 0,
            "trace_completeness": 0.0,
            "governance_interventions": 0,
            "final_metrics": {},
        }

    proposal_count = sum(len(step.get("proposals", [])) for step in trace)
    accepted_count = sum(
        sum(1 for action in step.get("accepted_actions", []) if action.get("accepted"))
        for step in trace
    )
    complete_steps = sum(
        1
        for step in trace
        if step.get("proposals") is not None
        and step.get("accepted_actions") is not None
        and step.get("emission_governor") is not None
        and step.get("fairness_after") is not None
    )
    governance_interventions = sum(
        1
        for step in trace
        if step.get("emission_governor", {}).get("pressure", 0) > 0
        or step.get("fairness_after", {}).get("pressure", 0) > 0
    )
    final = trace[-1]
    final_metrics = {
        "total_fuel": payload.get("total_fuel"),
        "mean_fuel": payload.get("mean_fuel"),
        "gini": payload.get("gini"),
        "max_min_ratio": payload.get("max_min_ratio"),
        "emission_pressure": payload.get("emission_pressure"),
        "fairness_pressure": payload.get("fairness_pressure"),
        "final_step_fairness": final.get("fairness_after", {}),
        "final_step_emission": final.get("emission_governor", {}),
    }
    return {
        "steps": len(trace),
        "proposal_count": proposal_count,
        "accepted_count": accepted_count,
        "trace_completeness": complete_steps / len(trace),
        "governance_interventions": governance_interventions,
        "final_metrics": final_metrics,
    }


def build_claim_evidence(summary: dict[str, Any]) -> list[ClaimEvidence]:
    metrics = summary.get("final_metrics", {})
    trace_completeness = summary.get("trace_completeness", 0.0)
    governance_interventions = summary.get("governance_interventions", 0)
    proposal_count = summary.get("proposal_count", 0)
    accepted_count = summary.get("accepted_count", 0)

    evidence: list[ClaimEvidence] = []

    evidence.append(
        ClaimEvidence(
            claim_id="C1_AGENTIC_DECOMPOSITION",
            claim="CHMARL-Goose produces auditable vessel proposals and coordinated actions.",
            claim_type="interpretability",
            status="supported" if trace_completeness >= 1.0 and proposal_count > 0 else "partially_supported",
            evidence=[
                {"kind": "trace", "description": "Trace contains vessel proposals and accepted actions.", "value": proposal_count},
                {"kind": "metric", "description": "Accepted coordinated actions.", "value": accepted_count},
                {"kind": "metric", "description": "Trace completeness ratio.", "value": trace_completeness},
            ],
            missing_evidence=[] if trace_completeness >= 1.0 else ["Some trace steps are missing proposals, actions, or governance fields."],
            falsification_tests=["Run traces with larger fleets and verify proposal/action evidence remains complete."],
            reviewer_note="This claim is about auditability of the scaffold, not final policy optimality.",
        )
    )

    evidence.append(
        ClaimEvidence(
            claim_id="C2_GOVERNANCE_PRESSURE",
            claim="Emission and fairness governors provide explicit constraint pressure signals.",
            claim_type="governance",
            status="supported" if governance_interventions > 0 else "partially_supported",
            evidence=[
                {"kind": "metric", "description": "Governance interventions with positive pressure.", "value": governance_interventions},
                {"kind": "metric", "description": "Final emission pressure.", "value": metrics.get("emission_pressure")},
                {"kind": "metric", "description": "Final fairness pressure.", "value": metrics.get("fairness_pressure")},
            ],
            missing_evidence=[] if governance_interventions > 0 else ["No positive governance pressure was observed in this run."],
            falsification_tests=["Tighten emission budget and fairness target to verify pressure updates respond predictably."],
            reviewer_note="Fuel is currently treated as an emissions proxy unless direct emissions are logged.",
        )
    )

    evidence.append(
        ClaimEvidence(
            claim_id="C3_FAIRNESS_TRACKING",
            claim="The runtime tracks fairness burden through Gini and max-min ratio.",
            claim_type="fairness",
            status="supported" if metrics.get("gini") is not None and metrics.get("max_min_ratio") is not None else "unsupported",
            evidence=[
                {"kind": "metric", "description": "Final Gini coefficient.", "value": metrics.get("gini")},
                {"kind": "metric", "description": "Final max-min ratio.", "value": metrics.get("max_min_ratio")},
            ],
            missing_evidence=["Multi-seed variance is not available in a single trace."],
            falsification_tests=["Run multiple seeds and check whether fairness improvements remain stable."],
            reviewer_note="Fairness tracking is supported; fairness improvement requires comparison against baselines.",
        )
    )

    evidence.append(
        ClaimEvidence(
            claim_id="C4_OPTIMIZATION_PERFORMANCE",
            claim="CHMARL-Goose improves optimization performance over baseline CHMARL.",
            claim_type="optimization",
            status="needs_verification",
            evidence=[
                {"kind": "metric", "description": "Prototype total fuel.", "value": metrics.get("total_fuel")},
            ],
            missing_evidence=[
                "No baseline CHMARL comparison is bundled with this trace.",
                "No return or throughput comparison is available.",
                "No multi-seed confidence interval is available.",
            ],
            falsification_tests=[
                "Compare against original CHMARL PPO across the same fleet settings.",
                "Run ablations without governors and without tool queries.",
            ],
            reviewer_note="Do not claim optimization superiority until baseline outputs are connected.",
        )
    )

    return evidence


def render_markdown(summary: dict[str, Any], claims: list[ClaimEvidence]) -> str:
    lines = [
        "# CHMARL-Goose artifact review",
        "",
        "## Summary metrics",
        "",
        "```json",
        json.dumps(summary, indent=2),
        "```",
        "",
        "## Claim-evidence graph",
        "",
    ]
    for claim in claims:
        lines.extend(
            [
                f"### {claim.claim_id}: {claim.claim}",
                "",
                f"- Type: `{claim.claim_type}`",
                f"- Status: `{claim.status}`",
                f"- Reviewer note: {claim.reviewer_note}",
                "",
                "Evidence:",
            ]
        )
        for item in claim.evidence:
            lines.append(f"- {item.get('description')} `{item.get('value')}`")
        if claim.missing_evidence:
            lines.append("")
            lines.append("Missing evidence:")
            for item in claim.missing_evidence:
                lines.append(f"- {item}")
        if claim.falsification_tests:
            lines.append("")
            lines.append("Falsification tests:")
            for item in claim.falsification_tests:
                lines.append(f"- {item}")
        lines.append("")
    lines.extend(
        [
            "## Global caveats",
            "",
            "- This artifact reviews the CHMARL-Goose scaffold, not a final learned MARL policy.",
            "- Fuel is an emissions proxy unless direct emissions are logged.",
            "- Optimization superiority requires matched CHMARL baselines and multi-seed evaluation.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate(trace_path: Path, out_dir: Path) -> dict[str, str]:
    payload = load_trace(trace_path)
    summary = summarize_trace(payload)
    claims = build_claim_evidence(summary)

    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "summary_metrics.json"
    graph_path = out_dir / "claim_evidence_graph.json"
    report_path = out_dir / "artifact_review.md"

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    graph_path.write_text(json.dumps([asdict(claim) for claim in claims], indent=2), encoding="utf-8")
    report_path.write_text(render_markdown(summary, claims), encoding="utf-8")

    return {
        "summary_metrics": str(summary_path),
        "claim_evidence_graph": str(graph_path),
        "artifact_review": str(report_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate CHMARL-Goose artifact review from a runtime trace.")
    parser.add_argument("--trace", required=True, help="Path to chmarl_goose_runtime.py JSON output.")
    parser.add_argument("--out-dir", default="reports/chmarl_goose_artifact", help="Output directory for artifact files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = generate(Path(args.trace).expanduser().resolve(), Path(args.out_dir).expanduser().resolve())
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
