---

name: studio-domain-model
description: Model the minimum entities, relationships, invariants, ownership, and unknowns needed for the next decision.
---
# Studio Domain Model

Use this lens only when the request needs domain boundaries and durable vocabulary.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `DOMAIN_MODEL`.
- This skill does not own premature database or subsystem design.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: approved outcome, vocabulary, actors, data, and ownership
- Method: Model only the minimum entities, relationships, invariants, ownership, and unknowns needed for the next decision.
- Output: domain model with stable IDs, relationship direction, invariants, and open questions
- Stop: Stop when an invariant or ownership boundary is unknown for a required behavior.
- Escalate: Escalate cross-boundary ownership conflicts before architecture selection.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
