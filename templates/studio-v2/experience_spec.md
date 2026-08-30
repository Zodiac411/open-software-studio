---

schema: studio.artifact-template/v2
artifact_type: EXPERIENCE_SPEC
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# EXPERIENCE_SPEC

Describe the actor's flow, states, responsive behavior, accessibility, fallback, and visual proof.
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
| `actor` | `string` | `required` |
| `flow` | `string` | `required` |
| `states` | `array[object]` | `required` |
| `components` | `array[object]` | `required` |
| `responsive` | `string` | `required` |
| `accessibility` | `string` | `required` |
| `fallback` | `string` | `required` |
| `visual_qa` | `string` | `required` |

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

### Actor and job

Record the actor and job using the fields above; link IDs and direct proof where available.

### Task flow

Record the task flow using the fields above; link IDs and direct proof where available.

### Surface map

Record the surface map using the fields above; link IDs and direct proof where available.

### State matrix

Record the state matrix using the fields above; link IDs and direct proof where available.

### Component map

Record the component map using the fields above; link IDs and direct proof where available.

### Interaction rules

Record the interaction rules using the fields above; link IDs and direct proof where available.

### Responsive composition

Record the responsive composition using the fields above; link IDs and direct proof where available.

### Accessibility acceptance

Record the accessibility acceptance using the fields above; link IDs and direct proof where available.

### Dreamfield material budget

Record the dreamfield material budget using the fields above; link IDs and direct proof where available.

### Fallbacks

Record the fallbacks using the fields above; link IDs and direct proof where available.

### Visual QA

Record the visual qa using the fields above; link IDs and direct proof where available.
