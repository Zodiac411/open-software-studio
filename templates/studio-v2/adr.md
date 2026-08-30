---

schema: studio.artifact-template/v2
artifact_type: ADR
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# ADR

Capture one durable decision, the options considered, consequences, evidence, and revisit trigger.
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
| `decision` | `string` | `required` |
| `status` | `string` | `required` |
| `context` | `string` | `required` |
| `options` | `array[object]` | `required` |
| `consequences` | `string` | `required` |
| `evidence` | `array[object]` | `required` |
| `revisit_trigger` | `string` | `required` |

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

### Context

Record the context using the fields above; link IDs and direct proof where available.

### Decision

Record the decision using the fields above; link IDs and direct proof where available.

### Options

Record the options using the fields above; link IDs and direct proof where available.

### Consequences

Record the consequences using the fields above; link IDs and direct proof where available.

### Evidence

Record the evidence using the fields above; link IDs and direct proof where available.

### Revisit trigger

Record the revisit trigger using the fields above; link IDs and direct proof where available.

