# Pilot A receipt: greenfield

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-A

Implementation checkpoint: 468e231b55558052906aafc267e135608ddb94ff

## Evidence

- Greenfield fixture: evals/pilots/greenfield.
- Local acceptance: python evals/pilots/greenfield/test_app.py returned exit
  0 for greeting(" Ada ") == "Hello, Ada!".
- Studio lifecycle: init, plan, freeze, context, work-package validation,
  evidence add/validate, current-SHA handoff, status, doctor, and tracking
  projection all completed without external writes.
- Fresh Codex session: PASS_WITH_LIMITATIONS. A new read-only process read the
  project state and reported phase CLOSED, active work package WP-001, and the
  next action independent fresh-context review. It did not edit or merge.
- Unrelated fresh Codex task: PASS. A separate process answered 2+2=4 without
  inspecting files or invoking Studio.
- Current project state, SNAP-014, WP-001, EVID-PILOT-A-012, and
  HANDOFF-468E231B5555 are current against the implementation checkpoint.
- EVID-PILOT-A-012 records complete synthesized-entry ZIP ordering, the
  validator assertion, committed-HEAD clean-checkout reproducibility, and
  canonical source-manifest validation.
- Review 008 accepted the prior checkpoint with one archive-order contract
  finding; REPAIR-ARCHIVE-ORDER is now at `468e231`. Review 009 verified that
  repair but found stale `SETUP_STATE.json` review text; REPAIR-REV-009-001
  records the fix. Review 010 independently accepted the repaired state with
  no local defect.

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
- Codex handoff and local execution: PASS_WITH_LIMITATIONS.
- Fresh ChatGPT Review: Review 010 returned PASS_WITH_LIMITATIONS after
  independently verifying the complete archive-order repair at `468e231` and
  the state repair. Drive's authoritative update still requires separate
  approval.
- GitHub and Drive reads: PASS in both the connected Codex environment and the
  ChatGPT verification chat.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

The greenfield ChatGPT -> Codex -> fresh ChatGPT Review loop is complete with
the documented external and user-check limitations.
