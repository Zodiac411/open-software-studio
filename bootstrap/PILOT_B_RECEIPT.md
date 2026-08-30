# Pilot B receipt: brownfield defect repair

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-B

Implementation checkpoint: 3b739c1e16dc089749aa13d282b4f7cce470e9cf

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
- Current project state, SNAP-009, WP-001, EVID-PILOT-B-007, and
  HANDOFF-3B739C1E16DC are current against the implementation checkpoint.
- The new EVID-PILOT-B-007 also records the committed-HEAD clean-checkout
  reproducibility gate.
- A fresh isolated local review at this checkpoint is pending; historical
  REV-004 and INDEPENDENT_REVIEW_005 remain preserved.

## Cross-surface gates

- ChatGPT intake and Studio routing: PASS_WITH_LIMITATIONS. The fresh chat at
  https://chatgpt.com/c/6a946dee-ef10-83ed-9c1b-3e86b9b6cc15 visibly routed
  through Studio and completed read-only GitHub/Drive probes with a V2 brief.
- Explicit ChatGPT routing: PASS. A fresh `@Studio` chat returned
  `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery` at
  https://chatgpt.com/c/6a94741f-cedc-83eb-a82c-240a2a5acd42.
- ChatGPT write gate: PASS_WITH_LIMITATIONS. A fresh Studio Track probe at
  https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 showed the exact
  proposed GitHub mutation and stopped pending approval; no write occurred.
- Codex handoff, local defect detection, repair, green test, and the
  fail-closed session-close guard: PASS_WITH_LIMITATIONS. Session close will
  only pass after the current independent local review is accepted; the fresh
  ChatGPT review remains pending.
- Fresh ChatGPT Review: NOT_RUN at the published repaired checkpoint. The
  historical blocked reports remain in the bootstrap directory; Drive's
  authoritative update still requires separate approval.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

No executor accepted or merged its own repair.
