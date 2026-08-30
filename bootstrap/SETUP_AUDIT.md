# Studio V2 setup audit

## Read-only preflight

Recorded: 2026-08-30T16:29:15.8053770Z

### Scope and non-goals

- Goal: implement and qualify Studio V2 from one canonical catalog, then install and verify it where the current host and account surfaces permit.
- Non-goals: changing unrelated user work, resetting or cleaning any checkout, removing legacy plugins, changing ChatGPT custom instructions without an approved diff, enabling global Full Access, creating unapproved external test artifacts, merging, or releasing.
- Protected assets: the existing global Codex instructions and configuration, the existing seven Open Software Studio plugin installations, pre-existing GitHub/Drive connections, and all unrelated worktrees.

### Host evidence

| Check | Result | Observation |
|---|---|---|
| Operating system | PASS | Windows 11 Pro 10.0.26200, 64-bit |
| Shell | PASS | PowerShell 7.6.4 Core |
| Git | PASS | 2.53.0.windows.1 |
| Python | PASS | 3.14.3 |
| Node | PASS | v24.14.0 |
| Bun | PASS | 1.4.0 |
| Codex | PASS | codex-cli 0.144.5 |
| Browser use | PASS | Codex in-app browser backend available |
| Chrome extension | UNPROVEN | No connected extension session was discovered; fallback browser is available |

### Repository evidence

- No canonical clone existed in the current task directory or the searched Codex project roots.
- Remote read probe: `master` at `d697efc16d86835ff3941f54b05e560b91a4a125`.
- Clean bare source: `open-software-studio.git`.
- Clean implementation worktree: `studio-v2-bootstrap` on branch `studio-v2-bootstrap`.
- Worktree HEAD equals the remote default HEAD and is clean at baseline.
- The repository baseline contains seven plugin directories, 36 specialist Skills, shared Markdown contracts, a seven-entry marketplace, a small MCP server, and Python validation/evaluation/package scripts.

### Baseline commands

```text
python scripts/validate_suite.py
PASS: validated 7 manifests and 36 skills

python scripts/run_evals.py
PASS: 36 routing specialists x 3 cases; 10 execution scenarios; cross-plugin demo chain
```

### Existing Codex evidence

- `codex plugin --help`, `codex plugin marketplace --help`, `codex plugin list --help`, and `codex plugin add --help` were read from the installed CLI.
- Existing installed and enabled Open Software Studio packages: `project-architect`, `interface-studio`, `engineering-guard`, `research-engineer`, `project-docs`, `web-app-builder`, and `execution-guard`, all at `0.1.0` from the existing `open-software-studio` marketplace snapshot.
- Existing global instructions: `C:/Users/badcr/.codex/AGENTS.md`; preserved except for the single marker-delimited Studio block recorded in the Codex installation receipt.
- Existing Studio config: NOT_FOUND before implementation.
- Existing global config observations: `approval_policy = never`, `sandbox_mode = danger-full-access`, `model = gpt-5.6-luna`, and max reasoning. These are baseline facts, not changes made by this setup.

### Connection evidence

- GitHub profile read: account label `Zodiac411`; target repository metadata and README read successfully.
- Google Drive profile read: `HellStar / badcrayfish11@gmail.com`; canonical folder list and governing Studio documents read successfully.
- The four supplied governing documents were read from the attachments. The canonical Drive copies were also read: SD-DOC-043, SD-DOC-036, SD-DOC-044, SD-DOC-045, plus the relevant SD-DOC-013, SD-DOC-024, SD-DOC-025, SD-DOC-030, and SD-DOC-035 records.
- ChatGPT browser surface: the in-app browser opened `https://chatgpt.com/` and visibly showed `chris folorunso` / `Pro`; no workspace label was visible. Account intent is not inferred. Browser-side mutation is blocked until the owner confirms this is the intended account/workspace.

### Current repository layout

```text
.agents/plugins/marketplace.json
plugins/{project-architect,interface-studio,engineering-guard,research-engineer,project-docs,web-app-builder,execution-guard}/
shared/{artifact-contracts,handoff-contracts,schemas,templates,quality-rules,terminology}/
scripts/{validate_suite.py,run_evals.py,package_chatgpt_plugins.py,package_chatgpt_skills.py,wire_chatgpt_apps.py}
server/{index.ts,smoke.ts}
evals/{routing,execution,cross-plugin,artifacts}
docs/{artifact-system,architecture,install-codex,install-chatgpt,chatgpt-mobile,EXTENSION-RADAR,plugin-coordination}
```

