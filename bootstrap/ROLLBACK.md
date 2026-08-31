# Studio V2 rollback and recovery

Result: PASS_WITH_LIMITATIONS

This setup uses a separate worktree and branch. The remote default branch and
unrelated user work were not reset, cleaned, stashed, overwritten, or deleted.

## Checkpoints

- Baseline `master`: `d697efc16d86835ff3941f54b05e560b91a4a125`.
- Implementation branch: `studio-v2-bootstrap`.
- Implementation source checkpoint: `da5038327ce517b9bea4c4b6ee18c112ad82ce14`.
- Worktree: `C:/Users/badcr/Documents/Codex/2026-08-30/you-are-the-implementation-and-setup/studio-v2-bootstrap`.
- Codex AGENTS backup: `C:/Users/badcr/.codex/backups/studio-v2/AGENTS.md.before-studio-v2-20260831-182256`.
- AGENTS backup SHA-256:
  `CD9E3F64E967E6EA697DF6678244FC17E3C2D54DFA74D65E20F8B6953BEDDF34`.

## Repository recovery

Inspect before changing anything:

```powershell
git -C <worktree> status --short
git -C <worktree> diff --stat d697efc16d86835ff3941f54b05e560b91a4a125
git -C <worktree> log --oneline --decorate -8
```

For a local diagnostic return to baseline, use the separate worktree only:

```powershell
git -C <worktree> switch --detach d697efc16d86835ff3941f54b05e560b91a4a125
```

Do not delete the implementation branch or worktree as part of routine
recovery. If generated outputs must be reverted, review the diff and restore
only paths owned by this branch. Preserve `bootstrap/` receipts as the audit
record.

## Codex recovery

1. Re-read the current installed command help: `codex plugin --help`.
2. Remove only `studio-delivery@studio-v2` with the command reported by that
   help; leave the legacy Open Software Studio packages untouched.
3. Remove only the `<!-- STUDIO V2 BEGIN -->` through
   `<!-- STUDIO V2 END -->` block from `C:/Users/badcr/.codex/AGENTS.md`, if
   desired.
4. Restore the verified AGENTS backup only after checking the exact path and
   SHA-256. Do not overwrite unrelated later instructions without owner
   approval.
5. Remove `C:/Users/badcr/.studio/config.yaml` only if the Studio defaults are
   no longer wanted.

No Codex uninstall or global rollback was executed during this run.

## ChatGPT recovery

If the current Skill upload completes, disable or remove only the current
Studio Skill through the visible ChatGPT Skills UI after confirming the exact
skill. Do not remove unrelated skills or plugins. No custom-instruction change
was made, so there is no instruction rollback to perform.

## Google Drive recovery

The reconciliation changed only append-only content in SD-DOC-000,
SD-DOC-002, and SD-DOC-040. To recover, inspect each document’s revision
history and restore the prior revision through the visible owner-controlled
Drive UI after review. Do not delete documents or change sharing. No Drive
permission change was made.

## Dry-run verification

The non-destructive dry-run is PASS_WITH_LIMITATIONS: the baseline resolves,
the implementation branch is separate, the AGENTS backup exists with a
verified digest, the generated package/cache trees match, and the Drive
updates are revision-guarded. Actual uninstall, disconnect, deletion, merge,
release, or ChatGPT removal remains NOT_RUN. iPhone/mobile remains USER CHECK.
