---

schema: studio.artifact-template/v2
artifact_type: VERIFICATION_CONTRACT
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# VERIFICATION_CONTRACT

Map every requirement to direct commands, probes, evidence levels, failure policy, and rollback.
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
| `requirements` | `array[string]` | `product_spec.requirements` |
| `proof_levels` | `array[string]` | `required` |
| `commands` | `array[string]` | `required` |
| `runtime_probes` | `array[string]` | `required` |
| `failure_policy` | `string` | `required` |
| `rollback` | `string` | `required` |

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

### Requirement-to-proof map

Record the requirement-to-proof map using the fields above; link IDs and direct proof where available.

### Commands

Record the commands using the fields above; link IDs and direct proof where available.

### Runtime probes

Record the runtime probes using the fields above; link IDs and direct proof where available.

### Failure policy

Record the failure policy using the fields above; link IDs and direct proof where available.

### Rollback

Record the rollback using the fields above; link IDs and direct proof where available.
