# Studio V2 final acceptance

Overall result: BLOCKED

Reviewed source checkpoint: c00f7ab98ef83108675ffcda06f2f04f81c7977e

Branch: studio-v2-bootstrap

## Acceptance matrix

| Requirement | Result | Evidence |
|---|---|---|
| One canonical catalog | PASS | catalog/studio.yaml and generated manifests |
| Deterministic umbrella and satellites | PASS | build digest comparison and validate_studio.py |
| Codex install and fresh-session proof | PASS_WITH_LIMITATIONS | CODEX_INSTALL_RECEIPT.md |
| ChatGPT install and fresh-chat proof | PASS_WITH_LIMITATIONS | CHATGPT_INSTALL_RECEIPT.md; refreshed Skills upload visibly shows Studio v2.0.0, and fresh verification plus explicit @Studio routing chats pass |
| GitHub read connection | PASS | CONNECTED_APPS_RECEIPT.md |
| Google Drive read connection | PASS | CONNECTED_APPS_RECEIPT.md |
| Write confirmation gating | PASS_WITH_LIMITATIONS | seeded gates and CLI track --apply failure pass; fresh ChatGPT Track probe displayed the exact mutation and stopped for approval; actual external write remains NOT_RUN |
| Greenfield local pilot | PASS | PILOT_A_RECEIPT.md |
| Brownfield defect found and repaired | PASS | INDEPENDENT_REVIEW_001.md, REV-001, bounded repair, REV-002, REV-003, current local REV-004 and INDEPENDENT_REVIEW_005 |
| Cross-surface ChatGPT -> Codex -> fresh ChatGPT Review pilots | BLOCKED | Fresh ChatGPT Review could not retrieve current local SHA from canonical GitHub |
| Current-SHA independent review | BLOCKED | Local REV-004 and INDEPENDENT_REVIEW_005 accept the current local checkpoint; fresh ChatGPT Review 003 is blocked on remote SHA/branch availability and Drive baseline drift, with typed findings in INDEPENDENT_CHATGPT_REVIEW_003.md |
| Rollback dry-run | PASS | ROLLBACK.md |
| iPhone/mobile availability | USER CHECK | personal device verification not performed |

## Blocking item

The user confirmed that the browser-visible ChatGPT account chris folorunso /
Pro, with no visible workspace label, is the intended account. The personal
Skills fallback accepted `dist/chatgpt/studio.zip`; Studio routing and a
read-only GitHub/Drive verification chat passed. A fresh explicit `@Studio`
routing chat returned `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery`, and a
fresh Studio Track probe displayed the exact external mutation and stopped
pending approval without writing. The refreshed Skills UI now visibly shows
`Studio v2.0.0`. Fresh independent review 003 at
https://chatgpt.com/c/6a947ba5-7af0-83eb-8549-2d5c1cde6d5b returned BLOCKED
because GitHub could not find current SHA
c00f7ab98ef83108675ffcda06f2f04f81c7977e or branch studio-v2-bootstrap, and
Drive still records the pre-V2 baseline. Its typed findings are recorded in
`bootstrap/INDEPENDENT_CHATGPT_REVIEW_003.md`. An explicitly approved GitHub
push or PR is required to close the source gate; updating Drive also requires
separate owner approval. No push or Drive write was performed. Actual external
write execution and mobile verification remain open by policy.

No merge, push, issue, milestone, Drive write, or release was performed.
