---

schema: studio.artifact-template/v2
artifact_type: EVIDENCE_RECEIPT
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# EVIDENCE_RECEIPT

Record one direct observation with its requirement, command, result, digest, environment, and limitation.
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
| `evidence_id` | `string` | `evidence_receipt.evidence_id` |
| `requirement` | `string` | `product_spec.requirements` |
| `level` | `string` | `required` |
| `command_or_probe` | `string` | `required` |
| `observed` | `string` | `required` |
| `timestamp` | `string` | `date-time` |
| `limitations` | `string` | `required` |
| `sequence` | `string` | `required` |
| `head_sha` | `string` | `^[0-9a-f]{40}$` |
| `exit_code` | `string` | `required` |
| `environment` | `object` | `required` |
| `observed_output_digest` | `string` | `^[0-9a-f]{64}$` |

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

### Requirement

Record the requirement using the fields above; link IDs and direct proof where available.

### Evidence level

Record the evidence level using the fields above; link IDs and direct proof where available.

### Command or probe

Record the command or probe using the fields above; link IDs and direct proof where available.

### Observed result

Record the observed result using the fields above; link IDs and direct proof where available.

### Limitations

Record the limitations using the fields above; link IDs and direct proof where available.
