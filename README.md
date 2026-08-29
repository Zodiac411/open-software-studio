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

Every plugin contains portable Skills and an official `.codex-plugin/plugin.json` manifest. The package also includes a small shared MCP service so one private ChatGPT app connection can expose the seven specialist tools; see [ChatGPT setup](docs/install-chatgpt.md). The first five keep useful core workflows without shell, localhost, filesystem, or a connected app. The last two remain Codex-gated because they require repository work.

## Start here

Read [Architecture](ARCHITECTURE.md), then the [coordination contract](docs/plugin-coordination.md). The canonical repository is [github.com/Zodiac411/open-software-studio](https://github.com/Zodiac411/open-software-studio). Import the repository marketplace from `.agents/plugins/marketplace.json` in a supported workspace, use the Codex installation notes in [docs/install-codex.md](docs/install-codex.md), or create the private ChatGPT app described in [docs/install-chatgpt.md](docs/install-chatgpt.md).

No third-party service, API, or subscription is required by this repository.

## Validation

```powershell
python scripts/validate_suite.py
python scripts/run_evals.py
```

The scripts use only Python's standard library. See `evals/RESULTS.md` for the recorded baseline.

## License

MIT. See [LICENSE](LICENSE).