### Drift and implementation decision

The approved V2 documents describe a canonical Studio family, V2 schemas, file-backed state, generated templates/packages, and a no-MCP default ChatGPT artifact. The repository baseline predates those features and has hand-maintained seven-plugin manifests plus MCP/app companion files. The bounded implementation will preserve those legacy source packages and IDs, add a catalog-driven generated Studio family, keep compatibility entries, and leave the existing MCP server out of the default ChatGPT archive.

### Human gates and approvals

1. Account confirmation: PASS. The user confirmed the visible ChatGPT account
   `chris folorunso` / Pro as the intended account/workspace.
2. Branch publication: PASS. The user approved publication of
   `studio-v2-bootstrap`; the repaired implementation checkpoint is published.
3. External write smoke test, Drive authoritative update, and GitHub issue or
   milestone reconciliation remain separately approval-gated and NOT_RUN.
4. No ChatGPT custom-instruction diff was needed; the owner retains the
   merge/release decision.

No credentials or secrets were requested, entered, or recorded.

## Post-preflight setup and acceptance

- Current V2 layout: catalog/studio.yaml; generated/codex/plugins for the
  umbrella and satellites; dist/codex/satellites and dist/chatgpt/studio.zip;
  schemas/v2; skills/studio; templates/studio-v2; brand/icon-system;
  .agents/plugins/marketplace.json; the preserved server; and
  evals/studio plus evals/pilots.
- Current implementation source checkpoint: 468e231b55558052906aafc267e135608ddb94ff on
  studio-v2-bootstrap.
- The branch is published at this checkpoint. Later bootstrap commits are
  evidence-only refreshes generated from this immutable source checkpoint.
- Codex install: PASS_WITH_LIMITATIONS. studio-delivery@studio-v2 version 2.0.0
  is installed and enabled from the local studio-v2 marketplace; the seven
  legacy packages remain installed.
- Codex fresh-session routing: PASS_WITH_LIMITATIONS. An isolated fresh
  read-only session read the Studio state and the required next action. A
  separate fresh trivial task was not routed through Studio.
- Brownfield review loop: PASS_WITH_LIMITATIONS. REV-001 found the seeded
  formatter defect, REPAIR-FINDING-001 repaired it, and the current source
  checkpoint adds a committed-HEAD reproducibility gate, canonical source
  manifest validation, and fail-closed close transition. Current pilot
  evidence is regenerated at `468e231`; Review 009 found stale machine-readable
  review state, `REPAIR-REV-009-001` repaired it, and fresh Review 010 accepted
  the repaired state with no local defect.
- Current pilot project state, snapshots, work packages, evidence, and
  handoffs match the current source checkpoint; fresh local REV-006 receipts
  validate and the guarded close command has moved both pilot states to CLOSED.
- GitHub and Drive read probes: PASS. No external write was performed.
- ChatGPT installation and fresh-chat verification: PASS_WITH_LIMITATIONS.
  The confirmed chris folorunso / Pro account has the accepted Studio v2.0.0
  Skill installed and explicit @Studio routing passes; a fresh independent
  Review 010 accepted the source, archive repair, and evidence state with no
  local defect; the remaining limitations are external or user-gated.
- Pilot session close: PASS_WITH_LIMITATIONS for both local pilot projects;
  release and merge remain owner-gated.
- iPhone/mobile availability: USER CHECK.

## Local implementation checkpoint

The initial implementation checkpoint contained a catalog-driven Studio V2
package family. That checkpoint was superseded by the repair and current-SHA
independent reviews recorded below.

| Gate | Result | Evidence |
|---|---|---|
| Canonical catalog and provenance | PASS | `catalog/studio.yaml`, pinned source register, no copied third-party files |
| Generated family | PASS | 9 generated packages, public names Studio through Studio Track, legacy source packages preserved |
| V2 artifacts and state | PASS | 22 catalog templates, `schemas/v2`, `scripts/studio.py`, `.project` recovery commands |
| Deterministic build | PASS | two committed-HEAD rebuilds and a separate clean clone reproduced canonical text and binary content |
| Package validation | PASS | repository validator and Plugin Creator validator passed all 9 packages |
| ChatGPT artifact | PASS | `dist/chatgpt/studio.zip`, skills-first, no `.mcp.json`/`.app.json`/MCP declaration |
| Icon gate | PASS | Opal Seed contact sheet plus actual 24px/32px files visually inspected; transparent corners preserved |
| Seeded gates | PASS | routing, evidence vocabulary, self-accept trap, rollback, and permission fixtures |
| Greenfield pilot | PASS | local requirement/test slice passes |
| Brownfield planted defect | PASS | expected failure reproduced; bounded repair and current-SHA independent review complete |

