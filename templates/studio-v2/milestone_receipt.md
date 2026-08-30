---

schema: studio.artifact-template/v2
artifact_type: MILESTONE_RECEIPT
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# MILESTONE_RECEIPT

Tie a milestone outcome to accepted work packages, evidence, revision, residual risk, and owner approval.
Fill only the fields required for the current profile and next phase.
Never invent missing facts; use `TBD` or `UNPROVEN` with an owner and next action.

## Non-goals

- Do not create a competing authority, silently expand scope, or convert an unverified claim into proof.

## Assumptions

- State each load-bearing assumption, owner, confidence, and cheapest useful validation.

## Requirements and inputs

| Field | Shape | Reference or rule |
|---|---|---|
| `document_id` | `string` | `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$` |
| `milestone_id` | `string` | `^MILESTONE-[A-Z0-9]+(?:-[A-Z0-9]+)*$` |
| `revision` | `string` | `^[0-9a-f]{40}$` |
| `work_packages` | `array[string]` | `required` |
| `evidence` | `array[object]` | `required` |
| `remaining_risk` | `string` | `required` |
| `owner_approval` | `string` | `required` |

## Proof

- Evidence level: `E0`/`E1`/`E2`/`E3`/`E4`/`E5` or `UNPROVEN`.
- Direct command or probe: `TBD`.
- Observed result and output digest: `TBD`.

## References

- Governing source or linked artifact ID: `TBD`.
- Current revision or retrieval date: `TBD`.

## Next action

- Name one owner, one bounded action, and the evidence needed to close it.

## Artifact blueprint

### Outcome

Record the outcome using the fields above; link IDs and direct proof where available.

### Accepted work

Record the accepted work using the fields above; link IDs and direct proof where available.

### Evidence

Record the evidence using the fields above; link IDs and direct proof where available.

### Remaining risk

Record the remaining risk using the fields above; link IDs and direct proof where available.

### Owner approval

Record the owner approval using the fields above; link IDs and direct proof where available.

