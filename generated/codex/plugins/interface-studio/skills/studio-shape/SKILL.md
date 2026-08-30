---

name: studio-shape
description: Shape an ambiguous product or repository request into a decision-ready scope and smallest adequate solution.
---
# Studio Shape

Use this front-door only when the request needs problem framing, assumptions, constraints, solution ladder, scope budget, and disposition.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PROJECT_BRIEF`, `CHANGE_PROPOSAL`.
- This skill does not own premature implementation.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current project state and the request for problem framing, assumptions, constraints, solution ladder, scope budget, and disposition
- Method: Apply a bounded review of problem framing, assumptions, constraints, solution ladder, scope budget, and disposition and preserve the evidence trail.
- Output: named PROJECT_BRIEF, CHANGE_PROPOSAL outputs with evidence and one next action
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
