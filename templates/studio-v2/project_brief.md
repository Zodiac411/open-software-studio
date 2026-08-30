---

schema: studio.artifact-template/v2
artifact_type: PROJECT_BRIEF
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# PROJECT_BRIEF

Turn the request into a bounded outcome with explicit constraints, assumptions, and disposition.
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
| `project_id` | `string` | `project.project_id` |
| `primary_outcome` | `string` | `required` |
| `target_actor` | `string` | `required` |
| `desired_outcome` | `string` | `required` |
| `constraints` | `array[string]` | `required` |
| `non_goals` | `array[string]` | `required` |
| `assumptions` | `array[string]` | `required` |
| `parked_ideas` | `array[string]` | `required` |
| `solution_ladder` | `array[string]` | `required` |
| `disposition` | `string` | `required` |

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

### Problem and current limitation

Record the problem and current limitation using the fields above; link IDs and direct proof where available.

### Target actor

Record the target actor using the fields above; link IDs and direct proof where available.

### Desired outcome

Record the desired outcome using the fields above; link IDs and direct proof where available.

### Success signals

Record the success signals using the fields above; link IDs and direct proof where available.

### Constraints

Record the constraints using the fields above; link IDs and direct proof where available.

### Primary outcome

Record the primary outcome using the fields above; link IDs and direct proof where available.

### Non-goals

Record the non-goals using the fields above; link IDs and direct proof where available.

### Assumptions

Record the assumptions using the fields above; link IDs and direct proof where available.

### Parked ideas

Record the parked ideas using the fields above; link IDs and direct proof where available.

### Smallest adequate solution

Record the smallest adequate solution using the fields above; link IDs and direct proof where available.

### Decision

Record the decision using the fields above; link IDs and direct proof where available.
