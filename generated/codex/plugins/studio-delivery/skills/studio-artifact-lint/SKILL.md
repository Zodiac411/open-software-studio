---

name: studio-artifact-lint
description: Lint Studio artifacts for IDs, authority, links, required fields, scope, proof, freshness, and unsupported claims.
---
# Studio Artifact Lint

Use this lens only when the request needs deterministic artifact and template integrity.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `EVIDENCE_RECEIPT`, `INDEPENDENT_REVIEW`.
- This skill does not own silently filling missing facts.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: artifact data, schema, references, current revision, and evidence receipts
- Method: Validate IDs, types, links, required fields, scope, proof, freshness, and unsupported claims deterministically.
- Output: lint result with typed errors, source field, evidence gap, and next action
- Stop: Reject the artifact on schema, broken-reference, stale-proof, or overclaim errors.
- Escalate: Escalate missing authority or unverifiable external evidence as UNPROVEN.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: artifact data, schema, references, current revision, and evidence receipts
3. Apply the lens method: Validate IDs, types, links, required fields, scope, proof, freshness, and unsupported claims deterministically.
4. Produce the lens output: lint result with typed errors, source field, evidence gap, and next action
5. Enforce the stop condition: Reject the artifact on schema, broken-reference, stale-proof, or overclaim errors.
6. Follow the escalation path: Escalate missing authority or unverifiable external evidence as UNPROVEN.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
