# Install Open Software Studio in ChatGPT

Open Software Studio's ChatGPT distribution is skills-only. The six
ChatGPT-facing plugin bundles contain their `.codex-plugin/plugin.json`, all
specialist Skills, a small upload wrapper, and the matching icon. They do not
declare `mcpServers` or `apps`, and they do not need a tunnel, API key,
localhost service, OAuth, or a hosted endpoint.

The six uploadable bundles are:

- Project Architect
- Interface Studio
- Engineering Guard
- Research Engineer
- Project Docs
- Web App Builder

Execution Guard stays Codex-first. It is installed with the repository
marketplace and is not uploaded to ChatGPT as a ChatGPT-facing bundle.

## Build the six plugin bundles

From the repository root:

```powershell
python scripts/package_chatgpt_plugins.py
```

The ZIP files are written to `dist/chatgpt-plugins/`. Each ZIP contains the
plugin manifest, its `skills/` directory, a root upload wrapper, and a
`plugin-icon.png` referenced by `agents/openai.yaml`. The wrapper lets the
same plugin package pass through ChatGPT's Skills uploader while preserving
the full plugin layout for Codex and other Agent Skills clients.

## Upload in ChatGPT web

1. Open **Plugins** in the ChatGPT sidebar.
2. Open the **Skills** tab.
3. Choose **Create → Upload from your computer**.
4. Upload one ZIP from `dist/chatgpt-plugins/` at a time.
5. Wait for ChatGPT's security scan and install each accepted bundle.

ChatGPT currently displays these uploads in the Skills library. The package
itself remains a plugin bundle: Codex reads `.codex-plugin/plugin.json` and
loads the nested `skills/` directory. ChatGPT's current custom-app flow is a
separate MCP surface and is intentionally not used here.

## Icons

Every bundle has:

- `assets/plugin-icon.png` for the plugin manifest;
- `assets/plugin-icon.png` inside each nested Skill; and
- `agents/openai.yaml` entries with `icon_small` and `icon_large`.

The upload icon is a square true-color PNG below 10 KB. This avoids the blank
icon fallback seen when a Skill has no `agents/openai.yaml` metadata or when a
mobile client cannot decode the prior palette-only asset.

## Surface limits

Personal Skills must be installed separately on ChatGPT web and mobile; they
do not automatically sync from Codex. Mobile can use an installed Skill, but
it does not provide the same plugin/app management controls as ChatGPT web.
The six core workflows remain useful without shell access, localhost,
filesystem assumptions, or a local MCP server. Web App Builder's repository
implementation guidance is naturally most useful in Codex.

## Codex installation

Use the repository marketplace for the actual Codex plugins:

```powershell
codex plugin marketplace add .
codex plugin install open-software-studio/project-architect
```

Repeat installation for the other six plugins as needed. Execution Guard is
also installed here and supplies the global Codex discipline layer.

## Current OpenAI references

- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066)
- [Plugins package guide](https://developers.openai.com/plugins/build/plugins)
- [OpenAI plugin examples](https://github.com/openai/plugins)
