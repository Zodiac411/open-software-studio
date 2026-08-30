---

schema: studio.artifact-template/v2
artifact_type: WORK_PACKAGE
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# WORK_PACKAGE

Give one executor a frozen, bounded outcome with allowed paths, proof, stop conditions, and handoff.
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
| `status` | `string` | `required` |
| `snapshot_id` | `string` | `snapshot.snapshot_id` |
| `base_sha` | `string` | `^[0-9a-f]{40}$` |
| `primary_outcome` | `string` | `required` |
| `requirements` | `array[string]` | `product_spec.requirements` |
| `allowed_paths` | `array[string]` | `required` |
| `forbidden_paths` | `array[string]` | `required` |
| `scope_budget` | `object` | `required` |
| `acceptance` | `array[string]` | `required` |
| `verification` | `array[object]` | `required` |
| `non_goals` | `array[string]` | `required` |
| `stop_conditions` | `array[string]` | `required` |
| `rollback` | `string` | `required` |
| `handoff_requirements` | `array[string]` | `required` |
| `implementer_actor_id` | `string` | `required` |
| `implementer_session_id` | `string` | `required` |
| `requirement_digest` | `string` | `^[0-9a-f]{64}$` |

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

### Primary outcome

Record the primary outcome using the fields above; link IDs and direct proof where available.

### Value slice

Record the value slice using the fields above; link IDs and direct proof where available.

### Proof slice

Record the proof slice using the fields above; link IDs and direct proof where available.

### Requirements

Record the requirements using the fields above; link IDs and direct proof where available.

### Assumptions and constraints

Record the assumptions and constraints using the fields above; link IDs and direct proof where available.

### Allowed paths

Record the allowed paths using the fields above; link IDs and direct proof where available.

### Forbidden paths

Record the forbidden paths using the fields above; link IDs and direct proof where available.

### Solution ladder

Record the solution ladder using the fields above; link IDs and direct proof where available.

### Scope budget

Record the scope budget using the fields above; link IDs and direct proof where available.

### Acceptance and verification

Record the acceptance and verification using the fields above; link IDs and direct proof where available.

### Non-goals

Record the non-goals using the fields above; link IDs and direct proof where available.

### Stop and replan conditions

Record the stop and replan conditions using the fields above; link IDs and direct proof where available.

### Rollback

Record the rollback using the fields above; link IDs and direct proof where available.

### Handoff

Record the handoff using the fields above; link IDs and direct proof where available.

