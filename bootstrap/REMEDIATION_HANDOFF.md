# Studio V2 remediation handoff

Result before independent review: `PASS_WITH_LIMITATIONS`

## Reviewer instructions

Inspect the governing review report, live Git HEAD, base-to-head diff, current
requirements, generated package metadata, and direct command output before
reading the claimed outcomes below. Do not inherit the executor conclusion.
Reject stale SHA evidence and do not merge or release.

## Scope

- Review baseline: `ce04df0f682d84bdf7818ae8a204162ce9567c86`
- Local remediation code head: `f300908d5306085f72215ce09e95f5cf8f434033`
- Final review candidate: resolve live Git HEAD after this handoff commit
- Branch: `studio-v2-bootstrap`
- External writes: `NOT_RUN`

## Bounded implementation commits

| Commit | Package | Claimed outcome |
|---|---|---|
| `8941070` | CI/readiness foundation | V2 docs, initial clean-checkout CI, and bounded MCP readiness polling. |
| `dcc6750` | Luna WP-A | Atomic state writes, strict current-SHA independent review, generic planning/tracking, coherent recovery, evidence/handoff repair, and focused regressions. |
| `4ba6ddb` | Luna WP-B | Catalog-owned recipes/prompts/provenance, typed schemas, useful templates, distinct lens contracts, and regenerated packages. |
| `417275c` | Review repair | Windows/Linux CI, security/archive gate, and explicit optional compatibility-server identity. |
| `f300908` | Integration repair | Runtime/schema alignment, malformed artifact rejection, portable compiler targets, executable evaluation gates, and canonical source coverage. |

## Direct local evidence

```text
python scripts/build_studio.py --check-only
PASS: catalog and all canonical generated outputs match a clean temporary rebuild

python scripts/validate_suite.py
PASS: catalog, 9 generated packages, 71 skills, V2 schemas, icons, archive, routing, and seeded gates validated
PASS: two clean-checkout builds reproduced canonical text and binary content

python scripts/run_evals.py
PASS: 71 routing specialists x 3 cases; 10 execution scenarios; cross-plugin demo chain; 6 seeded Studio gates; 6 executable control-plane regressions

python scripts/security_checks.py
PASS: 1365 tracked paths scanned; packaged paths are traversal-safe

Plugin Creator and Skill Creator under PYTHONUTF8=1
PASS: 9 generated plugins and 35 generated source skills

bun run mcp:check (twice)
PASS: MCP health, initialization, and execution-guard tool discovery

python evals/pilots/greenfield/test_app.py
exit 0

python evals/pilots/brownfield/test_billing.py
exit 0
```

## Known limits

- The current commits are local and not yet published to GitHub.
- Hosted CI has not executed the new workflow.
- The repaired Codex package has not been reinstalled in a fresh Codex host
  session.
- The repaired ChatGPT archive has not been uploaded or invoked in a fresh
  ChatGPT chat.
- The two full cross-surface pilots and fresh ChatGPT Review have not been
  replayed at the remediation SHA.
- Drive revision drift remains unresolved and requires owner-approved writes.
- External GitHub issue/milestone application remains approval-gated and was
  not executed.
- Real-host icon presentation, Chrome extension availability, and mobile
  availability remain unproven or USER CHECK.

## Requested reviewer action

Return typed findings with exact files, lines, commands, and observed results.
Use `ACCEPT` only if the final live SHA is clean, deterministic, behaviorally
gated, and has no blocking local defect. External account/publishing limits
must remain explicit and must not be converted into local passes.
