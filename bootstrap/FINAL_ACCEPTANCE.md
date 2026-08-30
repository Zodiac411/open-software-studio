# Studio V2 final acceptance

Overall result: BLOCKED

Implementation source checkpoint: 4afaa3d17be234187fe77aece05a9e2024cac556

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
| Greenfield local pilot | PASS_WITH_LIMITATIONS | PILOT_A_RECEIPT.md; current SNAP-011 and EVID-PILOT-A-009 |
| Brownfield defect found and repaired | PASS | INDEPENDENT_REVIEW_001.md, REV-001, bounded repair, REV-002, REV-003, and current EVID-PILOT-B-009 |
| Cross-surface ChatGPT -> Codex -> fresh ChatGPT Review pilots | NOT_RUN | Local ChatGPT and Codex legs pass; a new fresh ChatGPT Review is pending, and canonical Drive remains pre-V2 |
| Current-SHA independent review | BLOCKED | INDEPENDENT_CHATGPT_REVIEW_005.md found host-dependent archive ordering at the prior checkpoint; repair is now at 4afaa3d and a new fresh review is pending |
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
`4afaa3d17be234187fe77aece05a9e2024cac556`, and a fresh clone from it passes the
reproducibility gate. The fresh isolated local review accepted that published
source and the evidence-only refresh. Fresh ChatGPT Review 005 then found a
host-dependent archive-order defect; the minimal repair is now published at
`4afaa3d`, and a new fresh ChatGPT Review is required. Canonical Drive still
records the pre-V2 authoritative state and may only be updated after a
separate explicit owner approval. Actual external write execution, branch
protection, and mobile verification remain open by policy.

The authorized branch publication occurred; no issue, milestone, PR, Drive
write, permission change, merge, or release was performed.
