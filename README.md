# Open Software Studio

Open Software Studio is a small, open-source Studio V2 workflow for product
design, research, documentation, implementation, verification, and review. It
keeps decisions in portable Markdown, treats evidence as first-class, and
keeps execution discipline separate from implementation capability.

## Plugins

| Surface | Package | Owns |
|---|---|---|
| ChatGPT / Codex | Studio | complete bounded delivery loop |
| ChatGPT / Codex | Studio Plan | scope, requirements, architecture, plans |
| ChatGPT / Codex | Studio Design | UX, interaction, visual system |
| ChatGPT / Codex | Studio Research | current external evidence |
| ChatGPT / Codex | Studio Docs | durable artifacts and traceability |
| ChatGPT / Codex | Studio Review | independent critique and repair gates |
| ChatGPT / Codex | Studio Build | approved repository implementation |
| ChatGPT / Codex | Studio Verify | evidence-backed execution verification |
| ChatGPT / Codex | Studio Track | GitHub issue/milestone projection |

All generated packages are rendered from [`catalog/studio.yaml`](catalog/studio.yaml).
The generated Codex packages contain portable Skills and an official
`.codex-plugin/plugin.json` manifest. The default ChatGPT artifact is the
single skills-first [`dist/chatgpt/studio.zip`](dist/chatgpt/studio.zip): it
does not declare an MCP server or require localhost, a tunnel, an API key, or
a connected app. The seven pre-V2 package directories remain untouched as
compatibility sources until parity is accepted.

Run `python scripts/build_studio.py` to regenerate the package family,
templates, schemas, routing cases, and deterministic archives from the
checked-in Opal Seed assets. Run `python scripts/build_studio.py --render-icons`
only when the catalog's icon roles or palette change; review and commit the
resulting assets together. Run `python scripts/check_reproducibility.py` to
verify two isolated clean-checkout builds reproduce every repository byte.
`python scripts/validate_suite.py` runs the structural and reproducibility
gates.

## Start here

Read [Architecture](ARCHITECTURE.md), then the [coordination contract](docs/plugin-coordination.md).
The canonical repository is [github.com/Zodiac411/open-software-studio](https://github.com/Zodiac411/open-software-studio).
Import `.agents/plugins/marketplace.json` in Codex, use the V2 installation
notes in [docs/install-codex.md](docs/install-codex.md), or upload the default
skills-first archive described in [docs/install-chatgpt.md](docs/install-chatgpt.md).
The executable control plane is [scripts/studio.py](scripts/studio.py), and
the setup evidence is under [bootstrap](bootstrap/).

No third-party service, API, or subscription is required by this repository.

## Validation

```powershell
python scripts/validate_suite.py
python scripts/run_evals.py
```

The V2 validators use Python's standard library plus the already-installed
Pillow renderer for icons. See [THIRD_PARTY_SOURCES.md](THIRD_PARTY_SOURCES.md)
for pinned clean-room source references and [bootstrap/REQUIREMENTS.md](bootstrap/REQUIREMENTS.md)
for the governing Drive documents.

## License

MIT. See [LICENSE](LICENSE).
