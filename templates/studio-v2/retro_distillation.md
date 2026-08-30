---

schema: studio.artifact-template/v2
artifact_type: RETRO_DISTILLATION
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# RETRO_DISTILLATION

Separate measured learning and friction from the next bounded improvements.
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
| `outcomes` | `array[string]` | `required` |
| `friction` | `array[string]` | `required` |
| `measured_evidence` | `string` | `required` |
| `decisions` | `array[string]` | `required` |
| `next_actions` | `array[string]` | `required` |

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

### Outcomes

Record the outcomes using the fields above; link IDs and direct proof where available.

### Friction

Record the friction using the fields above; link IDs and direct proof where available.

### Measured evidence

Record the measured evidence using the fields above; link IDs and direct proof where available.

### Decisions

Record the decisions using the fields above; link IDs and direct proof where available.

### Next actions

Record the next actions using the fields above; link IDs and direct proof where available.
