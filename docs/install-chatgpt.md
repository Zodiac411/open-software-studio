# Install in ChatGPT

Current OpenAI workspace documentation allows administrators to import a GitHub marketplace and configure plugin/app access. Import `https://github.com/Zodiac411/open-software-studio` (the repository root, where `.agents/plugins/marketplace.json` is present), then set installation policy for eligible users.

The first five plugins are skills-only. They neither require nor declare apps/MCP servers, so their core workflows are usable without local tooling. Availability still depends on plan, workspace, role, region, and the surface. Apps are optional enhancements outside this suite; installing a plugin never grants provider access.

Authoritative current references: [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex/) and [Importing and syncing plugin marketplaces from GitHub](https://help.openai.com/en/articles/20001504).
