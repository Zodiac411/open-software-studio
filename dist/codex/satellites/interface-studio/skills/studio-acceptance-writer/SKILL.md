---

name: studio-acceptance-writer
description: Turn approved outcomes into precise acceptance criteria with direct commands, probes, and evidence levels.
---
# Studio Acceptance Writer

Use this lens only when the request needs observable acceptance and proof contract.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PRODUCT_SPEC`, `VERIFICATION_CONTRACT`, `WORK_PACKAGE`.
- This skill does not own claiming a result before observation.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: approved outcomes, requirements, and verification capabilities
- Method: Translate outcomes into observable criteria with command/probe, expected result, evidence level, and failure handling.
- Output: acceptance table that maps every required outcome to direct proof
- Stop: Stop when a criterion cannot name an observation or acceptable limitation.
- Escalate: Escalate proof gaps instead of lowering the acceptance bar silently.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: approved outcomes, requirements, and verification capabilities
3. Apply the lens method: Translate outcomes into observable criteria with command/probe, expected result, evidence level, and failure handling.
4. Produce the lens output: acceptance table that maps every required outcome to direct proof
5. Enforce the stop condition: Stop when a criterion cannot name an observation or acceptable limitation.
6. Follow the escalation path: Escalate proof gaps instead of lowering the acceptance bar silently.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
