---

schema: studio.artifact-template/v2
artifact_type: RELEASE_RECEIPT
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# RELEASE_RECEIPT

Qualify one release revision with review, package evidence, limitations, waivers, rollback, and approval.
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
| `version` | `string` | `required` |
| `revision` | `string` | `^[0-9a-f]{40}$` |
| `review_id` | `string` | `independent_review.review_id` |
| `requirement_digest` | `string` | `^[0-9a-f]{64}$` |
| `package_digests` | `array[object]` | `required` |
| `environment` | `object` | `required` |
| `evidence` | `array[object]` | `required` |
| `limitations` | `string` | `required` |
| `waivers` | `array[string]` | `required` |
| `rollback` | `string` | `required` |
| `owner_approval` | `string` | `required` |

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

### Revision

Record the revision using the fields above; link IDs and direct proof where available.

### Environment

Record the environment using the fields above; link IDs and direct proof where available.

### Evidence

Record the evidence using the fields above; link IDs and direct proof where available.

### Known limitations

Record the known limitations using the fields above; link IDs and direct proof where available.

### Waivers

Record the waivers using the fields above; link IDs and direct proof where available.

### Rollback

Record the rollback using the fields above; link IDs and direct proof where available.

### Owner approval

Record the owner approval using the fields above; link IDs and direct proof where available.

