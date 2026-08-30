# Studio V2 governing requirements

This file makes the external governing inputs reproducible without copying
their full contents into the repository. The implementation reads the
current repository state and treats these sources as the authority map.

| ID | Source | Drive revision observed | Use |
|---|---|---|---|
| SD-DOC-043 | [Codex Master Bootstrap Prompt](https://docs.google.com/document/d/19Nz-U2hgJqjwxlohbnjtU_teRR4F1pgHJDwYqjaLbgE/edit) | `ANLCKQnAdaXU-qBD6cqTm2Vj-kWOzx9g5Kf6RZbz6YzrnLuDCWY8wyXerByOUM3U4Ar0MTYd2xtjWRXmpQcVqZqsSnmN9C9-mcbOghcaNzE` | Governing scope, work packages, gates, result states |
| SD-DOC-036 | [End-to-End Bootstrap Plan](https://docs.google.com/document/d/1pAiDbApXsnS_bqm73q2K00ZvAc8pfNzDbshK3o8D8RU/edit) | `AIroW36FBXNi-chulF1PqsPn2lw3v0B5pLwCBJf5c-l5lHzwxCWjeYe-He93WtIlh1WF1x4YcNs3Zbow9OSo-tJ0PzitW88tcI_hh0mdYKU` | Sequencing and acceptance evidence |
| SD-DOC-044 | [Setup Acceptance and Recovery](https://docs.google.com/document/d/1WTJp3NMciUOJNqM1cFHKdReQJ63DE3DZMuQ1-fwylmg/edit) | `ANLCKQmEuO90xTqRSA1zIn3W4PmtPS56huFqz9dBXAKSatigv5tjsz4ar5voqM3Bk0Jrf9nLQT-CPSPZBaQOlsD16jmXsFi-BXEUVrBcHFU` | Human gates, recovery, and external-write policy |
| SD-DOC-045 | [Future Project Quickstart](https://docs.google.com/document/d/15fRTlcpfLoLLAv7dPfNnDhkuohdWAGFIZZTKwj5cDz4/edit) | `ANLCKQljEwcxQ7Yc3dd3CuvW5BvGVNIfJTLjc85VNMnSYdUnWJGA0X98nZLncLmEvJgFRjaBayGLR9uanmm4bPBVeSSEfZDm_mgriQjScis` | Fresh-project invocation and handoff contract |
| SD-DOC-013 | Drive workspace record `17Kahp-ECMyGTnse-nFHT4ZSZaHiG9WhoHhkLnJr7GOI` | `ANLCKQno8SVwY3F25NeKFm3J5BQdQjvNb2w6x5cX-P_IfutRcImAz-VBkJQQRX8n3BY-HniQfuXGSdEJiImiUk9nHNpsi2PzDIXkMb_OKq0` | Opal Seed naming and icon direction |
| SD-DOC-024 | Drive workspace record `1yd0XI_PM6Scx3bAYugBtdOUAzbUvhIfsb_A4hSEUK3k` | `ANLCKQl63GhuE-PDg-eJrOSeUFR1oeNPNlsjbFFji-vdhyimtJfTcthUW_f3mdNCGPi9BOOSO0wan8okUsqAM-xai1O76NKUpZPzN3RhTCI` | V2 artifact and template conventions |
| SD-DOC-025 | Drive workspace record `17Bj1dzcYP-XNvU9J1euoaiogQ-hguyMF9eFmwq8VV9A` | `ANLCKQnWhOUJw92Qu7j-rAxElTyF9TpKBnVK3OwVZTTeBwvMAB75pFupxPql2x8TAbM0u3FZxR1W8-Ea6xVCTu6wq09PIRTokQO1wQNfEN4` | ChatGPT planning and review surface |
| SD-DOC-030 | Drive workspace record `13k-nTkA9JsDoqoBQ7PGquET-rEtDAim5aSV5Ywjm7Ls` | `ANLCKQlYqhd4xfWhbxwJdi4XLDTaWz2HoivkB4V0SkkAwzO3Y4IuGbbI_yrPJmbns94-VXU3hqnagDI3kQS35Xy2hcoukvpEF2LdlUM-kF0` | Roadmap and compatibility context |
| SD-DOC-035 | Drive workspace record `1JyNgEJjEgDvYqJfr0Ukadvk0MtH9DX0R2q8VeaiLQMw` | `ANLCKQnIDCEnbsNh7440LgWFBXmohbcP5uK__9NEiZc6iLUfAA_kypUuywr_tcWAXLU_oit0-371-LSmFSWV7KpcXnzf5nuwj6rqSQZg8ps` | V2 workflow migration context |

## Stable acceptance IDs

- `REQ-CATALOG`: one canonical catalog generates package and marketplace metadata.
- `REQ-FAMILY`: Studio plus the eight named satellites build from that catalog;
  legacy IDs remain available as compatibility aliases.
- `REQ-PROTOCOL`: artifact, state, evidence, review, repair, and release schemas
  reject stale or self-accepting transitions.
- `REQ-RECOVERY`: `.project/session/active-plan.md`, `findings.md`, and
  `progress.md` survive a fresh process and are safe to initialize repeatedly.
- `REQ-CHATGPT`: the default archive is skills-first and declares no MCP server,
  localhost dependency, tunnel, or API key.
- `REQ-GATES`: writes, OAuth/account selection, custom-instruction changes,
  external artifacts, merge, and release remain human-gated.
- `REQ-PROOF`: direct repository/package evidence is distinguished from
  unproven ChatGPT, mobile, or external-host claims.
- `REQ-ROLLBACK`: local generated outputs and installation changes have bounded,
  reversible recovery instructions.

The exact current Drive revisions and any future changes must be refreshed by
the operator before a release review; these revision IDs are the read-time
audit pointers captured on 2026-08-30, not a substitute for live source
verification.
