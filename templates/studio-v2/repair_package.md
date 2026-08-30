---

schema: studio.artifact-template/v2
artifact_type: REPAIR_PACKAGE
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# REPAIR_PACKAGE

Turn accepted findings into a bounded repair with regression proof and explicit stop conditions.
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
| `repair_id` | `string` | `^REPAIR-[A-Z0-9]+(?:-[A-Z0-9]+)*$` |
| `accepted_findings` | `string` | `required` |
| `allowed_paths` | `array[string]` | `required` |
| `forbidden_paths` | `array[string]` | `required` |
| `required_behavior` | `string` | `required` |
| `regression_proof` | `string` | `required` |
| `evidence` | `array[object]` | `required` |
| `non_goals` | `array[string]` | `required` |
| `repair_budget` | `string` | `required` |
| `stop_conditions` | `array[string]` | `required` |

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

### Accepted findings

Record the accepted findings using the fields above; link IDs and direct proof where available.

### Allowed and forbidden scope

Record the allowed and forbidden scope using the fields above; link IDs and direct proof where available.

### Required behavior

Record the required behavior using the fields above; link IDs and direct proof where available.

### Regression proof

Record the regression proof using the fields above; link IDs and direct proof where available.

### Evidence

Record the evidence using the fields above; link IDs and direct proof where available.

### Non-goals

Record the non-goals using the fields above; link IDs and direct proof where available.

### Stop conditions

Record the stop conditions using the fields above; link IDs and direct proof where available.

