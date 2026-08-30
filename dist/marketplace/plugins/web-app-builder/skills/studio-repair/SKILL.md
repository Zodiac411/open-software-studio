---

name: studio-repair
description: Execute only an accepted bounded repair package and emit fresh evidence for independent re-review.
---
# Studio Repair

Use this front-door only when the request needs accepted findings, allowed paths, regression proof, and stop conditions.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `REPAIR_PACKAGE`, `IMPLEMENTATION_HANDOFF`.
- This skill does not own optional finding promotion.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current project state and the request for accepted findings, allowed paths, regression proof, and stop conditions
- Method: Apply a bounded review of accepted findings, allowed paths, regression proof, and stop conditions and preserve the evidence trail.
- Output: named REPAIR_PACKAGE, IMPLEMENTATION_HANDOFF outputs with evidence and one next action
- Stop: Stop when required context or direct proof is missing.
- Escalate: Escalate unresolved authority, safety, or scope conflicts instead of guessing.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
