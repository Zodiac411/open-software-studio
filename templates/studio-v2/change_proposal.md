---

schema: studio.artifact-template/v2
artifact_type: CHANGE_PROPOSAL
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# CHANGE_PROPOSAL

Record why a decision should change, its impact, approval, and rollback.
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
| `change_id` | `string` | `^CHG-[A-Z0-9]+(?:-[A-Z0-9]+)*$` |
| `reason` | `string` | `required` |
| `current_decision` | `string` | `required` |
| `proposed_decision` | `string` | `required` |
| `impact` | `string` | `required` |
| `approval` | `string` | `required` |
| `rollback` | `string` | `required` |

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

### Reason

Record the reason using the fields above; link IDs and direct proof where available.

### Current decision

Record the current decision using the fields above; link IDs and direct proof where available.

### Proposed change

Record the proposed change using the fields above; link IDs and direct proof where available.

### Impact

Record the impact using the fields above; link IDs and direct proof where available.

### Approval

Record the approval using the fields above; link IDs and direct proof where available.

### Rollback

Record the rollback using the fields above; link IDs and direct proof where available.
