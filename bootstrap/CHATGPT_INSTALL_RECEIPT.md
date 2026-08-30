# ChatGPT Studio V2 installation receipt

Result: PASS_WITH_LIMITATIONS

Recorded: 2026-08-30

Implementation source checkpoint: `468e231b55558052906aafc267e135608ddb94ff` on
published branch `studio-v2-bootstrap`.

The archive was rebuilt after the committed-HEAD reproducibility repair and
uploaded to the confirmed Skills installation. Subsequent receipt commits
are evidence-only and do not change the implementation source checkpoint.

## Artifact readiness

- Build artifact: dist/chatgpt/studio.zip.
- Artifact version: 2.0.0.
- SHA-256 at this checkpoint:
  08A62A947120249783B51C91B115962DD6644DCF5207D279AC4F74074A95DAD8.
- Size: 110,928 bytes.
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
  `STUDIO_ROUTE_V2_OK studio-chatgpt-studio-delivery` at
  https://chatgpt.com/c/6a9490be-6f08-83eb-9110-f95f56ee4226.
- Version parity: PASS. The uploaded package metadata records version 2.0.0,
  the current artifact digest above, and the Skills Installed/Created by me
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
- Historical independent Studio Reviews 003 through 009 are preserved
  verbatim. Review 006 correctly blocked the prior checkpoint after a fresh
  Linux rebuild found host-dependent archive bytes and uncommitted generated
  outputs. Review 007 accepted the repaired source with one low portability
  note, and Review 008 accepted the complete archive-order repair with one
  remaining contract finding. Review 009 then verified the source repair but
  found stale machine-readable review text in SETUP_STATE.json; that
  evidence-only defect is repaired and Review 010 is pending. The complete-entry
  ordering and validator assertion remain published at source checkpoint
  `468e231`.
- No ChatGPT custom instruction, OAuth flow, account switch, permission
  change, or external write was performed. Passwords, MFA codes, recovery
  codes, cookies, OAuth tokens, and API keys were never requested or handled.
- iPhone/mobile availability: USER CHECK.
