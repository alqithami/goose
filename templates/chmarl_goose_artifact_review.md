# CHMARL-Goose artifact review

Generated: `{{ generated_at }}`

Trace: `{{ trace_path }}`

## Status summary

| Status | Count |
|---|---:|
| supported | {{ supported_count }} |
| partially_supported | {{ partially_supported_count }} |
| needs_verification | {{ needs_verification_count }} |
| unsupported | {{ unsupported_count }} |
| overclaimed | {{ overclaimed_count }} |

## Claim-evidence table

| Claim ID | Claim | Status | Evidence | Missing evidence | Reviewer note |
|---|---|---|---|---|---|
| {{ claim_id }} | {{ claim }} | {{ status }} | {{ evidence_summary }} | {{ missing_evidence }} | {{ reviewer_note }} |

## Decision-trace checks

- Trace steps complete: `{{ trace_steps_complete }}`
- Proposals with tool evidence: `{{ proposals_with_tool_evidence }}`
- Accepted actions: `{{ accepted_actions }}`
- Rejected actions: `{{ rejected_actions }}`
- Governance interventions: `{{ governance_interventions }}`

## Artifact caveats

- The current CHMARL-Goose runtime is a scaffold, not a completed learned MARL algorithm.
- Fuel usage is an emissions proxy unless a direct emissions model is configured.
- Performance claims require comparison against baseline CHMARL outputs.
- Fairness claims require no-governor and fairness-governor ablations.
- Top-tier conference claims require multi-seed evidence and a reproducible experiment bundle.

## Reviewer-facing conclusion

`{{ conclusion }}`
