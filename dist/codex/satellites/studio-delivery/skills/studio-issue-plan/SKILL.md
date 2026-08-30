---

name: studio-issue-plan
description: Compile one reviewable Studio work package into an idempotent GitHub issue projection with dependencies and proof.
---
# Studio Issue Plan

Use this lens only when the request needs issue-ready scope, labels, dependencies, and drift detection.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `WORK_PACKAGE`, `MILESTONE_RECEIPT`.
- This skill does not own making GitHub a second authority.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: frozen work package, dependencies, repository identity, and proof plan
- Method: Project one bounded package into create/update/no-op/stale/conflict actions while preserving Studio authority.
- Output: typed issue or milestone reconciliation plan with idempotency keys and drift notes
- Stop: Do not apply when repository identity, base revision, or action conflict is unresolved.
- Escalate: Escalate connector permission or unsupported-operation differences without fabricating success.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
