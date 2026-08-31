# ChatGPT Studio V2 installation receipt

Result: BLOCKED

Recorded: 2026-08-31

## Current artifact

- Implementation source checkpoint: `da5038327ce517b9bea4c4b6ee18c112ad82ce14`.
- Archive: `dist/chatgpt/studio.zip`.
- Version: `2.0.0`.
- SHA-256: `D004F894ACA624DC86DFF346D208820F0B76AE67D0B01862CCA15B84CD00E796`.
- Size: 141,805 bytes.
- Local package validation: PASS.
- The bundle is skills-first and declares no MCP server, `.mcp.json`, app
  manifest, localhost dependency, tunnel, API key, or server reference.
- Mobile-safe Opal Seed PNG assets are present and validated locally.

## Account and route

- Intended destination: `chris folorunso / Pro`.
- Account confirmation: PASS. The user confirmed the account previously
  observed during the setup flow.
- Best supported route to use when a browser is connected:
  `Plugins -> Skills -> Create -> Upload`.
- Current browser surface: BLOCKED. The Chrome extension and Codex in-app
  browser both returned unavailable, and browser enumeration returned no
  connected sessions.

## Current gates

- Current archive upload: BLOCKED. No supported browser surface was available
  to upload the current archive or inspect scanning/review results.
- Fresh ChatGPT conversation: BLOCKED. The current package has not been
  installed or invoked in a fresh chat.
- Explicit `@Studio` invocation: UNPROVEN. No current visible invocation
  surface is available.
- Current ChatGPT write-confirmation smoke: UNPROVEN. No current ChatGPT
  session was available to display a proposed mutation and stop for approval.
- Fresh independent ChatGPT Review: BLOCKED. It cannot inspect the current
  package and SHA until the current archive is installed and a fresh chat is
  available.
- Cross-surface pilots: BLOCKED for the same reason; local fixture portions
  remain recorded in the pilot receipts.
- Global ChatGPT custom-instruction change: NOT_RUN. No diff was needed or
  approved.
- iPhone/mobile availability: USER CHECK.

## Historical evidence boundary

Earlier visible ChatGPT installation and Review records are preserved in the
bootstrap directory. They refer to an older archive/source checkpoint and are
not reused as proof of the current SHA. No password, MFA code, recovery code,
cookie, OAuth token, or API key was requested or handled.