The current evidence refresh may leave this worktree dirty while it is being
committed; the implementation branch is separate from `master`. The source
checkpoint changed repository code only in the bounded reproducibility,
close-gate, and archive-byte repairs. No Drive, issue, milestone, PR, merge, or permission write
was performed.

## Historical pre-publication ChatGPT and fresh review evidence

- The user confirmed that the visible `chris folorunso` / `Pro` account, with
  no visible workspace label, is the intended ChatGPT destination.
- The live route used was `Plugins -> Skills -> Create -> Upload from your
  computer`. `dist/chatgpt/studio.zip` was accepted and Studio is visibly
  listed under both Installed and Created by me.
- The installed detail view visibly contains the Studio metadata, SKILL.md,
  Opal Seed assets, and generated skill directories. `Try in chat` visibly
  added the Studio routing badge to a fresh chat.
- Fresh ChatGPT verification: PASS. The chat at
  `https://chatgpt.com/c/6a946dee-ef10-83ed-9c1b-3e86b9b6cc15` used the
  Studio context-grounding route, visibly used GitHub and Google Drive, read
  both canonical locations read-only, and produced the requested V2 brief.
- Fresh independent ChatGPT Review 003: BLOCKED at
  `https://chatgpt.com/c/6a947ba5-7af0-83eb-8549-2d5c1cde6d5b`. The reviewer
  independently verified the focused current receipts, pilot state, review
  records, package-source metadata, and deterministic umbrella archive, then
  confirmed that the expected GitHub SHA/branch is absent remotely and that
  Drive remains on its pre-V2 authoritative state. Its typed findings are
  recorded in `bootstrap/INDEPENDENT_CHATGPT_REVIEW_003.md`.
- This historical blocker was closed for source publication by the authorized
  branch push. No issue, milestone, PR, Drive write, permission change, or
  custom instruction change was performed in that earlier pass.

## Fix pass: ChatGPT metadata, routing, and write-gate evidence

- The generator now emits `Studio v2.0.0` in the package manifest description,
  Skill frontmatter, README, and ChatGPT `openai.yaml`; the validator enforces
  the manifest and archive labels. Two full rebuilds produced the identical
  archive digest `96E79FD0EDF0C01164336AE6AF1532A0C4E851CBAA5AC477C57C7C10DFB030FA`.
- The corrected archive replaced the existing personal Skill in the confirmed
  `chris folorunso / Pro` account. The live Skills page and detail view visibly
  show `Studio v2.0.0`.
- Explicit `@Studio` routing is now proven by the fresh chat at
  https://chatgpt.com/c/6a94741f-cedc-83eb-a82c-240a2a5acd42, which returned
  `STUDIO_ROUTE_V2_OK studio-chatgpt-studio-delivery`.
- The safe write-gate probe at
  https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 performed only a
  GitHub identity read, displayed the exact proposed issue mutation, stopped
  for explicit approval, and created no issue. Actual external write execution
  remains `NOT_RUN` because it requires a separate owner approval.
- Read-only Chrome diagnostics found the extension installed in the Default
  profile but disabled (`disableReasons: [1]`). No browser state was changed;
  the in-app browser remains the active supported route. iPhone/mobile remains
  `USER CHECK`.
- Historical ChatGPT Review 003 and 004 were blocked by a missing or stale
  remote checkpoint; that source-publication finding is repaired. The current
  published checkpoint is `4afaa3d17be234187fe77aece05a9e2024cac556`, and a
  fresh review against it is still required. Canonical Drive remains on its
  pre-V2 authoritative state and needs separate owner approval before update.

## Repair pass: committed-HEAD reproducibility and lifecycle enforcement

- Implementation checkpoint: `4afaa3d17be234187fe77aece05a9e2024cac556`.
- `scripts/check_reproducibility.py` now materializes `HEAD` with `git archive`
  before building, so untracked worktree files cannot affect the proof.
- `scripts/studio.py close` now requires a current independent `ACCEPT` review
  and checks the declared `IN_REVIEW -> ACCEPTED -> CLOSED` transitions. The
  negative gate was directly exercised and returned `BLOCKED` before a current
  review existed.
