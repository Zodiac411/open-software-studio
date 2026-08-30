---

schema: studio.artifact-template/v2
artifact_type: DOMAIN_MODEL
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# DOMAIN_MODEL

Define only the entities, relationships, invariants, ownership, and unknowns needed next.
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
| `entities` | `array[object]` | `required` |
| `relationships` | `array[object]` | `required` |
| `invariants` | `array[object]` | `required` |
| `ownership` | `array[object]` | `required` |
| `unknowns` | `array[object]` | `required` |

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

### Entities

Record the entities using the fields above; link IDs and direct proof where available.

### Relationships

Record the relationships using the fields above; link IDs and direct proof where available.

### Invariants

Record the invariants using the fields above; link IDs and direct proof where available.

### Ownership

Record the ownership using the fields above; link IDs and direct proof where available.

### Unknowns

Record the unknowns using the fields above; link IDs and direct proof where available.
