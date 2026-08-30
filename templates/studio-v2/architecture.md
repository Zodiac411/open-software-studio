---

schema: studio.artifact-template/v2
artifact_type: ARCHITECTURE
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# ARCHITECTURE

Make boundaries, quality attributes, dependencies, trust edges, recovery, and revisit triggers reviewable.
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
| `verified_current_architecture` | `string` | `required` |
| `boundaries` | `string` | `required` |
| `quality_attributes` | `string` | `required` |
| `options` | `array[object]` | `required` |
| `chosen_architecture` | `string` | `required` |
| `failure_recovery` | `string` | `required` |
| `security` | `string` | `required` |
| `dependencies` | `array[string]` | `required` |
| `rollback` | `string` | `required` |
| `revisit_triggers` | `string` | `required` |

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

### Verified current architecture

Record the verified current architecture using the fields above; link IDs and direct proof where available.

### Ownership boundaries

Record the ownership boundaries using the fields above; link IDs and direct proof where available.

### Quality attributes

Record the quality attributes using the fields above; link IDs and direct proof where available.

### Options considered

Record the options considered using the fields above; link IDs and direct proof where available.

### Chosen architecture

Record the chosen architecture using the fields above; link IDs and direct proof where available.

### Data and control flow

Record the data and control flow using the fields above; link IDs and direct proof where available.

### Failure and recovery

Record the failure and recovery using the fields above; link IDs and direct proof where available.

### Security and trust boundaries

Record the security and trust boundaries using the fields above; link IDs and direct proof where available.

### Dependency policy

Record the dependency policy using the fields above; link IDs and direct proof where available.

### Migration and rollback

Record the migration and rollback using the fields above; link IDs and direct proof where available.

### ADR index

Record the adr index using the fields above; link IDs and direct proof where available.

### Revisit triggers

Record the revisit triggers using the fields above; link IDs and direct proof where available.
