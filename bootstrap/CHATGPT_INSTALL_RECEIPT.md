# ChatGPT Studio V2 installation receipt

Result: PASS_WITH_LIMITATIONS

Recorded: 2026-08-30

Local source checkpoint: `c00f7ab98ef83108675ffcda06f2f04f81c7977e` on
`studio-v2-bootstrap`.

## Artifact readiness

- Build artifact: dist/chatgpt/studio.zip.
- Artifact version: 2.0.0.
- SHA-256 at this checkpoint:
  7645DB0D9A99109BF37FA72A98E042C57B41448F2FB53E4EF693761EAD9FFF76.
- Size: 78,536 bytes.
- Repository validator: PASS.
- Plugin Creator validator: PASS.
- The archive is skills-first. It declares no MCP server, .mcp.json, app
  manifest, localhost dependency, tunnel, API key, or server reference.
- Opal Seed assets are packaged in the archive and remain mobile-safe raster
  assets; mobile availability itself remains USER CHECK.
- The package now exposes the user-visible label `Studio v2.0.0` in its
  manifest, Skill description, and `openai.yaml`; the repository validator
  rejects a generated package that loses that label.

## Account and route gate

- Browser surface available: Codex in-app browser (iab).
- Chrome extension: BLOCKED for this run. Read-only diagnostics found the
  extension installed in Chrome Default but disabled (`disableReasons: [1]`),
  so the setup used the supported Codex in-app browser and did not override
  browser state.
- Visible ChatGPT account: chris folorunso / Pro.
- Visible workspace label: none.
- Account/workspace confirmation: PASS. The user confirmed this is the
  intended destination.
- Route used: Plugins -> Skills -> Create -> Upload from your computer.
  The personal Skills route was selected after the live UI exposed it; no
  marketplace import or repository push was required.
- Upload and scan: PASS. The exact dist/chatgpt/studio.zip archive was uploaded
  and the UI accepted it.
- Installed-surface proof: PASS. The Skills page visibly lists Studio under
  Installed and Created by me. The detail view identifies
  studio-chatgpt-studio-delivery, shows the bundled SKILL.md, plugin metadata,
  Opal Seed assets, and the generated skill directories.
- Invocation proof: PASS. Try in chat visibly added the Studio routing badge
  to a fresh chat, and a separate fresh chat accepted `@Studio` and returned
  `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery` at
  https://chatgpt.com/c/6a94741f-cedc-83eb-a82c-240a2a5acd42.
- Version parity: PASS. The uploaded package metadata records version 2.0.0,
  the matching artifact digest above, and the Skills Installed/Created by me
  entries plus detail view visibly show `Studio v2.0.0`.
- Fresh-chat verification: PASS. The completed read-only verification chat is
  https://chatgpt.com/c/6a946dee-ef10-83ed-9c1b-3e86b9b6cc15.
- The chat visibly used GitHub and Google Drive, identified both canonical
  locations, and produced the requested V2 brief without writes.
- Write-confirmation probe: PASS_WITH_LIMITATIONS. A fresh Studio Track chat
  at https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 performed a
  read-only GitHub identity check, displayed the exact proposed issue
  mutation, explicitly stated that no issue was created, and stopped pending
  approval. Actual external issue creation remains NOT_RUN because it is
  irreversible repository history and requires a separate explicit approval.
- Fresh independent Studio Review: BLOCKED at
  https://chatgpt.com/c/6a947ba5-7af0-83eb-8549-2d5c1cde6d5b; the full typed
  result is recorded in `bootstrap/INDEPENDENT_CHATGPT_REVIEW_003.md`. It
  independently confirmed the canonical GitHub branch and SHA are absent and
  also recorded that canonical Drive state still describes the pre-V2 baseline.
  Local package and pilot evidence remained internally coherent.
- No ChatGPT custom instruction, OAuth flow, account switch, permission
  change, or external write was performed. Passwords, MFA codes, recovery
  codes, cookies, OAuth tokens, and API keys were never requested or handled.
- iPhone/mobile availability: USER CHECK.
