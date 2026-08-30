---

name: studio-assumption-map
description: Extract and rank assumptions by uncertainty, impact, owner, evidence, and cheapest useful test.
---
# Studio Assumption Map

Use this lens only when the request needs load-bearing assumptions and validation order.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PROJECT_BRIEF`, `RESEARCH_DECISION_MEMO`.
- This skill does not own presenting assumptions as facts.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: brief, constraints, unknowns, and available evidence
- Method: Rank assumptions by uncertainty and impact, assign an owner, and choose the cheapest useful test.
- Output: assumption map ordered by risk with evidence and validation sequence
- Stop: Stop or mark UNPROVEN when a load-bearing assumption has no owner or test.
- Escalate: Escalate high-impact assumptions that cannot be cheaply tested.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
