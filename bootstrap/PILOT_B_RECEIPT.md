# Pilot B receipt: brownfield defect repair

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-B

Implementation checkpoint: 468e231b55558052906aafc267e135608ddb94ff

## Evidence

- Brownfield fixture: evals/pilots/brownfield.
- First independent review: REV-001, fresh 5.6 Luna reviewer, disposition
  REPAIR.
- FINDING-001 was the planted cents-formatting defect. Before repair,
  python test_billing.py returned the expected failure, "$12" versus "$12.34".
- Bounded repair: REPAIR-FINDING-001 changed only billing.py and used no new
  dependency.
- Repair validation: PASS.
- After repair, python evals/pilots/brownfield/test_billing.py returned exit
  0 and format_cents(1234) returned "$12.34".
- Current project state, SNAP-014, WP-001, EVID-PILOT-B-012, and
  HANDOFF-468E231B5555 are current against the implementation checkpoint.
- EVID-PILOT-B-012 records complete synthesized-entry ZIP ordering, the
  validator assertion, committed-HEAD clean-checkout reproducibility, and
  canonical source-manifest validation.
- Review 008 accepted the prior checkpoint with one archive-order contract
  finding; REPAIR-ARCHIVE-ORDER is now at `468e231`. Review 009 verified that
  repair but found stale `SETUP_STATE.json` review text; REPAIR-REV-009-001
  records the fix and Review 010 is pending.

## Cross-surface gates

- ChatGPT intake and Studio routing: PASS_WITH_LIMITATIONS. The fresh chat at
  https://chatgpt.com/c/6a946dee-ef10-83ed-9c1b-3e86b9b6cc15 visibly routed
  through Studio and completed read-only GitHub/Drive probes with a V2 brief.
- Explicit ChatGPT routing: PASS. A fresh `@Studio` chat returned
  `STUDIO_ROUTE_V2_OK studio-chatgpt-studio-delivery` at
  https://chatgpt.com/c/6a9490be-6f08-83eb-9110-f95f56ee4226.
- ChatGPT write gate: PASS_WITH_LIMITATIONS. A fresh Studio Track probe at
  https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 showed the exact
  proposed GitHub mutation and stopped pending approval; no write occurred.
- Codex handoff, local defect detection, repair, green test, independent
  acceptance, and the fail-closed session-close guard: PASS_WITH_LIMITATIONS.
  Both pilot sessions closed only after the current independent local review
  was accepted; the fresh ChatGPT review remains pending.
- Fresh ChatGPT Review: Review 009 was BLOCKED by stale machine-readable state
  text after independently verifying the complete archive-order repair at
  `468e231`; REPAIR-REV-009-001 records the fix and Review 010 is pending.
  Drive's authoritative update still requires separate approval.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

No executor accepted or merged its own repair.
