---

name: studio-architecture-review
description: Review architecture boundaries, quality attributes, dependencies, trust edges, failure recovery, and revisit triggers.
---
# Studio Architecture Review

Use this lens only when the request needs evidence-led architecture fitness and risk.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `ARCHITECTURE`, `INDEPENDENT_REVIEW`.
- This skill does not own implementation acceptance.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current architecture, proposed boundaries, quality attributes, and evidence
- Method: Review ownership, trust edges, dependencies, failure recovery, security, and revisit triggers against requirements.
- Output: architecture fitness findings and accepted boundary decisions
- Stop: Reject the option when a critical trust edge, failure path, or quality attribute is unaddressed.
- Escalate: Escalate architecture risks that require a new authority, dependency, or migration.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: current architecture, proposed boundaries, quality attributes, and evidence
3. Apply the lens method: Review ownership, trust edges, dependencies, failure recovery, security, and revisit triggers against requirements.
4. Produce the lens output: architecture fitness findings and accepted boundary decisions
5. Enforce the stop condition: Reject the option when a critical trust edge, failure path, or quality attribute is unaddressed.
6. Follow the escalation path: Escalate architecture risks that require a new authority, dependency, or migration.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
