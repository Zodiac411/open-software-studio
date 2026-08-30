# Pilot A receipt: greenfield

Result: PASS_WITH_LIMITATIONS

Project: PRJ-PILOT-A

Reviewed checkpoint: 18ddbc14a6f9b16967064f4066ff167799cb8a92

## Evidence

- Greenfield fixture: evals/pilots/greenfield.
- Local acceptance: python evals/pilots/greenfield/test_app.py returned exit
  0 for greeting(" Ada ") == "Hello, Ada!".
- Studio lifecycle: init, plan, freeze, context, work-package validation,
  evidence add/validate, current-SHA handoff, status, doctor, and tracking
  projection all completed without external writes.
- Fresh Codex session: PASS_WITH_LIMITATIONS. A new read-only process read the
  project state and reported phase IN_REVIEW, active work package WP-001, and
  the next action independent fresh-context review. It did not edit or merge.
- Unrelated fresh Codex task: PASS. A separate process answered 2+2=4 without
  inspecting files or invoking Studio.
- Current project state, SNAP-002, WP-001, EVID-PILOT-A-002, and
  HANDOFF-18DDBC14A6F9 are current against the reviewed checkpoint.

## Cross-surface gates

- ChatGPT intake and Studio routing: BLOCKED pending visible account/workspace
  confirmation.
- Codex handoff and local execution: PASS_WITH_LIMITATIONS.
- Fresh ChatGPT Review: BLOCKED; no ChatGPT installation or fresh chat was
  attempted while account identity was unconfirmed.
- GitHub and Drive reads: PASS in the connected Codex environment; ChatGPT-side
  reads are NOT_RUN.
- External writes: NOT_RUN.
- iPhone/mobile availability: USER CHECK.

The local greenfield proof is complete, but the requested full
ChatGPT -> Codex -> fresh ChatGPT Review loop is not claimed.
