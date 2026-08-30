# Connected applications receipt

Result: PASS_WITH_LIMITATIONS

Recorded: 2026-08-30

## GitHub

- Account label: Zodiac411.
- Target: Zodiac411/open-software-studio.
- Read probe: repository metadata, default branch, README, and repository
  permissions were read successfully.
- Default branch: master.
- Remote baseline HEAD: d697efc16d86835ff3941f54b05e560b91a4a125.
- Permissions observed: admin/maintain/pull/push/triage.
- External writes: none.
- Issue/milestone reconciliation: local confirmation-gated projection only;
  no issue, milestone, comment, branch push, or PR was created.

Status: PASS for the read-only connector probe; external write behavior is
NOT_RUN.

## Google Drive

- Account label: HellStar / badcrayfish11@gmail.com.
- Canonical workspace:
  https://drive.google.com/drive/folders/1GDlSRW9aJVOvCH-fiZcWPQYsQcUNYGXe
- Read probe: canonical folder listing and governing documents were read
  successfully.
- Governing document IDs and Drive revisions are recorded in
  bootstrap/REQUIREMENTS.md.
- External writes: none.
- Full Access was not enabled and permissions were not changed.

Status: PASS for the read-only connector probe; external write behavior is
NOT_RUN.

## ChatGPT-side connections

- Visible account/workspace identity confirmation: PASS. The browser showed
  chris folorunso / Pro with no workspace label, and the user confirmed it.
- ChatGPT GitHub connection: PASS for read-only use. The fresh verification
  chat visibly used GitHub and resolved Zodiac411/open-software-studio.
- ChatGPT Drive connection: PASS for read-only use. The same chat visibly used
  Google Drive and resolved the canonical Studio Delivery workspace.
- ChatGPT returned a read-only Studio V2 brief and reported no unavailable
  connector or permission for those probes.
- ChatGPT Studio routing: PASS. A fresh `@Studio` chat returned
  `STUDIO_ROUTE_OK studio-chatgpt-studio-delivery` at
  https://chatgpt.com/c/6a94741f-cedc-83eb-a82c-240a2a5acd42.
- ChatGPT write-confirmation gate: PASS_WITH_LIMITATIONS. A fresh Studio Track
  chat at https://chatgpt.com/c/6a947454-fac4-83eb-a3ed-3265561e8b76 showed
  the exact proposed GitHub issue mutation and stopped for explicit approval;
  no external write was executed.
- Fresh independent ChatGPT Review: BLOCKED. Review 003 at
  https://chatgpt.com/c/6a947ba5-7af0-83eb-8549-2d5c1cde6d5b independently
  confirmed that the expected branch and SHA are absent from canonical GitHub
  and that Drive still records the pre-V2 baseline; typed findings are recorded
  in `bootstrap/INDEPENDENT_CHATGPT_REVIEW_003.md`.
- ChatGPT-side external writes: NOT_RUN. No issue, milestone, comment, file,
  folder, document, permission, or custom-instruction write was attempted.
- Full Access was not enabled and no account selection or permission change was
  performed.
