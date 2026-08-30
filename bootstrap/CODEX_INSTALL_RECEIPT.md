# Codex Studio V2 installation receipt

Result: `PASS_WITH_LIMITATIONS`

Recorded: 2026-08-30

## Installation

- Host: Windows 11 Pro 10.0.26200, PowerShell 7.6.4.
- Codex: `codex-cli 0.144.5`.
- Source branch: `studio-v2-bootstrap`.
- Source revision at initial installation: `a9454048456c9cef9d5eca0fa8be47b3ecc4ee4c`.
- Current implementation source verification revision: `4afaa3d17be234187fe77aece05a9e2024cac556`.
- The published `studio-v2-bootstrap` branch contains this immutable source
  checkpoint; later bootstrap commits are evidence-only refreshes.
- CLI syntax was read from the installed executable before use:
  `codex plugin marketplace add <path-or-git-source>` and
  `codex plugin add <plugin>@<marketplace>`.
- Marketplace add result: local `studio-v2` marketplace added from this
  worktree.
- Install result: `studio-delivery@studio-v2`, version `2.0.0`, installed and
  enabled, with source `generated/codex/plugins/studio-delivery`.
- Live recheck at the implementation source revision: `codex plugin list -m studio-v2 --json`
  reports the package installed and enabled. The source manifest and cached
  2.0.0 manifest have identical SHA-256
  `ECFA6F197BE9A8E5DEF8FBF3D088C356E34614CBA067B76217DB4B0F880C42BA`.
- The seven pre-existing `open-software-studio` packages were preserved and
  remained installed/enabled: `project-architect`, `interface-studio`,
  `engineering-guard`, `research-engineer`, `project-docs`,
  `web-app-builder`, and `execution-guard`.
- No token, cookie, password, MFA code, recovery code, OAuth token, or API key
  was requested or stored.

## Global Studio configuration

Created the previously absent `C:/Users/badcr/.studio/config.yaml` with:

```yaml
default_profile: standard
default_archetype: auto
review_mode: fresh_context
auto_merge: false
permission_posture: ask_before_writes
open_source_only: true
prefer_free: true
```

Before changing the global instruction file, a restorable backup was made and
verified at `C:/Users/badcr/.codex/backups/studio-v2/AGENTS.md.before-studio-v2`.
Backup SHA-256:
`C07E44A0C5A992A4E4AC389141392292B51DE1E36CA48A0463544D6731A19D3C`.

The only added global content is the single marker-delimited block:

```text
[STUDIO WORKFLOW BEGIN]
When `.project/project.yaml` exists, read Studio state before substantive work. Use one bounded active work package; inspect requirements, snapshot, current SHA, and allowed paths before changing files. Keep writes confirmation-gated, preserve unrelated work, never self-accept or auto-merge, record named evidence, and stop for fresh independent review.
[STUDIO WORKFLOW END]
```

Marker verification: exactly one begin marker and one end marker. Current
`AGENTS.md` SHA-256 is `CD9E3F64E967E6EA697DF6678244FC17E3C2D54DFA74D65E20F8B6953BEDDF34`.
All unrelated global instructions were retained.

## Fresh-session evidence

- Studio-directed fresh process: `PASS_WITH_LIMITATIONS`. A new
  `codex exec --ephemeral --ignore-user-config --sandbox read-only` session
  using `gpt-5.6-luna` read the greenfield `.project` state and reported
  `CLOSED`, `WP-001`, next action `complete a fresh independent review, then
  obtain release approval`, and the absence of a review artifact. It made no
  writes. This is direct behavioral evidence that the installed Studio
  workflow is available to a fresh Codex process.
- Unrelated fresh process: `PASS`. A separate new session asked only for
  `2+2=4` and returned `2+2=4` without inspecting files or invoking Studio.
- The default-config fresh attempt was stopped after the existing unrelated
  `doop` MCP endpoint at `http://localhost:4300/mcp` refused connections.
  The isolated retry avoided that unrelated host configuration; no host config
  was changed.
- Codex emitted pre-existing loader warnings for unrelated cached plugins and
  a stale models-cache field; the default process also reported a non-curated
  marketplace-cache warning for studio-delivery. Direct plugin listing,
  matching source/cache manifests, and the isolated fresh session still prove
  the installed 2.0.0 package, but these host warnings remain a limitation.

## Rollback

Remove only `studio-delivery@studio-v2` with the current CLI, remove the
single marker block if desired, restore the backed-up `AGENTS.md` after
confirming the target path, and remove `C:/Users/badcr/.studio/config.yaml` if
the Studio defaults are no longer wanted. Legacy packages are not part of this
rollback. See `bootstrap/ROLLBACK.md`.
