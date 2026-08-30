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

### Human gates currently open

1. Confirm the visible ChatGPT account `chris folorunso` / Pro is the intended account/workspace before any ChatGPT install, upload, OAuth, permission, or settings action.
2. Approve any external GitHub push or reversible external write smoke test if needed for real-host marketplace/pilot evidence.
3. Approve any ChatGPT custom-instruction diff if routing proves it is necessary.
4. Owner retains merge/release decision.

No credentials or secrets were requested, entered, or recorded.

## Post-preflight setup and acceptance

- Current V2 layout: catalog/studio.yaml; generated/codex/plugins for the
  umbrella and satellites; dist/codex/satellites and dist/chatgpt/studio.zip;
  schemas/v2; skills/studio; templates/studio-v2; brand/icon-system;
  .agents/plugins/marketplace.json; the preserved server; and
  evals/studio plus evals/pilots.
- Current source checkpoint: 55d4ab31c10d5ac22f0f3232bccd7d261fdea9b1 on
  studio-v2-bootstrap.
- Codex install: PASS_WITH_LIMITATIONS. studio-delivery@studio-v2 version 2.0.0
  is installed and enabled from the local studio-v2 marketplace; the seven
  legacy packages remain installed.
- Codex fresh-session routing: PASS_WITH_LIMITATIONS. An isolated fresh
  read-only session read the Studio state and the required next action. A
  separate fresh trivial task was not routed through Studio.
- Brownfield review loop: PASS_WITH_LIMITATIONS. REV-001 found the seeded
  formatter defect, REPAIR-FINDING-001 repaired it, REV-002 accepted the
  repaired durable checkpoint, and REV-003 independently accepted the current
  checkpoint.
- Current pilot project state, snapshots, work packages, evidence, and
  handoffs match the current source checkpoint.
- GitHub and Drive read probes: PASS. No external write was performed.
- ChatGPT installation and fresh-chat review: BLOCKED pending confirmation of
  the visible account chris folorunso / Pro with no visible workspace label.
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
| Deterministic build | PASS | two full rebuild output digests matched |
| Package validation | PASS | repository validator and Plugin Creator validator passed all 9 packages |
| ChatGPT artifact | PASS | `dist/chatgpt/studio.zip`, skills-first, no `.mcp.json`/`.app.json`/MCP declaration |
| Icon gate | PASS | Opal Seed contact sheet plus actual 24px/32px files visually inspected; transparent corners preserved |
| Seeded gates | PASS | routing, evidence vocabulary, self-accept trap, rollback, and permission fixtures |
| Greenfield pilot | PASS | local requirement/test slice passes |
| Brownfield planted defect | PASS | expected failure reproduced; bounded repair and current-SHA independent review complete |

The current worktree is intentionally dirty with the implementation outputs;
the branch is separate from `master`. No GitHub, Drive, ChatGPT, or Codex
global state has been written by the implementation checkpoint.

## Post-confirmation ChatGPT and fresh review evidence

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
- Fresh independent ChatGPT Review: BLOCKED at
  `https://chatgpt.com/c/6a946f5f-7ea4-83ed-bd4f-8c9de69440ee`. The reviewer
  independently verified the uploaded umbrella archive hash, package version,
  no-MCP packaging, confirmation-gated policy, and Drive reads, but GitHub
  could not find current SHA `55d4ab31c10d5ac22f0f3232bccd7d261fdea9b1` or
  branch `studio-v2-bootstrap`. The local source tree and current SHA therefore
  cannot be independently reconstructed from the canonical remote.
- Closing this blocker requires an explicitly approved external GitHub push or
  PR, or an equivalent user-approved transfer of the current source checkpoint.
  No push, PR, issue, milestone, Drive write, permission change, or custom
  instruction change was performed.

## Fix pass: ChatGPT metadata, routing, and write-gate evidence

- The generator now emits `Studio v2.0.0` in the package manifest description,
  Skill frontmatter, README, and ChatGPT `openai.yaml`; the validator enforces
  the manifest and archive labels. Two full rebuilds produced the identical
  archive digest `7645DB0D9A99109BF37FA72A98E042C57B41448F2FB53E4EF693761EAD9FFF76`.
- The corrected archive replaced the existing personal Skill in the confirmed
  `chris folorunso / Pro` account. The live Skills page and detail view visibly
  show `Studio v2.0.0`.
- Explicit `@Studio` routing is now proven by the fresh chat at
  https://chatgpt.com/c/6a94741f-cedc-83eb-a82c-240a2a5acd42, which returned
  `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery`.
- The safe write-gate probe at
  https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 performed only a
  GitHub identity read, displayed the exact proposed issue mutation, stopped
  for explicit approval, and created no issue. Actual external write execution
  remains `NOT_RUN` because it requires a separate owner approval.
- Read-only Chrome diagnostics found the extension installed in the Default
  profile but disabled (`disableReasons: [1]`). No browser state was changed;
  the in-app browser remains the active supported route. iPhone/mobile remains
  `USER CHECK`.
- The fresh independent ChatGPT Review remains `BLOCKED` only because the
  source checkpoint and branch are not present on the canonical GitHub remote.
  Closing that finding requires explicit approval to push or open a PR.
