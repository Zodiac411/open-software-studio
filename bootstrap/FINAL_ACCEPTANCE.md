# Studio V2 final acceptance

Overall result: PASS_WITH_LIMITATIONS

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
| Cross-surface ChatGPT -> Codex -> fresh ChatGPT Review pilots | PASS_WITH_LIMITATIONS | Local ChatGPT and Codex legs pass; Review 010 accepted source 468e231 and the current evidence chain with only recorded external/host limitations |
| Current-SHA independent review | PASS_WITH_LIMITATIONS | Fresh Review 010 accepted source 468e231 and remote tip 320ec6d with no local source, package, validator, receipt, or state defect |
| Rollback dry-run | PASS | ROLLBACK.md |
| iPhone/mobile availability | USER CHECK | personal device verification not performed |

## Current limitations

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
`468e231b55558052906aafc267e135608ddb94ff`. Review 009 verified that source
and the exact remote evidence tip, then found stale `blocking_findings` text in
`SETUP_STATE.json`; `REPAIR-REV-009-001` records the evidence-only fix. Fresh
Review 010 independently verified the repaired state and returned
`PASS_WITH_LIMITATIONS` with no local defect.
Canonical Drive still records the pre-V2 authoritative state and may only be
updated after a separate explicit owner approval. Actual external write
execution, branch protection, historical host replay, the disabled Chrome
extension, and mobile verification remain open by policy or user check.

The authorized branch publication occurred; no issue, milestone, PR, Drive
write, permission change, merge, or release was performed.
