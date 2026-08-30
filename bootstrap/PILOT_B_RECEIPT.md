# Pilot B receipt: brownfield defect repair

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-B

Implementation checkpoint: 17e9407569eb642e11d86def752c22ae6b638337

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
- Current project state, SNAP-013, WP-001, EVID-PILOT-B-011, and
  HANDOFF-17E9407569EB are current against the implementation checkpoint.
- EVID-PILOT-B-011 records the repaired committed-HEAD clean-checkout
  reproducibility, explicit archive tie-breaker, and canonical source-manifest
  validation gates.
- Review 007 accepted the prior checkpoint with one low portability finding;
  REPAIR-ARCHIVE-TIEBREAK is now at `17e9407`, and Review 008 is pending.

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
- Fresh ChatGPT Review: PASS_WITH_LIMITATIONS in Review 007 for prior source
  `8f8e9fc`; the tie-breaker repair is published at `17e9407` and Review 008 is
  pending. Drive's authoritative update still requires separate approval.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

No executor accepted or merged its own repair.
