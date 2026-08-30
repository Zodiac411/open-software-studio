---

schema: studio.artifact-template/v2
artifact_type: SOURCE_LEDGER
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# SOURCE_LEDGER

Preserve claim-level source, freshness, license, strength, and decision links.
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
| `source` | `string` | `required` |
| `retrieved` | `string` | `date-time` |
| `freshness` | `string` | `required` |
| `license` | `string` | `required` |
| `strength` | `string` | `required` |
| `affected_decision` | `string` | `required` |

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

### Claim ledger

Record the claim ledger using the fields above; link IDs and direct proof where available.

### Source quality

Record the source quality using the fields above; link IDs and direct proof where available.

### Freshness

Record the freshness using the fields above; link IDs and direct proof where available.

### License and attribution

Record the license and attribution using the fields above; link IDs and direct proof where available.

### Decision links

Record the decision links using the fields above; link IDs and direct proof where available.
