# Independent ChatGPT Studio Review 008

Result: PASS_WITH_LIMITATIONS

Reviewed: 2026-08-30

Reviewer: fresh ChatGPT chat using the installed Studio Review skill

Review chat: https://chatgpt.com/c/6a949e45-7e7c-83eb-97db-d34fbbe85183

Repository: https://github.com/Zodiac411/open-software-studio

Branch reviewed: `studio-v2-bootstrap`

Branch tip reviewed: `27a387bfd58d246ddaf2192e5b450a14647f5737`

Source checkpoint reviewed: `17e9407569eb642e11d86def752c22ae6b638337`

## Independent result

The reviewer independently read GitHub and Drive, cloned the published branch,
ran the repository validators/evaluations/reproducibility gates, checked the
package hashes, source-to-tip scope, pilot state, installation receipts,
connections, permissions, and rollback. The branch, package family, generated
artifacts, hashes, V2 schemas, Opal Seed assets, pilots, lifecycle guards, and
clean-checkout reproducibility passed. The attached receipts matched the
repository counterparts.

## Typed findings

- `REV-008-011` / `LOW` / `Incomplete archive-order contract`: the source
  package files used the explicit `(casefolded POSIX path, UTF-8 bytes)` key,
  but synthesized `SKILL.md` and `agents/openai.yaml` entries were appended
  afterward. The complete ZIP entry list was therefore not globally ordered by
  the declared key, although current bytes were reproducible.
- `REV-008-024` / `MEDIUM` / `Canonical Drive state`: the connected Drive
  workspace remained the pre-publication governing structure and did not mirror
  the GitHub package/evidence tip. This requires a separately authorized
  external write and is not a local implementation defect.
- `REV-008-012` / `MEDIUM` / `ChatGPT host-proof limitation`: the receipt
  supports the Windows Codex install, Skills UI, prior fresh-chat route, and
  write-gate probe, but a read-only GitHub/Drive review cannot replay those
  historical host interactions.
- `REV-008-022` / `INFO` / `GitHub governance`: the branch is unprotected and
  commits are unsigned; the authenticated read probe reports admin-level access.

## Disposition

The reviewer accepted the source with limitations and explicitly required the
archive-order contract repair plus a validator assertion over every complete
ZIP entry list. `REPAIR-ARCHIVE-ORDER` implements that bounded repair at source
checkpoint `468e231`; this review is now historical and a new fresh review is
required. No external write, installation, merge, release, or permission
change was performed by the reviewer.
