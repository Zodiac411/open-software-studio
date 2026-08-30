# Independent ChatGPT Review 004

Result: BLOCKED
Recorded: 2026-08-30
Review URL: https://chatgpt.com/c/6a947e69-e5cc-83ed-acca-cd9080b913f5
Reviewed remote branch tip: 42b43b8dc9a77754b23300a9d634da283ecba69f
Branch: studio-v2-bootstrap

## Independent disposition

The fresh ChatGPT reviewer verified that the named branch and commit existed
remotely, cloned the remote checkpoint read-only, and independently ran the
repository validators, evaluations, pilot smoke commands, archive checks, and
Drive comparison. It returned BLOCKED with the typed findings below.

## Typed findings

- `FIND-001` BLOCKING / High: committed setup state, pilots, handoffs, reviews,
  receipts, and final acceptance still identified parent checkpoint c00f7ab.
  Remediation: regenerate the active evidence against the repaired immutable
  source checkpoint and preserve superseded history.
- `FIND-002` BLOCKING / High: a clean remote build changed the committed
  `studio.zip` and generated PNG assets, producing a different stable archive
  digest. Remediation: stop normal builds from regenerating Pillow-dependent
  raster assets or pin the renderer, and add a clean-checkout reproduction
  gate.
- `FIND-003` BLOCKING / High: canonical Drive remained on the pre-V2 baseline
  while GitHub contained the V2 branch. Remediation: after source acceptance,
  update authoritative Drive records through a separately approved write.
- `FIND-004` IMPORTANT / High: existing validators missed stale-SHA and
  clean-rebuild drift. Remediation: add reproducibility and active-state gates.
- `FIND-005` IMPORTANT / High: Codex and ChatGPT runtime evidence was tied to
  the older source checkpoint. Remediation: prove the same archive bytes at the
  repaired checkpoint and run fresh routing/read-only probes as needed.
- `FIND-006` IMPORTANT / High: pilot snapshots, states, handoffs, and reviews
  closed the parent checkpoint rather than the published tip. Remediation:
  refresh both pilot evidence after the build repair.
- `FIND-007` MODERATE / High: rollback dry-run evidence was recorded only at
  the parent checkpoint. Remediation: repeat the non-mutating preflight at the
  repaired checkpoint.
- `FIND-008` MODERATE / High: the branch was unprotected, required checks were
  disabled, and the checkpoint was unsigned. Remediation: configure an
  owner-approved protected release path before merge/release; signing remains
  optional unless adopted as policy.

No external write, merge, Drive mutation, installation change, permission
change, or secret access occurred during this review.
