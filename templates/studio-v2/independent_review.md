---

schema: studio.artifact-template/v2
artifact_type: INDEPENDENT_REVIEW
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# INDEPENDENT_REVIEW

Prove an independent reviewer examined the exact requirements, revision, scope, evidence, and findings.
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
| `review_id` | `string` | `independent_review.review_id` |
| `reviewer_actor_id` | `string` | `required` |
| `reviewer_session_id` | `string` | `required` |
| `reviewer_role` | `string` | `required` |
| `reviewer_context` | `string` | `required` |
| `implementer_actor_id` | `string` | `required` |
| `implementer_session_id` | `string` | `required` |
| `reviewed_base_sha` | `string` | `^[0-9a-f]{40}$` |
| `reviewed_head_sha` | `string` | `^[0-9a-f]{40}$` |
| `wp_id` | `string` | `work_package.wp_id` |
| `requirements` | `array[string]` | `product_spec.requirements` |
| `requirements_digest` | `string` | `^[0-9a-f]{64}$` |
| `artifact_ids` | `array[string]` | `required` |
| `evidence_digest` | `string` | `^[0-9a-f]{64}$` |
| `independent_checks` | `array[object]` | `required` |
| `scope_delta` | `object` | `required` |
| `findings` | `array[object]` | `required` |
| `disposition` | `string` | `required` |
| `conditions` | `array[string]` | `required` |

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

### Independence

Record the independence using the fields above; link IDs and direct proof where available.

### Reviewed state

Record the reviewed state using the fields above; link IDs and direct proof where available.

### Requirement coverage

Record the requirement coverage using the fields above; link IDs and direct proof where available.

### Independent checks

Record the independent checks using the fields above; link IDs and direct proof where available.

### Findings

Record the findings using the fields above; link IDs and direct proof where available.

### Disposition

Record the disposition using the fields above; link IDs and direct proof where available.

### Acceptance conditions

Record the acceptance conditions using the fields above; link IDs and direct proof where available.
