---

schema: studio.artifact-template/v2
artifact_type: CONTEXT_CAPSULE
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# CONTEXT_CAPSULE

Provide only the active work package context required for a safe fresh session.
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
| `wp_id` | `string` | `work_package.wp_id` |
| `snapshot_id` | `string` | `snapshot.snapshot_id` |
| `active_goal` | `string` | `required` |
| `requirements` | `array[string]` | `product_spec.requirements` |
| `decisions` | `array[string]` | `required` |
| `scope_budget` | `object` | `required` |
| `allowed_paths` | `array[string]` | `required` |
| `forbidden_paths` | `array[string]` | `required` |
| `acceptance` | `string` | `required` |
| `proof` | `string` | `required` |
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

### Active goal

Record the active goal using the fields above; link IDs and direct proof where available.

### Relevant requirements

Record the relevant requirements using the fields above; link IDs and direct proof where available.

### Relevant decisions

Record the relevant decisions using the fields above; link IDs and direct proof where available.

### Scope budget

Record the scope budget using the fields above; link IDs and direct proof where available.

### Allowed and forbidden paths

Record the allowed and forbidden paths using the fields above; link IDs and direct proof where available.

### Acceptance

Record the acceptance using the fields above; link IDs and direct proof where available.

### Proof

Record the proof using the fields above; link IDs and direct proof where available.

### Stop conditions

Record the stop conditions using the fields above; link IDs and direct proof where available.

