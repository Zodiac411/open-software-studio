# Studio V2 final acceptance

Overall result: `BLOCKED`

Local remediation code head: `f300908d5306085f72215ce09e95f5cf8f434033`

Branch: `studio-v2-bootstrap`

The prior `PASS_WITH_LIMITATIONS` conclusion is superseded. It referred to
source checkpoint `468e231...` and a ChatGPT archive that predates the current
control-plane, schema, evaluation, and package repairs.

## Current matrix

| Requirement | Result | Current evidence |
|---|---|---|
| One canonical catalog | `PASS_WITH_LIMITATIONS` | Catalog now owns prompts, recipes, app references, icon sources, schemas, templates, validation inputs, and source-manifest roots. Final independent review is pending. |
| Deterministic umbrella and satellites | `PASS` | Canonical check and two clean-checkout builds pass. |
| Strict review, close, and release gates | `PASS_WITH_LIMITATIONS` | Six focused regressions cover self-review, stale SHA, atomic release failure, idempotent close, generic plan/track, evidence, and malformed artifact compilation. Independent review is pending. |
| Versioned schemas and artifact compiler | `PASS_WITH_LIMITATIONS` | Typed schemas reject unknown/malformed fields; compiler emits Markdown, JSON/YAML, GitHub, and Google Docs payloads. Host publishing is not exercised. |
| Recovery coherence and live SHA | `PASS_WITH_LIMITATIONS` | CLI now maintains typed events/projections and blocks stale state. Existing historical pilot state must be refreshed before reuse. |
| Behavioral evaluations and CI | `PASS_WITH_LIMITATIONS` | Executable regressions, Windows/Linux CI, security/archive checks, deterministic builds, and optional MCP smoke are versioned. Hosted CI has not run on the unpublished commits. |
| Codex installation | `PASS_WITH_LIMITATIONS` | Previous 2.0.0 installation remains present; the repaired package has not yet been reinstalled and freshly re-proven. |
| ChatGPT installation and fresh chat | `BLOCKED` | Installed archive predates the remediation. Re-upload and a fresh invocation are required. |
| GitHub and Drive reads | `PASS` | Existing read probes remain valid. |
| Write confirmation behavior | `PASS_WITH_LIMITATIONS` | Local tracking stays read-only and confirmation-gated; no approved external write was executed. |
| Greenfield and brownfield local pilots | `PASS` | Both local pilot tests pass. |
| Full cross-surface pilots at current SHA | `BLOCKED` | Must be replayed against the repaired package and current published SHA. |
| Current-SHA independent Luna review | `UNPROVEN` | Requested after this handoff is committed. |
| Current-SHA fresh ChatGPT Review | `UNPROVEN` | Requires current package upload and published SHA. |
| Rollback documentation | `PASS_WITH_LIMITATIONS` | Existing rollback remains scoped; remediation commit rollback has not been destructively exercised. |
| Mobile/iPhone | **USER CHECK** | Personal device verification remains required. |

## Remaining approval-bound actions

- Push the remediation branch.
- Reinstall the repaired package in Codex and prove it from a fresh session.
- Upload the repaired `dist/chatgpt/studio.zip` and prove it from a fresh chat.
- Replay both full cross-surface pilots and obtain fresh ChatGPT Review at the
  published current SHA.
- Reconcile changed Drive source revisions.
- Execute any reversible GitHub or Drive write only after displaying the exact
  mutation and receiving explicit approval.
- Merge or release only after owner approval and no blocking finding.

No issue, milestone, PR, Drive document, permission, merge, or release was
created or changed by the remediation run.
