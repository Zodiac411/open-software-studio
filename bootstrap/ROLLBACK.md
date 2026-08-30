# Studio V2 rollback and recovery

This bootstrap uses an isolated worktree and keeps the remote default branch untouched.

## Local source and branch

- Baseline SHA: `d697efc16d86835ff3941f54b05e560b91a4a125`
- Implementation branch: `studio-v2-bootstrap`
- Source repository: `open-software-studio.git` (bare clone in the task workspace)
- Implementation worktree: `studio-v2-bootstrap`

To return to the baseline without touching unrelated work:

```powershell
git -C <worktree> diff --stat d697efc16d86835ff3941f54b05e560b91a4a125
git -C <worktree> diff d697efc16d86835ff3941f54b05e560b91a4a125 -- <path>
git -C <worktree> switch --detach d697efc16d86835ff3941f54b05e560b91a4a125
```

The last command is a local diagnostic/recovery choice only. Do not delete the implementation branch or worktree as part of routine rollback.

## Generated repository outputs

Generated packages, icons, templates, fixtures, and receipts are owned by the Studio V2 branch. Revert the branch or restore only the generated paths after reviewing `git diff`; do not reset or clean another checkout. The bootstrap audit and receipts are intentionally preserved as the recovery record when source outputs are rolled back.

## Codex

1. Record the installed Studio version and source marketplace.
2. Disable or remove only the Studio package installed by this bootstrap; preserve the seven pre-existing legacy packages.
3. Restore the prior managed block in `C:/Users/badcr/.codex/AGENTS.md` from the backup recorded in `bootstrap/CODEX_INSTALL_RECEIPT.md` after that receipt exists. Before Codex installation, the preflight record in `bootstrap/SETUP_AUDIT.md` is the applicable evidence and no global block should be removed.
4. Remove only the bootstrap-created `%USERPROFILE%/.studio/config.yaml` if the owner requests a full rollback; do not remove unrelated configuration.
5. Refresh Codex and verify an ordinary non-Studio task still routes normally.

## ChatGPT

1. Uninstall or disable only the Studio package/Skill created by this bootstrap.
2. If a managed custom-instruction block was ever approved and added, remove only `[STUDIO WORKFLOW BEGIN]` through `[STUDIO WORKFLOW END]`; preserve all other text. No such change is authorized by default.
3. Leave pre-existing GitHub and Google Drive connections intact. Disconnect only a connection created by this bootstrap and only after owner approval.
4. Delete only temporary smoke-test artifacts that were explicitly created and recorded; prefer closing a temporary issue and moving temporary Drive artifacts to trash rather than deleting without confirmation.

## External and release recovery

- No GitHub issue, PR, Drive folder, or Drive document is created by the local bootstrap without an explicit owner gate.
- A branch push, marketplace import, external write smoke test, merge, or release remains separately reviewable and reversible.
- If the reviewed SHA changes, mark the previous review stale and run a fresh review against the new SHA.

## Dry-run status

The rollback paths are structurally documented. A non-destructive dry-run will verify path ownership and baseline resolution after implementation. External disconnect/delete and merge/release actions remain `NOT_RUN` unless explicitly approved.
