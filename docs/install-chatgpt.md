# Install Open Software Studio in ChatGPT

Open Software Studio now ships as seven official-format Codex plugins. Each
plugin contains its portable Skills plus an MCP descriptor; the seven
descriptors point at one small, open-source MCP service in `server/`.

The repository is the source package. A ChatGPT app connection is created in
your account because ChatGPT assigns the technical app ID. The checked-in
`.app.json` files intentionally contain an empty `apps` object until that
connection exists; the repository never invents or commits an app ID.

## 1. Start the shared MCP service

From the repository root:

```powershell
bun install
bun run mcp -- --port 8791
Invoke-RestMethod http://127.0.0.1:8791/readyz
```

The aggregate endpoint is `http://127.0.0.1:8791/mcp`. Per-plugin endpoints
are available at `/mcp/project-architect`, `/mcp/interface-studio`,
`/mcp/engineering-guard`, `/mcp/research-engineer`, `/mcp/project-docs`,
`/mcp/web-app-builder`, and `/mcp/execution-guard`.

## 2. Expose it through your Software studio tunnel

Keep the API key in your local environment only. Do not paste it into ChatGPT,
commit it, or put it in a repository file. With the repository service running,
start the tunnel client with your existing Software studio tunnel ID:

```powershell
$env:CONTROL_PLANE_API_KEY = "<your-runtime-key>"
$env:CONTROL_PLANE_TUNNEL_ID = "<your-software-studio-tunnel-id>"
tunnel-client run `
  --control-plane.tunnel-id $env:CONTROL_PLANE_TUNNEL_ID `
  --control-plane.api-key env:CONTROL_PLANE_API_KEY `
  --mcp.server-url http://127.0.0.1:8791/mcp `
  --health.listen-addr 127.0.0.1:8091
```

Then verify the tunnel client reports ready:

```powershell
Invoke-RestMethod http://127.0.0.1:8091/readyz
```

The repository also includes `scripts/start-chatgpt-tunnel.ps1`, which starts
the MCP service and tunnel together without writing the key to disk.

## 3. Create the private ChatGPT app

ChatGPT currently creates custom MCP apps from the web developer-mode flow:

1. Open **Settings → Apps & Connectors → Advanced settings** and enable
   **Developer mode** (the exact labels can vary by account rollout).
2. Open **Apps**, choose **Create app**, and enter a display name such as
   **Open Software Studio**.
3. Select **Tunnel**, choose **Software studio**, choose **No Auth** for this
   local tunnel, acknowledge the unreviewed-server warning, and create the
   private app.
4. Copy the technical ID shown for the created app. It has the form
   `plugin_asdk_app_...`.

Wire the real ID into all seven package descriptors:

```powershell
python scripts/wire_chatgpt_apps.py --id plugin_asdk_app_<actual-id>
python scripts/validate_suite.py
```

You can instead provide a JSON map to assign different app IDs:

```json
{
  "project-architect": "plugin_asdk_app_...",
  "interface-studio": "plugin_asdk_app_..."
}
```

```powershell
python scripts/wire_chatgpt_apps.py --map app-ids.json
```

After creation, the app appears under **Apps → Personal → Created by me**. The
single shared connection exposes the seven narrowly scoped MCP tools; the
portable Skills remain in each plugin folder for Codex and other supported
surfaces.

## iOS-compatible Skills

Custom MCP app creation and management is a web developer-mode capability, so
it should not be treated as an iOS installation path. To use the specialist
workflows on ChatGPT mobile, package the Skills and upload them from ChatGPT
web:

```powershell
python scripts/package_chatgpt_skills.py
```

The generated ZIPs are in `dist/chatgpt-skills/`. Upload one ZIP per Skill via
**Plugins → Skills → Create → Upload from your computer**, wait for scanning,
and install it. Each ZIP embeds its plugin's approved
`assets/plugin-icon.png` (square PNG, below 10 KB), which prevents the blank
icon fallback on mobile. Re-upload updated ZIPs after changing a Skill; Codex
plugin metadata and ChatGPT Skill uploads are separate installation surfaces.

## Surface limits

This is a private developer-mode app, not a public marketplace submission.
ChatGPT web currently supports creating and managing these custom MCP apps;
ChatGPT mobile can use only the capabilities that the current product rollout
exposes and does not provide the same developer-mode installation controls.
The first five plugins keep their core workflows usable without shell access,
localhost, a filesystem, or a local MCP server. Web App Builder and Execution
Guard remain Codex-first and require repository-capable Codex use for their
implementation workflows.

## Current OpenAI references

- [Plugins package guide](https://developers.openai.com/plugins/build/plugins)
- [Connect and test a plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Developer mode and full MCP connectors](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta)
- [OpenAI plugin examples](https://github.com/openai/plugins)
