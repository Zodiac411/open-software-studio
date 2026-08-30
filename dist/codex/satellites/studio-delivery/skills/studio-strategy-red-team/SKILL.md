---

name: studio-strategy-red-team
description: Challenge load-bearing assumptions, hidden coupling, false proof, scope gaming, and authority conflicts.
---
# Studio Strategy Red Team

Use this lens only when the request needs adversarial plan and review critique.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `INDEPENDENT_REVIEW`, `CHANGE_PROPOSAL`.
- This skill does not own quietly redesigning the approved plan.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: approved plan, evidence, authority map, and scope delta
- Method: Adversarially test load-bearing assumptions, hidden coupling, false proof, scope gaming, and authority conflicts.
- Output: independent findings with severity, evidence, repair acceptance, and disposition
- Stop: Reject acceptance when a blocking claim is unsupported or the reviewed scope is stale.
- Escalate: Escalate blocking findings to a fresh independent reviewer; never repair silently.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