- Both pilots were refreshed to `SNAP-011`, `EVID-PILOT-*-009`, and
  `HANDOFF-4AFAA3D17BE2`; their assertions, doctor/status, and evidence checks
  pass.
- Historical local acceptance records `REV-005` and `INDEPENDENT_REVIEW_006`
  cover the prior source checkpoint. The archive-order repair at `4afaa3d`
  passes the repository validators and committed-HEAD reproducibility gate; a
  fresh ChatGPT Review is pending against the new source checkpoint and its
  evidence-only branch tip.

## Current repair review

- Fresh ChatGPT Review 005 at
  `https://chatgpt.com/c/6a949225-51d0-83eb-9e92-c10b1107c2f7` returned
  `BLOCKED` because the clean Linux rebuild exposed host-dependent archive
  ordering at the prior source checkpoint. Its typed findings and repair
  record are preserved in `INDEPENDENT_CHATGPT_REVIEW_005.md`.
- The minimal archive sort repair is committed at
  `4afaa3d17be234187fe77aece05a9e2024cac556`. Local validation, evaluation,
  both pilots, and source-manifest checks pass at that checkpoint. A new fresh
  ChatGPT Review is required before acceptance can close.

## Current archive-byte repair

- Fresh Review 006 is preserved in `INDEPENDENT_CHATGPT_REVIEW_006.md` and
  remains BLOCKED for the prior checkpoint because Linux rebuilt different
  compressed archive bytes and the generated outputs were not committed.
- The bounded repair changes `scripts/build_studio.py` to use stored ZIP
  entries, regenerates every ChatGPT archive and dependent hash manifest, and
  is published at `8f8e9fc2164a1ceeb503aecb36edbf8dc8c48dd6`.
- `python scripts/check_reproducibility.py` and `python scripts/validate_suite.py`
  pass from the repaired source. Both pilots now use `SNAP-012`,
  `EVID-PILOT-*-010`, and `HANDOFF-8F8E9FC2164A`.
- Review 007 is the next required fresh ChatGPT review. It must inspect the
  current branch tip, source checkpoint, active receipts, package hashes,
  pilot evidence, Codex installation, ChatGPT installation, connector reads,
  permissions, and rollback evidence before reading any conclusion.

## Current archive tie-breaker repair

- Review 007 returned PASS_WITH_LIMITATIONS for source `8f8e9fc` and identified
  `REV-007-014`, a low portability risk for case-fold collisions.
- `REPAIR-ARCHIVE-TIEBREAK` adds an explicit UTF-8 byte tie-breaker to
  `archive_sort_key`. The current catalog has no collision, so the published
  archive and manifest hashes remain unchanged.
- The repair is published at `17e9407569eb642e11d86def752c22ae6`; the local
  collision probe, `check_reproducibility.py`, `validate_suite.py`, both pilot
  evidence validators, and both doctor checks pass.
- Review 008 is required against this new source checkpoint and its current
  evidence-only branch tip.

## Current complete-archive-order repair

- Fresh Review 008 is preserved in `INDEPENDENT_CHATGPT_REVIEW_008.md` and
  returned `PASS_WITH_LIMITATIONS` for source `17e9407`. It identified
  `REV-008-011`: synthesized ChatGPT entries were appended after the sorted
  source entries, and the validator did not assert ordering across the complete
  archive entry list.
- `REPAIR-ARCHIVE-ORDER` now places source and synthesized entries in one
  POSIX/case-folded/UTF-8-byte sorted list, and `validate_studio.py` asserts the
  complete ZIP order. The repair and regenerated artifacts are published at
  `468e231b55558052906aafc267e135608ddb94ff`; the current `studio.zip` digest
  is `08A62A947120249783B51C91B115962DD6644DCF5207D279AC4F74074A95DAD8`.
- Local archive-order probing, `validate_studio.py`, `run_evals.py`,
  `check_reproducibility.py`, `validate_suite.py`, both pilot evidence
  validators, both repair validators, and both doctor checks pass from the
  repaired source.
- The regenerated archive was accepted by the confirmed ChatGPT Skills
  installation, whose detail view visibly shows `Studio v2.0.0`. Review 009
  verified source `468e231` and the current evidence-only branch tip but found
  stale `SETUP_STATE.json` review text. `REPAIR-REV-009-001` records the fix;
  fresh Review 010 at source `468e231` and remote tip `320ec6d` returned
  `PASS_WITH_LIMITATIONS` with no local defect.
