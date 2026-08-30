---

schema: studio.artifact-template/v2
artifact_type: PROJECT_INDEX
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# PROJECT_INDEX

Keep project identity, authority, phase, and recovery entry points in one readable index.
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
| `title` | `string` | `required` |
| `authority` | `string` | `required` |
| `status` | `string` | `required` |
| `version` | `string` | `required` |
| `owner` | `string` | `required` |
| `approved_by` | `string` | `required` |
| `applies_to` | `string` | `required` |
| `snapshot` | `string` | `required` |
| `last_verified` | `string` | `date-time` |
| `next_review_trigger` | `string` | `date-time` |

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

### Project in one paragraph

Record the project in one paragraph using the fields above; link IDs and direct proof where available.

### Authority map

Record the authority map using the fields above; link IDs and direct proof where available.

### Read-by-task routes

Record the read-by-task routes using the fields above; link IDs and direct proof where available.

### Current phase

Record the current phase using the fields above; link IDs and direct proof where available.

### Immediate next action

Record the immediate next action using the fields above; link IDs and direct proof where available.

### Recovery path

Record the recovery path using the fields above; link IDs and direct proof where available.
