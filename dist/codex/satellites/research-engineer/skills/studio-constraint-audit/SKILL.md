---

name: studio-constraint-audit
description: Identify technical, legal, platform, accessibility, security, budget, and delivery constraints with evidence.
---
# Studio Constraint Audit

Use this lens only when the request needs hard constraints, soft preferences, conflicts, and missing authority.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PROJECT_BRIEF`, `VERIFICATION_CONTRACT`.
- This skill does not own weakening a required safeguard.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: brief, authorities, platform context, and proposed solution
- Method: Separate hard constraints from preferences, identify conflicts, and attach evidence or authority to each.
- Output: constraint ledger with source, severity, conflict, and enforcement point
- Stop: Stop when a hard constraint is missing authority or conflicts with the proposed outcome.
- Escalate: Escalate legal, security, accessibility, or platform conflicts to the named authority.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: brief, authorities, platform context, and proposed solution
3. Apply the lens method: Separate hard constraints from preferences, identify conflicts, and attach evidence or authority to each.
4. Produce the lens output: constraint ledger with source, severity, conflict, and enforcement point
5. Enforce the stop condition: Stop when a hard constraint is missing authority or conflicts with the proposed outcome.
6. Follow the escalation path: Escalate legal, security, accessibility, or platform conflicts to the named authority.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
