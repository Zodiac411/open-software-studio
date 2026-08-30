---

name: studio-handoff
description: Compile a fact-first implementation handoff from the current branch, SHA, diff, checks, evidence, and scope delta.
---
# Studio Handoff

Use this front-door only when the request needs handoff claim package and reviewer action.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `IMPLEMENTATION_HANDOFF`.
- This skill does not own review disposition.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Apply the smallest adequate solution ladder and record why higher machinery is not required.
3. Make requirements, acceptance, scope, proof level, and stop conditions observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
