# Pilot A receipt: greenfield

Result: BLOCKED

Recorded: 2026-08-31

Implementation source checkpoint: `da5038327ce517b9bea4c4b6ee18c112ad82ce14`.

## Local evidence

- Fixture: `evals/pilots/greenfield`.
- Application assertion: PASS. `python evals/pilots/greenfield/test_app.py`
  returned exit 0 for `greeting(" Ada ") == "Hello, Ada!"`.
- Studio lifecycle: PASS. Init, plan, freeze, context, work-package
  validation, evidence add/validate, current-SHA handoff, status, doctor, and
  tracking projection completed without external writes.
- Fresh local Codex state read: PASS_WITH_LIMITATIONS. A new read-only process
  read the project state and reported the expected closed pilot state and next
  independent-review action; it did not edit or merge.
- Fresh unrelated Codex task: PASS. A separate process answered `2+2=4`
  without inspecting files or invoking Studio.
- No executor accepted or merged its own work: PASS.

## Current cross-surface gates

- ChatGPT current archive upload: BLOCKED pending the connected Chrome
  extension’s file-URL permission and the upload scan.
- Fresh ChatGPT invocation and the complete ChatGPT -> Codex -> fresh ChatGPT
  Review loop: BLOCKED until the current archive is installed and invoked.
- Current-SHA independent ChatGPT Review: BLOCKED.
- ChatGPT write-confirmation smoke: UNPROVEN for the current archive.
- iPhone/mobile availability: USER CHECK.

Historical ChatGPT pilot records remain in this directory but refer to an
older archive/source checkpoint and are not reused as current evidence.
