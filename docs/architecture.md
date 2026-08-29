# Detailed architecture

The current OpenAI plugin implementation is authoritative for format: `.codex-plugin/plugin.json` is required; `skills/` is the only declared surface in this suite. `.app.json` references an existing app by ID and `.mcp.json` declares MCP servers; neither is required here. Plugin-level `agents/`, `commands/`, `hooks.json`, and `assets/` are optional companion surfaces. Current validator guidance warns against unsupported `hooks` manifest fields, so no manifest declares it.

Marketplace `policy.products: ["CODEX"]` is used only for Web App Builder and Execution Guard, matching the current `openai/plugins` examples. The suite uses current skills-only plugins elsewhere to avoid the documented Desktop only risk associated with declared MCP servers.

Source references: [openai/plugins](https://github.com/openai/plugins) at `1e285826e604f66f7208f7ac4dba0fe8341d1f57` and [OpenAI plugin marketplace import guidance](https://help.openai.com/en/articles/20001504).
