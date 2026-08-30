---

schema: studio.artifact-template/v2
artifact_type: IMPLEMENTATION_HANDOFF
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# IMPLEMENTATION_HANDOFF

Let an independent reviewer reproduce what changed, what was tested, and what remains unproven.
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
| `wp_id` | `string` | `work_package.wp_id` |
| `base_sha` | `string` | `^[0-9a-f]{40}$` |
| `head_sha` | `string` | `^[0-9a-f]{40}$` |
| `branch` | `string` | `required` |
| `claimed_outcomes` | `array[string]` | `required` |
| `files` | `array[string]` | `required` |
| `commands` | `array[string]` | `required` |
| `evidence` | `array[object]` | `required` |
| `scope_delta` | `object` | `required` |
| `unproven` | `array[string]` | `required` |
| `next_action` | `string` | `required` |
| `reviewer_action` | `string` | `required` |

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

### Baseline and head

Record the baseline and head using the fields above; link IDs and direct proof where available.

### Claimed outcomes

Record the claimed outcomes using the fields above; link IDs and direct proof where available.

### Files and diff

Record the files and diff using the fields above; link IDs and direct proof where available.

### Observed verification

Record the observed verification using the fields above; link IDs and direct proof where available.

### Evidence levels

Record the evidence levels using the fields above; link IDs and direct proof where available.

### Scope delta

Record the scope delta using the fields above; link IDs and direct proof where available.

### Failures and unproven boundaries

Record the failures and unproven boundaries using the fields above; link IDs and direct proof where available.

### Residual risks

Record the residual risks using the fields above; link IDs and direct proof where available.

### Rollback

Record the rollback using the fields above; link IDs and direct proof where available.

### Requested reviewer action

Record the requested reviewer action using the fields above; link IDs and direct proof where available.
