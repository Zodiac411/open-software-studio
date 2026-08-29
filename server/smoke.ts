import { spawn, spawnSync } from "node:child_process";

const port = 8792;
const child = spawn("bun", ["run", "server/index.ts", "--port", String(port)], {
  stdio: ["ignore", "pipe", "pipe"],
});

const stop = () => {
  if (child.killed || child.exitCode !== null) return;
  if (process.platform === "win32" && child.pid) {
    spawnSync("taskkill", ["/PID", String(child.pid), "/T", "/F"], { stdio: "ignore" });
  } else {
    child.kill();
  }
};
process.on("exit", stop);
process.on("SIGINT", () => { stop(); process.exit(130); });

await new Promise((resolve) => setTimeout(resolve, 700));
const health = await fetch(`http://127.0.0.1:${port}/healthz`);
if (!health.ok) throw new Error(`healthz returned ${health.status}`);
const healthBody = await health.json() as { plugins?: unknown[] };
if (!Array.isArray(healthBody.plugins) || healthBody.plugins.length !== 7) {
  throw new Error("healthz did not list all seven plugins");
}

const initialize = await fetch(`http://127.0.0.1:${port}/mcp`, {
  method: "POST",
  headers: { "content-type": "application/json", accept: "application/json, text/event-stream" },
  body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "open-software-studio-smoke", version: "0.1.0" } } }),
});
if (!initialize.ok) throw new Error(`MCP initialize returned ${initialize.status}: ${await initialize.text()}`);
const sessionId = initialize.headers.get("mcp-session-id");
if (!sessionId) throw new Error("MCP initialize did not return mcp-session-id");

const tools = await fetch(`http://127.0.0.1:${port}/mcp`, {
  method: "POST",
  headers: { "content-type": "application/json", accept: "application/json, text/event-stream", "mcp-session-id": sessionId },
  body: JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} }),
});
if (!tools.ok) throw new Error(`MCP tools/list returned ${tools.status}: ${await tools.text()}`);
const toolsBody = await tools.text();
for (const name of ["project_architect_plan", "interface_studio_spec", "engineering_guard_review", "research_engineer_brief", "project_docs_pack", "web_app_builder_brief", "execution_guard_check"]) {
  if (!toolsBody.includes(name)) throw new Error(`${name} missing from tools/list`);
}

console.log("PASS: MCP health, initialization, and execution-guard tool discovery");
stop();
