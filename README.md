# Open Software Studio

Open Software Studio is a small, open-source suite of seven coordinated plugins for product design and implementation. It keeps decisions in portable Markdown, treats evidence as first-class, and keeps execution discipline separate from implementation capability.

## Plugins

| Surface | Plugin | Owns |
|---|---|---|
| ChatGPT / Codex | Project Architect | scope, requirements, architecture, plans |
| ChatGPT / Codex | Interface Studio | UX, interaction, visual system |
| ChatGPT / Codex | Engineering Guard | independent engineering critique |
| ChatGPT / Codex | Research Engineer | current external evidence |
| ChatGPT / Codex | Project Docs | durable artifacts and traceability |
| Codex | Web App Builder | repository implementation |
| Codex | Execution Guard | disciplined, evidence-backed execution |

The first five contain skills only: they retain useful core workflows without shell, localhost, filesystem, or a connected app. The last two are Codex-gated because they require repository work.

## Start here

Read [Architecture](ARCHITECTURE.md), then the [coordination contract](docs/plugin-coordination.md). The canonical repository is [github.com/Zodiac411/open-software-studio](https://github.com/Zodiac411/open-software-studio). Import the repository marketplace from `.agents/plugins/marketplace.json` in a supported workspace, or use the Codex installation notes in [docs/install-codex.md](docs/install-codex.md).

No third-party service, API, or subscription is required by this repository.

## Validation

```powershell
python scripts/validate_suite.py
python scripts/run_evals.py
```

The scripts use only Python's standard library. See `evals/RESULTS.md` for the recorded baseline.

## License

MIT. See [LICENSE](LICENSE).
