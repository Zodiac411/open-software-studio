# Studio V2 final acceptance

Overall result: BLOCKED

Recorded: 2026-08-31

Implementation source checkpoint: `da5038327ce517b9bea4c4b6ee18c112ad82ce14`
on branch `studio-v2-bootstrap`. The current branch may advance with
evidence-only receipt commits; the generated implementation and archive are
anchored to this checkpoint.

## Acceptance matrix

| Requirement | Result | Evidence and limitation |
|---|---|---|
| One canonical catalog | PASS | `catalog/studio.yaml` generates the Studio family, metadata, schemas, templates, icons, and validation inputs. |
| Deterministic umbrella and satellite builds | PASS | Canonical build, check-only build, clean-checkout reproducibility, and deterministic ChatGPT archive checks pass locally on Windows. |
| Versioned schemas, compiler, templates, and lifecycle commands | PASS | `validate_suite.py`, the CLI checks, 22 templates, and V2 schema/evaluation gates pass. |
| Studio family, compatibility aliases, and Opal Seed assets | PASS | Nine generated packages, compatibility satellites, mobile-safe icon assets, and package validators pass. |
| Recovery, evidence grading, seeded gates, and independent local review | PASS_WITH_LIMITATIONS | Local evaluations, security checks, focused regressions, seeded red/green gates, and Luna review pass; current ChatGPT review is not available. |
| Hosted GitHub validation | PASS_WITH_LIMITATIONS | Run `33419067013`: Windows validation, security, optional MCP smoke, and Windows MCP smoke pass. Ubuntu/native generated-output parity failed; Linux follow-up is intentionally not pursued. |
| Codex installation and fresh-session proof | PASS_WITH_LIMITATIONS | `studio-delivery@studio-v2` 2.0.0 is installed/enabled; source/cache match across 77 files; fresh package read, fresh `.project/` resume, and unrelated-task non-hijack pass. Explicit runtime route remains UNPROVEN because Bun was absent from the isolated child PATH. |
| ChatGPT installation and fresh-chat proof | BLOCKED | Current `dist/chatgpt/studio.zip` is ready, but upload and scan cannot complete until Chrome’s file-URL permission is enabled and the browser surface can perform the upload. |
| GitHub and Google Drive connections | PASS_WITH_LIMITATIONS | GitHub read/publication pass. Drive folder/governing-document reads and three authorized append-only reconciliation updates pass with revision-guarded readback. No permissions changed. |
| Confirmation-gated writes | PASS_WITH_LIMITATIONS | Local fail-closed write guards pass; current ChatGPT write smoke is UNPROVEN until a fresh current package session is available. |
| Greenfield and brownfield cross-surface pilots | BLOCKED | Local greenfield and brownfield portions pass; current ChatGPT -> Codex -> fresh ChatGPT Review loops await current ChatGPT installation. |
| Planted defect independently found and repaired | PASS_WITH_LIMITATIONS | Local Luna review found the planted billing defect, bounded Codex repair passed, and local acceptance passed; current-SHA ChatGPT confirmation remains blocked. |
| Fresh independent ChatGPT Review | BLOCKED | Requires current package upload, fresh chat, and review against the published current branch SHA. |
| Rollback and recovery | PASS_WITH_LIMITATIONS | Scoped rollback instructions, verified Codex backup, branch isolation, and non-destructive dry-run are recorded; uninstall/disconnect/merge/release were not executed. |
| iPhone/mobile availability | USER CHECK | The owner must personally verify mobile availability. |

## Current artifact evidence

- ChatGPT archive: `dist/chatgpt/studio.zip`.
- Archive SHA-256: `D004F894ACA624DC86DFF346D208820F0B76AE67D0B01862CCA15B84CD00E796`.
- Archive size: 141,805 bytes.
- Codex package: `studio-delivery@studio-v2`, version `2.0.0`.
- No MCP server, localhost dependency, tunnel, API key, or secret is present
  in the default ChatGPT artifact.

## Acceptance boundary

Studio is not declared fully complete. The remaining blocking evidence is
current browser-side ChatGPT installation and verification, both current
cross-surface pilots, and a fresh ChatGPT Review at the published SHA. No
executor self-accepted or merged work, and no merge or release was performed.
