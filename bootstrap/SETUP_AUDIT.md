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

- Current source checkpoint: 18ddbc14a6f9b16967064f4066ff167799cb8a92 on
  studio-v2-bootstrap.
- Codex install: PASS_WITH_LIMITATIONS. studio-delivery@studio-v2 version 2.0.0
  is installed and enabled from the local studio-v2 marketplace; the seven
  legacy packages remain installed.
- Codex fresh-session routing: PASS_WITH_LIMITATIONS. An isolated fresh
  read-only session read the Studio state and the required next action. A
  separate fresh trivial task was not routed through Studio.
- Brownfield review loop: PASS_WITH_LIMITATIONS. REV-001 found the seeded
  formatter defect, REPAIR-FINDING-001 repaired it, and REV-002 independently
  accepted the repaired local checkpoint.
- Current pilot project state, snapshots, work packages, evidence, and
  handoffs match the current source checkpoint.
- GitHub and Drive read probes: PASS. No external write was performed.
- ChatGPT installation and fresh-chat review: BLOCKED pending confirmation of
  the visible account chris folorunso / Pro with no visible workspace label.
- iPhone/mobile availability: USER CHECK.

## Local implementation checkpoint

The bounded implementation branch now contains a catalog-driven Studio V2
package family. The implementation is not yet independently accepted.

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
| Brownfield planted defect | PASS_WITH_LIMITATIONS | expected test failure reproduced; independent review and repair still pending |

The current worktree is intentionally dirty with the implementation outputs;
the branch is separate from `master`. No GitHub, Drive, ChatGPT, or Codex
global state has been written by the implementation checkpoint.
