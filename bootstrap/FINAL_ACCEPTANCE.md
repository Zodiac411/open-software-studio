# Studio V2 final acceptance

Overall result: BLOCKED

Implementation source checkpoint: 468e231b55558052906aafc267e135608ddb94ff

Branch: studio-v2-bootstrap

The implementation checkpoint is immutable. The branch may contain later
evidence-only commits generated from this checkpoint; those commits must not
be treated as a new implementation revision.

## Acceptance matrix

| Requirement | Result | Evidence |
|---|---|---|
| One canonical catalog | PASS | catalog/studio.yaml and generated manifests |
| Deterministic umbrella and satellites | PASS | build digest comparison, clean-checkout reproducibility gate, and validate_studio.py |
| Codex install and fresh-session proof | PASS_WITH_LIMITATIONS | CODEX_INSTALL_RECEIPT.md |
| ChatGPT install and fresh-chat proof | PASS_WITH_LIMITATIONS | CHATGPT_INSTALL_RECEIPT.md; refreshed Skills upload visibly shows Studio v2.0.0, and fresh verification plus explicit @Studio routing chats pass |
| GitHub read connection | PASS | CONNECTED_APPS_RECEIPT.md |
| Google Drive read connection | PASS | CONNECTED_APPS_RECEIPT.md |
| Write confirmation gating | PASS_WITH_LIMITATIONS | seeded gates and CLI track --apply failure pass; fresh ChatGPT Track probe displayed the exact mutation and stopped for approval; actual external write remains NOT_RUN |
| Greenfield local pilot | PASS_WITH_LIMITATIONS | PILOT_A_RECEIPT.md; current SNAP-014, EVID-PILOT-A-012, and HANDOFF-468E231B5555 |
| Brownfield defect found and repaired | PASS | INDEPENDENT_REVIEW_001.md, REV-001, bounded repairs, REV-002, REV-003, and current EVID-PILOT-B-012 |
| Cross-surface ChatGPT -> Codex -> fresh ChatGPT Review pilots | NOT_RUN | Local ChatGPT and Codex legs pass; Review 008 accepted the prior source with limitations and Review 009 is pending against the complete-entry-order repair |
| Current-SHA independent review | NOT_RUN | Review 008 accepted source 17e9407 with one archive-order contract finding; complete-entry sorting and validation are published at 468e231 and a new fresh review is pending |
| Rollback dry-run | PASS | ROLLBACK.md |
| iPhone/mobile availability | USER CHECK | personal device verification not performed |

## Current blocker

The user confirmed that the browser-visible ChatGPT account chris folorunso /
Pro, with no visible workspace label, is the intended account. The personal
Skills fallback accepted `dist/chatgpt/studio.zip`; Studio routing and a
read-only GitHub/Drive verification chat passed. A fresh explicit `@Studio`
routing chat returned `STUDIO_ROUTE_V2_OK studio-chatgpt-studio-delivery`, and a
fresh Studio Track probe displayed the exact external mutation and stopped
pending approval without writing. The refreshed Skills UI now visibly shows
`Studio v2.0.0`. The previously blocked remote-source finding is repaired:
`studio-v2-bootstrap` now publishes implementation checkpoint
`468e231b55558052906aafc267e135608ddb94ff`, and a fresh clone from it passes the
reproducibility gate. Fresh ChatGPT Review 006 then found that the committed
outputs still differed on Linux because the archive repair had not been
regenerated into the commit. The bounded ZIP_STORED repair and regenerated
outputs are now published at `8f8e9fc2164a1ceeb503aecb36edbf8dc8c48dd6`; local
clean-checkout reproducibility and the full validation suite pass there. Review
007 accepted that source with one low portability note; the explicit UTF-8
tie-breaker is now published at `17e9407569eb642e11d86def752c22ae6b638337`.
Review 008 then found that the synthesized entries were appended outside the
sorted list and that the validator did not assert complete entry ordering. The
complete-entry repair and validator assertion are now published at
`468e231b55558052906aafc267e135608ddb94ff`; a new fresh ChatGPT Review is
required against it and the current evidence tip.
Canonical Drive still records the pre-V2 authoritative state and may only be
updated after a separate explicit owner approval. Actual external write
execution, branch protection, and mobile verification remain open by policy.

The authorized branch publication occurred; no issue, milestone, PR, Drive
write, permission change, merge, or release was performed.
