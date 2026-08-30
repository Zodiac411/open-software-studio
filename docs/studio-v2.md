# Studio V2 implementation surface

`catalog/studio.yaml` is the only package-family source. The build command
renders:

- `generated/codex/plugins/*` and `dist/codex/*` for Codex;
- `.agents/plugins/marketplace.json` and `dist/marketplace/*` for marketplace
  import;
- `dist/chatgpt/studio.zip` as the default portable ChatGPT Skill artifact;
- `schemas/v2`, `templates/studio-v2`, `brand/icon-system`, routing cases, and
  seeded red/green fixtures.

The public display names are Studio, Studio Plan, Studio Design, Studio
Research, Studio Docs, Studio Review, Studio Build, Studio Verify, and Studio
Track. Stable pre-V2 IDs remain compatibility aliases. The V2 version is
`2.0.0` and the protocol is `2.0.0`.

## Control-plane commands

```powershell
python scripts/studio.py --project <root> doctor
python scripts/studio.py --project <root> init
python scripts/studio.py --project <root> status
python scripts/studio.py --project <root> plan
python scripts/studio.py --project <root> freeze --approved-by <owner-label>
python scripts/studio.py --project <root> context
python scripts/studio.py --project <root> wp validate
python scripts/studio.py --project <root> evidence validate
python scripts/studio.py --project <root> handoff
python scripts/studio.py --project <root> review validate
python scripts/studio.py --project <root> repair validate
python scripts/studio.py --project <root> close
python scripts/studio.py --project <root> release --approved-by <owner-label>
python scripts/studio.py --project <root> track
```

`track` writes a local, confirmation-gated GitHub projection plan. It never
creates or changes an external Issue or Milestone without an explicitly
approved exact plan. `.project/` remains the machine authority.

The result vocabulary is exactly `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`,
`NOT_RUN`, and `UNPROVEN`. A current SHA mismatch blocks status and review;
the executor role and same-session context cannot validate an `ACCEPT` review.
