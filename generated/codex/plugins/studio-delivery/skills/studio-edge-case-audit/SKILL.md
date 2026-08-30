---

name: studio-edge-case-audit
description: Elicit relevant failure, boundary, accessibility, concurrency, migration, and recovery cases for a bounded change.
---
# Studio Edge Case Audit

Use this lens only when the request needs critical edge cases proportional to risk.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `VERIFICATION_CONTRACT`, `WORK_PACKAGE`.
- This skill does not own inventing a test matrix without a requirement.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: requirements, flow/state model, risk, and recovery constraints
- Method: Select only failure, boundary, accessibility, concurrency, migration, and recovery cases that could change acceptance.
- Output: prioritized edge-case checks with trigger, expected behavior, and recovery proof
- Stop: Stop when a critical failure path has no safe fallback or owner.
- Escalate: Escalate critical data-loss, security, or accessibility cases immediately.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
