# Independent review 001

Result: BLOCKED

Reviewer: isolated 5.6 Luna subagent (Epicurus), read-only review

Reviewed revision: a9454048456c9cef9d5eca0fa8be47b3ecc4ee4c

Reviewed branch: studio-v2-bootstrap

The reviewer inspected the current requirements, catalog, generated family,
V2 schemas, compiler, validators, evaluation fixtures, provenance, setup
receipts, rollback instructions, and pilot state before reaching a verdict.

## Gate results

- Canonical catalog, generated family, legacy preservation, and provenance:
  PASS
- Skills-first ChatGPT archive with no MCP declaration: PASS
- Repository validators and evaluations: PASS
- Write and release gates: PASS
- Deterministic build evidence: PASS_WITH_LIMITATIONS; fixed archive
  timestamps and prior matching digests exist, but this review did not rerun
  the writing build.
- Greenfield direct pilot: PASS via python test_app.py
- Greenfield pytest discovery: NOT_RUN; no tests were collected.
- Brownfield pilot: BLOCKED; python test_billing.py returned the expected
  assertion failure, "$12" versus "$12.34".

## Typed findings

### FINDING-001

- Status: BLOCKED
- Severity: BLOCKING
- Evidence: evals/pilots/brownfield/billing.py and python test_billing.py.
- Remediation: repair the cents formatter, rerun the direct pilot, then obtain
  a fresh independent review.

### FINDING-002

- Status: BLOCKED
- Severity: HIGH
- Evidence: both pilot state and handoff records point to c2d9bcf while the
  reviewed repository is a945404; scripts/studio.py status and doctor report
  the stale state. SETUP_STATE.json also contains obsolete checkpoint fields.
- Remediation: regenerate pilot state, handoffs, and setup receipts against the
  exact final SHA and rerun freshness checks.

### FINDING-003

- Status: NOT_RUN
- Severity: MEDIUM
- Evidence: pytest in the greenfield pilot collected zero tests while the
  direct command passed.
- Remediation: retain the direct command as the named acceptance check or
  configure test discovery and rerun; do not treat pytest collection as proof.

Recommendation: do not accept, merge, or release until FINDING-001 and
FINDING-002 are repaired and a new independent review validates the current
SHA.
