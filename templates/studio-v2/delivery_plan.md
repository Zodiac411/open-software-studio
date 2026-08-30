---

schema: studio.artifact-template/v2
artifact_type: DELIVERY_PLAN
authority: Studio catalog
status: DRAFT
version: 2.0.0
---
# DELIVERY_PLAN

Sequence bounded work packages with dependencies, requirements, budget, and review gates.
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
| `work_packages` | `array[string]` | `required` |
| `dependencies` | `array[string]` | `required` |
| `requirements` | `array[string]` | `product_spec.requirements` |
| `scope_budget` | `object` | `required` |
| `review_gate` | `string` | `required` |

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

### Dependency graph

Record the dependency graph using the fields above; link IDs and direct proof where available.

### Work package table

Record the work package table using the fields above; link IDs and direct proof where available.

### Scope budget

Record the scope budget using the fields above; link IDs and direct proof where available.

### Review gate

Record the review gate using the fields above; link IDs and direct proof where available.
