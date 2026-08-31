---

name: studio-premortem
description: Run a focused pre-mortem for a high-risk plan and connect likely failures to signals, prevention, and fallback.
---
# Studio Premortem

Use this lens only when the request needs early failure signals and recovery.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `ARCHITECTURE`, `DELIVERY_PLAN`.
- This skill does not own expanding the project because of hypotheticals.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: high-risk plan, dependencies, assumptions, and fallback options
- Method: Imagine a bounded failure, trace its earliest signal, prevention, owner, and fallback.
- Output: short failure register tied to plan decisions and monitoring signals
- Stop: Stop plan approval when a likely failure has neither prevention nor fallback.
- Escalate: Escalate risks that exceed the approved budget or cannot be observed early.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: high-risk plan, dependencies, assumptions, and fallback options
3. Apply the lens method: Imagine a bounded failure, trace its earliest signal, prevention, owner, and fallback.
4. Produce the lens output: short failure register tied to plan decisions and monitoring signals
5. Enforce the stop condition: Stop plan approval when a likely failure has neither prevention nor fallback.
6. Follow the escalation path: Escalate risks that exceed the approved budget or cannot be observed early.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
