---

schema: studio.artifact-template/v2
artifact_type: RESEARCH_DECISION_MEMO
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# RESEARCH_DECISION_MEMO

Connect decision-changing claims to source quality, trade-offs, confidence, and refresh triggers.
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
| `claims` | `array[object]` | `required` |
| `decision` | `string` | `required` |
| `trade_offs` | `string` | `required` |
| `confidence` | `string` | `required` |
| `refresh_trigger` | `string` | `required` |

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

### Decision question

Record the decision question using the fields above; link IDs and direct proof where available.

### Material claims

Record the material claims using the fields above; link IDs and direct proof where available.

### Options

Record the options using the fields above; link IDs and direct proof where available.

### Decision

Record the decision using the fields above; link IDs and direct proof where available.

### Trade-offs

Record the trade-offs using the fields above; link IDs and direct proof where available.

### Confidence

Record the confidence using the fields above; link IDs and direct proof where available.

### Refresh trigger

Record the refresh trigger using the fields above; link IDs and direct proof where available.
