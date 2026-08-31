# Codex Studio V2 installation receipt

Result: PASS_WITH_LIMITATIONS

Recorded: 2026-08-31

## Current installation

- Host: Windows 11 Pro 10.0.26200, PowerShell 7.6.4 Core.
- Codex: `codex-cli 0.144.5`.
- Implementation source checkpoint: `da5038327ce517b9bea4c4b6ee18c112ad82ce14` on
  `studio-v2-bootstrap`.
- Current published branch tip: `9b1ce2b8db3625f75127489c4e51c0644e156b1d`
  (evidence-only receipt refresh on top of the implementation checkpoint).
- Current CLI syntax was read before use: `codex plugin marketplace add
  <SOURCE> [--ref REF] [--sparse PATH]`, `codex plugin list`, and
  `codex plugin add <PLUGIN[@MARKETPLACE]> [--json]`.
- Marketplace: local `studio-v2` source is registered.
- Installed package: `studio-delivery@studio-v2`, version `2.0.0`, enabled.
- Installed path: `C:/Users/badcr/.codex/plugins/cache/studio-v2/studio-delivery/2.0.0`.
- The generated source tree and installed cache tree match exactly: 77 files,
  with no missing, extra, or different files. Both `plugin.json` files have
  SHA-256 `9065E5D74183354D225774C5A37AFA3FBBD3BD0A86ED1688FA1A4DAC8F2CE906`.
- The seven legacy Open Software Studio packages remain installed and enabled
  until parity is proven.

## Global Codex configuration

- `.studio/config.yaml` exists with `standard`, `auto`, `fresh_context`,
  `auto_merge: false`, `ask_before_writes`, `open_source_only: true`, and
  `prefer_free: true`.
- `C:/Users/badcr/.codex/AGENTS.md` contains exactly one marker-delimited
  Studio block:

  ```text
  <!-- STUDIO V2 BEGIN -->
  For bounded software-delivery work, use the installed Studio plugin from the
  canonical Open Software Studio catalog. Read the project's `.project/` state,
  requirements, current SHA, allowed paths, and evidence before acting. Keep
  writes confirmation-gated, use fresh-context independent review, do not let an
  executor accept its own work, and do not auto-merge. Treat external app,
  account, mobile, and publication results as unproven until directly observed.
  <!-- STUDIO V2 END -->
  ```

- Backup made before that change: `C:/Users/badcr/.codex/backups/studio-v2/AGENTS.md.before-studio-v2-20260831-182256`.
- Backup SHA-256: `CD9E3F64E967E6EA697DF6678244FC17E3C2D54DFA74D65E20F8B6953BEDDF34`.
- Post-change file SHA-256: `65BB1B04B65712D200CD8694D6854408E8607495D72D6C8A090D561987FBB164`.
- No token, cookie, password, MFA code, recovery code, OAuth token, or API
  key was stored.

## Fresh-session verification

- Fresh package session: PASS. A new read-only Codex process loaded the Studio
  package and proved branch `studio-v2-bootstrap` at the current published tip.
  Its isolated child PATH did not expose Bun, so the optional runtime probe was
  not run in that process.
- Direct current-shell MCP smoke: PASS. `bun run mcp:check` passed twice.
- Fresh `.project/` resume: PASS. A disposable project resumed with project ID
  `PRJ-RESUME-001`, phase `INTAKE`, no active work package, and the next action
  “Shape the request and record non-goals before implementation”.
- Fresh unrelated task: PASS. A separate read-only process answered `2+2=4`
  without inspecting the repository or invoking Studio.
- Explicit Studio runtime route: UNPROVEN. The installed package and source
  cache are verified, but the isolated child could not execute the optional Bun
  probe. This is not treated as live routing proof.
- Pre-existing unrelated loader, models-cache, and optional local MCP endpoint
  warnings were not changed.

## Rollback

Remove only `studio-delivery@studio-v2` using the currently installed CLI after
re-reading `codex plugin --help`, remove the one marker block if desired, and
restore the verified AGENTS backup only after confirming its exact path. The
legacy packages are outside this rollback. See `bootstrap/ROLLBACK.md`.
