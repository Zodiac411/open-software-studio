# Pilot A receipt: greenfield

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-A

Reviewed checkpoint: c00f7ab98ef83108675ffcda06f2f04f81c7977e

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
- Current project state, SNAP-004, WP-001, EVID-PILOT-A-003, and
  HANDOFF-C00F7AB98EF8 are current against the reviewed checkpoint.
- Final local acceptance review: REV-004 and INDEPENDENT_REVIEW_005, fresh
  context, ACCEPT/PASS_WITH_LIMITATIONS for the local repaired checkpoint with
  no blocking local implementation finding.

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
- Codex handoff and local execution: PASS_WITH_LIMITATIONS.
- Fresh ChatGPT Review: BLOCKED. Review 003 ran at
  https://chatgpt.com/c/6a947ba5-7af0-83eb-8549-2d5c1cde6d5b and could not
  inspect current SHA c00f7ab98ef83108675ffcda06f2f04f81c7977e because the
  branch is not present on the canonical GitHub remote; it also recorded the
  stale canonical Drive baseline. Typed findings are in
  `bootstrap/INDEPENDENT_CHATGPT_REVIEW_003.md`.
- GitHub and Drive reads: PASS in both the connected Codex environment and the
  ChatGPT verification chat.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

The local greenfield proof is complete, but the requested full
ChatGPT -> Codex -> fresh ChatGPT Review loop is not claimed.
