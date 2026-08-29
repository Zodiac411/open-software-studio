# Open Software Studio MCP service

This service is the narrow integration layer for ChatGPT app connections. It
does not replace the seven Skills or decide which specialist should answer a
request; it exposes one read-only tool per plugin so a connected ChatGPT app
can route work to the same contracts.

Run it from the repository root:

```powershell
bun install
bun run mcp -- --port 8791
```

Endpoints:

- `GET /healthz` and `GET /readyz` — service and plugin inventory.
- `POST /mcp` — aggregate server with all seven tools.
- `POST /mcp/<plugin-slug>` — one-plugin server for local integrations.

The default listener is loopback-only (`127.0.0.1:8791`). Put a trusted HTTPS
tunnel in front of `/mcp` before connecting ChatGPT. The server has no built-in
authentication because authentication belongs at the tunnel or deployment
boundary; do not expose the loopback listener directly to the public internet.

The tools accept a request and optional context and return a focused workflow
brief. They are intentionally small: the durable specialist behavior remains
in `plugins/*/skills/`, where it can be inspected, reviewed, and reused by
Codex.
