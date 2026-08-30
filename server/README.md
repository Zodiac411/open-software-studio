# Studio V2 optional compatibility MCP service

This service is an optional compatibility adapter for the seven pre-V2
specialist tools. It is not part of the default Studio V2 ChatGPT package,
does not replace the Studio umbrella or focused Skills, and is not required
for Codex, ChatGPT, localhost-free use, or mobile use. The default package is
`dist/chatgpt/studio.zip`.

Run it from the repository root:

```powershell
bun install
bun run mcp -- --port 8791
```

Endpoints:

- `GET /healthz` and `GET /readyz` — service and plugin inventory.
- `POST /mcp` — compatibility aggregate server with all seven legacy tools.
- `POST /mcp/<plugin-slug>` — one-plugin server for local integrations.

The default listener is loopback-only (`127.0.0.1:8791`). The server has no
built-in authentication and must not be exposed directly to the public
internet. Any separately approved remote deployment must add authentication
at its deployment boundary.

The tools accept a request and optional context and return a focused workflow
brief. They are intentionally small: the durable specialist behavior remains
in `plugins/*/skills/`, where it can be inspected, reviewed, and reused by
Codex. Studio V2 package identity and workflow ownership remain in
`catalog/studio.yaml`.
