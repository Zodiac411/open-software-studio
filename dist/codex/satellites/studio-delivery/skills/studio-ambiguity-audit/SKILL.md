---

name: studio-ambiguity-audit
description: Find ambiguous nouns, verbs, actors, boundaries, and success statements before they harden into requirements.
---
# Studio Ambiguity Audit

Use this lens only when the request needs observable language, missing decisions, and clarify-or-stop questions.

## Contract

- Read current project state, governing requirements, and the current SHA before making a claim.
- Produce or update only the owned outputs: `PROJECT_BRIEF`, `PRODUCT_SPEC`.
- This skill does not own inventing product decisions.
- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.

## Lens contract

- Input: brief, requirements, actor, boundary, and success language
- Method: Mark ambiguous nouns, verbs, actors, boundaries, and measures; convert each into a decision question.
- Output: ambiguity register with clarified wording or an owner for each open decision
- Stop: Stop before planning when an ambiguity changes the actor, boundary, or success measure.
- Escalate: Escalate unanswered clarify-or-stop questions to the authority owner.

## Procedure

1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.
2. Read only the inputs named by the lens contract and apply its method to the smallest adequate scope.
3. Make requirements, acceptance, scope, proof, and the contract stop condition observable.
4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.
5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.

## Human gates

Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.
