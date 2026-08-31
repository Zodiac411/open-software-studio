---

name: studio-improve
description: Distil verified project learnings into bounded improvements without smuggling optional work into current acceptance.
---
# Studio Improve

Use this front-door only when the request needs retro evidence, friction, decisions, and separately scoped improvements.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `RETRO_DISTILLATION`, `CHANGE_PROPOSAL`.
- This skill does not own unapproved scope expansion.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current project state and the request for retro evidence, friction, decisions, and separately scoped improvements
- Method: Apply a bounded review of retro evidence, friction, decisions, and separately scoped improvements and preserve the evidence trail.
- Output: named RETRO_DISTILLATION, CHANGE_PROPOSAL outputs with evidence and one next action
- Stop: Stop when required context or direct proof is missing.
- Escalate: Escalate unresolved authority, safety, or scope conflicts instead of guessing.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: current project state and the request for retro evidence, friction, decisions, and separately scoped improvements
3. Apply the lens method: Apply a bounded review of retro evidence, friction, decisions, and separately scoped improvements and preserve the evidence trail.
4. Produce the lens output: named RETRO_DISTILLATION, CHANGE_PROPOSAL outputs with evidence and one next action
5. Enforce the stop condition: Stop when required context or direct proof is missing.
6. Follow the escalation path: Escalate unresolved authority, safety, or scope conflicts instead of guessing.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
