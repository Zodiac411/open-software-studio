# Studio V2 final acceptance

Overall result: BLOCKED

Implementation source checkpoint: dee9454070ba15ecf1c87f110b3db6cef1c59820

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
| Greenfield local pilot | PASS | PILOT_A_RECEIPT.md |
| Brownfield defect found and repaired | PASS | INDEPENDENT_REVIEW_001.md, REV-001, bounded repair, REV-002, REV-003, current local REV-004 and INDEPENDENT_REVIEW_005 |
| Cross-surface ChatGPT -> Codex -> fresh ChatGPT Review pilots | BLOCKED | Source is now published; a new fresh ChatGPT Review is still pending, and canonical Drive remains pre-V2 |
| Current-SHA independent review | NOT_RUN | New local review and fresh ChatGPT Review are pending at the repaired checkpoint; historical blocked reviews remain in INDEPENDENT_CHATGPT_REVIEW_003.md and INDEPENDENT_CHATGPT_REVIEW_004.md |
| Rollback dry-run | PASS | ROLLBACK.md |
| iPhone/mobile availability | USER CHECK | personal device verification not performed |

## Current blocker

The user confirmed that the browser-visible ChatGPT account chris folorunso /
Pro, with no visible workspace label, is the intended account. The personal
Skills fallback accepted `dist/chatgpt/studio.zip`; Studio routing and a
read-only GitHub/Drive verification chat passed. A fresh explicit `@Studio`
routing chat returned `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery`, and a
fresh Studio Track probe displayed the exact external mutation and stopped
pending approval without writing. The refreshed Skills UI now visibly shows
`Studio v2.0.0`. The previously blocked remote-source finding is repaired:
`studio-v2-bootstrap` now publishes implementation checkpoint
`dee9454070ba15ecf1c87f110b3db6cef1c59820`, and a fresh clone from it passes the
reproducibility gate. A new fresh ChatGPT Review is still required to inspect
that published source and the evidence-only refresh. Canonical Drive still
records the pre-V2 authoritative state and may only be updated after a
separate explicit owner approval. Actual external write execution, branch
protection, and mobile verification remain open by policy.

The authorized branch publication occurred; no issue, milestone, PR, Drive
write, permission change, merge, or release was performed.
