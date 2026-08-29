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

Every plugin contains portable Skills and an official `.codex-plugin/plugin.json` manifest. The six ChatGPT-facing bundles are skills-only: they do not require a tunnel, localhost, MCP server, OAuth, or a connected app. Web App Builder remains repository-oriented even when distributed as a skills-only bundle; Execution Guard remains Codex-gated because it governs Codex execution.

For ChatGPT uploads, run `python scripts/package_chatgpt_plugins.py`; it creates one plugin bundle per ChatGPT-facing plugin with its manifest, Skills, and icon. The bundle also includes a small upload wrapper so the same ZIP is accepted by ChatGPT's Skills uploader. Every generated bundle includes a mobile-safe PNG icon and has no tunnel dependency.

## Start here

Read [Architecture](ARCHITECTURE.md), then the [coordination contract](docs/plugin-coordination.md). The canonical repository is [github.com/Zodiac411/open-software-studio](https://github.com/Zodiac411/open-software-studio). Import the repository marketplace from `.agents/plugins/marketplace.json` in a supported workspace, use the Codex installation notes in [docs/install-codex.md](docs/install-codex.md), or upload the private ChatGPT bundles described in [docs/install-chatgpt.md](docs/install-chatgpt.md).

No third-party service, API, or subscription is required by this repository.

## Validation

```powershell
python scripts/validate_suite.py
python scripts/run_evals.py
```

The scripts use only Python's standard library. See `evals/RESULTS.md` for the recorded baseline.

## License

MIT. See [LICENSE](LICENSE).
