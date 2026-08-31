---

name: studio-scope-guard
description: Apply the necessity, reuse, native, dependency, and minimum ladder before adding Studio scope.
---
# Studio Scope Guard

Use this lens only when the request needs scope budget, reuse ledger, overshoot audit, safety exemptions, and replan triggers.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PROJECT_BRIEF`, `WORK_PACKAGE`.
- This skill does not own removing security, accessibility, validation, or error handling.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: approved outcome, scope budget, reuse candidates, and safety requirements
- Method: Apply necessity, reuse, native, dependency, and minimum-solution checks; record the rejected overshoot.
- Output: bounded scope decision with budget, reuse ledger, and explicit safety exceptions
- Stop: Stop and replan when the budget is exceeded or a required safeguard would be removed.
- Escalate: Escalate unresolved scope or safety conflicts to the project owner.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: approved outcome, scope budget, reuse candidates, and safety requirements
3. Apply the lens method: Apply necessity, reuse, native, dependency, and minimum-solution checks; record the rejected overshoot.
4. Produce the lens output: bounded scope decision with budget, reuse ledger, and explicit safety exceptions
5. Enforce the stop condition: Stop and replan when the budget is exceeded or a required safeguard would be removed.
6. Follow the escalation path: Escalate unresolved scope or safety conflicts to the project owner.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
