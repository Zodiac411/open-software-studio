---
name: studio-session-intelligence
description: Produce a local, on-demand, redacted Session Intelligence summary for the current project from selected session metadata and classified friction signals.
---

# Studio Session Intelligence

Use this skill only for a local, read-only `RETRO_DISTILLATION` and `CONTEXT_CAPSULE` derived from the current project’s recent sessions. It is on-demand; it has no daemon, scheduler, MCP server, board writer, or session-history writer.

## Contract

- Default scope is the requested project and the last 30 days. Accept explicit session IDs only when the caller names them.
- Invoke `session_intelligence.py` from this skill directory with an absolute `--project` path. The helper reads only session metadata and generic event classifications; it never emits session bodies, tool payloads, credentials, or source paths.
- Keep the helper’s `PASS_WITH_LIMITATIONS`, `BLOCKED`, and limitations fields intact. Stop on a `BLOCKED` result rather than widening the scope.
- A persisted artifact is optional and requires the caller to select an explicit absolute `--output` path in an allowed project location. Never write to session history, a project board, or an external surface.

## Procedure

1. Confirm the project directory and whether the default 30-day scope is sufficient. Do not infer a different project or session ID.
2. Run `python session_intelligence.py --project <absolute-project-path> --format markdown`. Add `--session-id <id>` only for caller-supplied IDs. Use explicit session roots only for an approved fixture or recovery location.
3. Convert the result into the existing Studio-style headings: `RETRO_DISTILLATION` for recurring friction and proposed bounded work packages; `CONTEXT_CAPSULE` for scope, evidence references, limitations, and one next action.
4. Retain only the redacted helper output. Do not quote, paste, or attach raw session text, tool input/output, credentials, or unrelated-project records.

## Output shape

The helper reports project-scoped observations, generic friction counts, evidence references in the form `session:<id>`, empty or proposed bounded work packages, limitations, and one next action. A zero-match result is `PASS_WITH_LIMITATIONS`; an invalid or out-of-scope explicit target is `BLOCKED`.

## Never own

- Full session-history injection or unbounded cross-project search.
- Live-completion inference from local artifacts.
- Credential recovery, secret inspection, background monitoring, scheduling, MCP, or board writing.
