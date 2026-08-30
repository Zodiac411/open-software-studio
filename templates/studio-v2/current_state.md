---

schema: studio.artifact-template/v2
artifact_type: CURRENT_STATE
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# CURRENT_STATE

Expose the current phase, revision, proof, blockers, and exactly one next action.
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
| `phase` | `string` | `required` |
| `status` | `string` | `required` |
| `active_wp` | `string` | `required` |
| `current_sha` | `string` | `^[0-9a-f]{40}$` |
| `next_action` | `string` | `required` |
| `blocking_items` | `string` | `required` |
| `proof` | `string` | `required` |
| `last_event` | `string` | `required` |
| `recovery_files` | `string` | `required` |

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

### Current phase

Record the current phase using the fields above; link IDs and direct proof where available.

### Active work package

Record the active work package using the fields above; link IDs and direct proof where available.

### Current revision

Record the current revision using the fields above; link IDs and direct proof where available.

### Proof and limitations

Record the proof and limitations using the fields above; link IDs and direct proof where available.

### Blocking items

Record the blocking items using the fields above; link IDs and direct proof where available.

### Recovery files

Record the recovery files using the fields above; link IDs and direct proof where available.

### Next action

Record the next action using the fields above; link IDs and direct proof where available.
