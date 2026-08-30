---

schema: studio.artifact-template/v2
artifact_type: PRODUCT_SPEC
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# PRODUCT_SPEC

Make the desired behavior, scenarios, acceptance, and proof observable.
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
| `requirements` | `array[string]` | `product_spec.requirements` |
| `scenarios` | `array[object]` | `required` |
| `acceptance` | `string` | `required` |
| `non_goals` | `array[string]` | `required` |
| `proof_level` | `string` | `required` |

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

### Actors and scenarios

Record the actors and scenarios using the fields above; link IDs and direct proof where available.

### Functional requirements

Record the functional requirements using the fields above; link IDs and direct proof where available.

### Non-functional requirements

Record the non-functional requirements using the fields above; link IDs and direct proof where available.

### Acceptance

Record the acceptance using the fields above; link IDs and direct proof where available.

### Proof plan

Record the proof plan using the fields above; link IDs and direct proof where available.

### Non-goals

Record the non-goals using the fields above; link IDs and direct proof where available.

