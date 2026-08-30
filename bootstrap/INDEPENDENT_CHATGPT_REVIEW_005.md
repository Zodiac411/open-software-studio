# Independent ChatGPT Review 005

Result: BLOCKED

Reviewer: fresh ChatGPT Work chat using the installed Studio Review route.

Review URL: https://chatgpt.com/c/6a949225-51d0-83eb-9e92-c10b1107c2f7

Reviewed branch tip: `34bd8f358c20108925a3a533a36e458649f941d9`.

The reviewer independently read the connected GitHub and Drive sources,
cloned the published branch, compared the evidence-only tip with the declared
source checkpoint, and ran repository checks before reaching its conclusion.

## Typed findings

- `REV-001` / `BLOCKING` / `Local defect`: a clean Linux checkout of source
  checkpoint `441d656fca614db87089a580857227401ceb04a7` rebuilt 11 tracked
  files differently, including all nine ChatGPT archives,
  `dist/chatgpt/package-source.json`, and
  `generated/catalog/archive-hashes.json`.
- `REV-002` / `HIGH` / `Local defect`: the ChatGPT archive entry order depended
  on host-specific `Path` ordering. The Windows archive placed `README.md`
  after `assets/`, while the Linux rebuild placed it before `assets/`; the
  recorded archive hash therefore did not prove cross-platform determinism.
- `REV-003` / `HIGH` / `Evidence defect`: the active acceptance receipts
  claimed the clean-checkout reproducibility repair passed, which was not true
  under the reviewer’s Linux rebuild.
- `REV-004` / `PASS` / `Source integrity`: the branch and checkpoint were
  published, the checkpoint was an ancestor, and post-checkpoint paths were
  restricted to `bootstrap/` and `evals/pilots/`.
- `REV-005` / `PASS` / `Catalog and package structure`: the reviewer confirmed
  the canonical catalog, generated package family, schemas, icons, and package
  validation before the reproducibility blocker stopped acceptance.

## Repair recorded

The executor did not self-accept this review. The minimal repair changed only
the archive path sort in `scripts/build_studio.py` to an explicit POSIX,
case-folded key. It was committed and pushed as
`4afaa3d17be234187fe77aece05a9e2024cac556`. Local build, validator,
committed-HEAD reproducibility, evaluation, greenfield, and brownfield checks
pass after that repair. A new fresh ChatGPT review is required against the new
source checkpoint.

Canonical Drive remains read-only and unchanged; no issue, milestone, PR,
permission, merge, release, or other external write was performed.
