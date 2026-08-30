# Independent ChatGPT Studio Review 007

Result: PASS_WITH_LIMITATIONS

Reviewed: 2026-08-30

Reviewer: fresh ChatGPT chat using the installed Studio Review skill

Review chat: https://chatgpt.com/c/6a949bad-ee94-83eb-93b3-4eaa84c45681

Repository: https://github.com/Zodiac411/open-software-studio

Branch reviewed: `studio-v2-bootstrap`

Branch tip reviewed: `766888b2a3382dc8a0e7db58429d5de04f452748`

Source checkpoint reviewed: `8f8e9fc2164a1ceeb503aecb36edbf8dc8c48dd6`

## Independent result

The reviewer cloned the published branch and independently verified the
source checkpoint, evidence-only post-source commits, catalog/package family,
archive hashes, ZIP_STORED entries, validators, evaluations, pilots, lifecycle
guards, receipts, and rollback. Fresh Linux validation, evaluations, and
committed-HEAD reproducibility all passed. The original Review 006 blocker is
closed.

## Typed findings

- `REV-007-001` through `REV-007-013`: INFO through MEDIUM verification and
  external-limit findings. The branch, source identity, reproducibility,
  package/hash integrity, generated family, seeded gates, pilot evidence,
  lifecycle guards, receipt consistency, and rollback all passed. Canonical
  Drive remains pre-publication and requires a separately authorized write;
  GitHub branch protection/signatures and complete Drive permission topology
  were not asserted by the read-only probes.
- `REV-007-014` / `LOW` / `Portability risk`: the archive ordering was
  explicitly case-folded but did not make a UTF-8 byte tie-breaker visible in
  the implementation contract. No current case-fold collision exists, so the
  published bytes were deterministic for the current catalog.
- `REV-007-015` / `INFO` / `Rollback`: rollback is bounded, source-aware,
  non-destructive, and approval-gated.

## Disposition

The source checkpoint was accepted with limitations. The follow-up bounded
repair `REPAIR-ARCHIVE-TIEBREAK` adds an explicit UTF-8 byte tie-breaker for
case-fold collisions. Because that repair changes the source checkpoint, this
review is now historical and a new fresh review is required for `17e9407`.
No external write, merge, release, or permission change was performed.
