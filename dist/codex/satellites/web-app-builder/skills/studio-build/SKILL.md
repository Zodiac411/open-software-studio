---

name: studio-build
description: Implement one approved repository work package with reuse-first scope, required safety, and direct verification.
---
# Studio Build

Use this front-door only when the request needs repository evidence, allowed paths, smallest safe change, tests, and handoff.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `IMPLEMENTATION_HANDOFF`, `EVIDENCE_RECEIPT`.
- This skill does not own planning authority or review acceptance.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current project state and the request for repository evidence, allowed paths, smallest safe change, tests, and handoff
- Method: Apply a bounded review of repository evidence, allowed paths, smallest safe change, tests, and handoff and preserve the evidence trail.
- Output: named IMPLEMENTATION_HANDOFF, EVIDENCE_RECEIPT outputs with evidence and one next action
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
