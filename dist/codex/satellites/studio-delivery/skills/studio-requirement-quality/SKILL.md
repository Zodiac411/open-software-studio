---

name: studio-requirement-quality
description: Check requirements for observable behavior, ownership, priority, scenario, acceptance, proof, and traceability.
---
# Studio Requirement Quality

Use this lens only when the request needs testable requirement wording and conflict/gap detection.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PRODUCT_SPEC`, `VERIFICATION_CONTRACT`.
- This skill does not own adding unrequested features.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: requirements, scenarios, owners, acceptance, and proof plan
- Method: Check each requirement for actor, behavior, priority, observable acceptance, proof, and traceability.
- Output: requirement quality findings linked to IDs and repair wording
- Stop: Stop approval when a must-have requirement is not observable or lacks proof.
- Escalate: Escalate conflicting or ownerless requirements before freezing the plan.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: requirements, scenarios, owners, acceptance, and proof plan
3. Apply the lens method: Check each requirement for actor, behavior, priority, observable acceptance, proof, and traceability.
4. Produce the lens output: requirement quality findings linked to IDs and repair wording
5. Enforce the stop condition: Stop approval when a must-have requirement is not observable or lacks proof.
6. Follow the escalation path: Escalate conflicting or ownerless requirements before freezing the plan.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
