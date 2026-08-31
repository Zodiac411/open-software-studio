---

name: studio-research
description: Research only decision-changing external evidence and record source quality, freshness, license, and confidence.
---
# Studio Research

Use this front-door only when the request needs primary sources, repository health, current APIs, trade-offs, and refresh triggers.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `RESEARCH_DECISION_MEMO`, `SOURCE_LEDGER`.
- This skill does not own unsupported claims or implementation.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: current project state and the request for primary sources, repository health, current APIs, trade-offs, and refresh triggers
- Method: Apply a bounded review of primary sources, repository health, current APIs, trade-offs, and refresh triggers and preserve the evidence trail.
- Output: named RESEARCH_DECISION_MEMO, SOURCE_LEDGER outputs with evidence and one next action
- Stop: Stop when required context or direct proof is missing.
- Escalate: Escalate unresolved authority, safety, or scope conflicts instead of guessing.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Gather the lens inputs: current project state and the request for primary sources, repository health, current APIs, trade-offs, and refresh triggers
3. Apply the lens method: Apply a bounded review of primary sources, repository health, current APIs, trade-offs, and refresh triggers and preserve the evidence trail.
4. Produce the lens output: named RESEARCH_DECISION_MEMO, SOURCE_LEDGER outputs with evidence and one next action
5. Enforce the stop condition: Stop when required context or direct proof is missing.
6. Follow the escalation path: Escalate unresolved authority, safety, or scope conflicts instead of guessing.
7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
