import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { URL } from "node:url";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

type PluginDefinition = {
  slug: string;
  displayName: string;
  toolName: string;
  toolTitle: string;
  toolDescription: string;
  outputLabel: string;
  focus: string;
  nextSteps: string[];
};

const plugins: PluginDefinition[] = [
  {
    slug: "project-architect",
    displayName: "Project Architect",
    toolName: "project_architect_plan",
    toolTitle: "Create project architecture plan",
    toolDescription: "Turn a software idea into a scoped, traceable planning brief. Use when the user needs requirements, architecture, decisions, or implementation sequencing.",
    outputLabel: "planning brief",
    focus: "problem framing, requirements, architecture boundaries, decisions, risks, and executable sequencing",
    nextSteps: ["Clarify the problem, audience, constraints, non-goals, and unknowns.", "Produce stable requirement and decision IDs.", "Convert approved decisions into an implementation plan and bounded tasks."],
  },
  {
    slug: "interface-studio",
    displayName: "Interface Studio",
    toolName: "interface_studio_spec",
    toolTitle: "Create interface specification",
    toolDescription: "Turn requirements into implementation-ready UX and UI behavior. Use for flows, screen maps, components, responsive rules, accessibility, and visual QA.",
    outputLabel: "UX/UI specification",
    focus: "user flows, information architecture, screen states, interaction feedback, components, responsive behavior, and accessibility",
    nextSteps: ["Map relevant screens, views, panels, modals, routes, and states.", "Specify loading, empty, error, success, disabled, offline, keyboard, pointer, and touch behavior where relevant.", "Hand off DESIGN.md, SCREEN-MAP, COMPONENT-MAP, and a visual QA plan."],
  },
  {
    slug: "engineering-guard",
    displayName: "Engineering Guard",
    toolName: "engineering_guard_review",
    toolTitle: "Review engineering work",
    toolDescription: "Independently critique a plan, architecture, implementation, or verification report. Use when the user asks about engineering risk, readiness, correctness, or evidence.",
    outputLabel: "engineering review",
    focus: "requirement fit, architecture compliance, correctness, security, test quality, complexity, performance, accessibility, and agent legibility",
    nextSteps: ["Separate findings into BLOCKING, IMPORTANT, and OPTIONAL.", "Cite the artifact, file, or evidence behind each finding.", "Do not silently redesign the approved project or expand optional scope."],
  },
  {
    slug: "research-engineer",
    displayName: "Research Engineer",
    toolName: "research_engineer_brief",
    toolTitle: "Create evidence-backed research brief",
    toolDescription: "Plan current multi-source software ecosystem research. Use for technology, library, extension, framework, project-health, or community comparisons.",
    outputLabel: "research brief",
    focus: "current primary sources, repository health, releases, documentation, trade-offs, community evidence, maturity, and confidence",
    nextSteps: ["Search official documentation and project repositories first.", "Distinguish verified fact, strong evidence, inference, anecdote, and unknown.", "Record source dates, trade-offs, risks, maturity, and a recommendation."],
  },
  {
    slug: "project-docs",
    displayName: "Project Docs",
    toolName: "project_docs_pack",
    toolTitle: "Compile project documentation pack",
    toolDescription: "Compile decisions, evidence, designs, and plans into the smallest coherent set of durable Markdown artifacts and handoffs.",
    outputLabel: "documentation pack",
    focus: "artifact selection, source-of-truth ownership, stable IDs, traceability, synchronization, handoffs, and document audits",
    nextSteps: ["Select only the documents justified by project size and risk.", "Link requirements to decisions, UX, tasks, code, and verification evidence.", "Include a concise handoff with current state, decisions, files, constraints, unknowns, and next action."],
  },
  {
    slug: "web-app-builder",
    displayName: "Web App Builder",
    toolName: "web_app_builder_brief",
    toolTitle: "Prepare web-app implementation",
    toolDescription: "Prepare an approved web-app build for repository-native Codex implementation. Use for repo intake, bounded work packages, reuse, tests, browser verification, review, and handoff.",
    outputLabel: "implementation brief",
    focus: "repository intake, approved artifacts, local conventions, reuse order, bounded delegation, tests, runtime verification, review, and handoff",
    nextSteps: ["Read AGENTS.md and project artifacts before coding.", "Define a concrete definition of done and bounded work packages.", "Implement verified slices, run tests and browser checks, then request independent review."],
  },
  {
    slug: "execution-guard",
    displayName: "Execution Guard",
    toolName: "execution_guard_check",
    toolTitle: "Apply execution discipline",
    toolDescription: "Apply the always-used Codex discipline layer. Use for grounding, reuse, incremental execution, root-cause debugging, final review, proof, and honest completion status.",
    outputLabel: "execution gate",
    focus: "understand before acting, repository evidence, smallest correct change, scope discipline, incremental feedback, root-cause debugging, and completion proof",
    nextSteps: ["Apply pragmatic-core and inspect the current task phase and risk.", "Load only the specialist workflow justified by the phase; never load all guard guidance speculatively.", "Before completion, define, break down, verify, and return PROVEN, FAILED, NOT PROVEN, or BLOCKED."],
  },
];

const bySlug = new Map(plugins.map((plugin) => [plugin.slug, plugin]));

function resolvePlugin(pathname: string, explicit?: string): PluginDefinition | undefined {
  const slug = explicit ?? pathname.match(/^\/mcp\/([^/]+)\/?$/)?.[1];
  return slug ? bySlug.get(slug) : undefined;
}

function registerPluginTool(server: McpServer, plugin: PluginDefinition): void {
  server.registerTool(
    plugin.toolName,
    {
      title: plugin.toolTitle,
      description: plugin.toolDescription,
      inputSchema: {
        request: z.string().min(1).describe("The user's software-work request or artifact to process."),
        context: z.string().optional().describe("Optional project context, constraints, artifacts, or evidence supplied by the user."),
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    },
    async ({ request, context }) => {
      const contextNote = context?.trim() ? "Context supplied: yes." : "Context supplied: no; ask only decision-changing questions or request the missing artifact.";
      const text = [
        `${plugin.displayName} ${plugin.outputLabel}`,
        "",
        `Request received: ${request.trim()}`,
        contextNote,
        "",
        `Focus: ${plugin.focus}.`,
        "",
        "Recommended next steps:",
        ...plugin.nextSteps.map((step, index) => `${index + 1}. ${step}`),
        "",
        "This tool returns a routing and artifact contract. The bundled Skills remain the detailed workflow authority.",
      ].join("\n");

      return {
        content: [{ type: "text", text }],
        structuredContent: {
          plugin: plugin.slug,
          displayName: plugin.displayName,
          output: plugin.outputLabel,
          request: request.trim(),
          contextProvided: Boolean(context?.trim()),
          focus: plugin.focus,
          nextSteps: plugin.nextSteps,
        },
      };
    },
  );

}

function createPluginServer(plugin: PluginDefinition): McpServer {
  const server = new McpServer(
    { name: `open-software-studio-${plugin.slug}`, version: "2.0.0" },
    {
      instructions: `${plugin.displayName} is one bounded part of Open Software Studio. ${plugin.focus}. Keep the core workflow useful without proprietary SaaS or local filesystem assumptions; use the repository, user-provided context, and current primary evidence where available.`,
    },
  );
  registerPluginTool(server, plugin);
  return server;
}

function createStudioServer(): McpServer {
  const server = new McpServer(
    { name: "open-software-studio-compatibility", version: "2.0.0" },
    {
      instructions: "This optional Studio V2 compatibility server exposes the seven pre-V2 specialist tools. The skills-first Studio package remains the default workflow and does not require this server. Select one bounded compatibility tool, keep context minimal, require confirmation for writes, and report unverified work honestly.",
    },
  );
  for (const plugin of plugins) registerPluginTool(server, plugin);
  return server;
}

async function runStdio(pluginSlug: string): Promise<void> {
  const plugin = bySlug.get(pluginSlug);
  if (!plugin) throw new Error(`Unknown plugin: ${pluginSlug}`);
  const server = createPluginServer(plugin);
  await server.connect(new StdioServerTransport());
}

function writeJson(res: ServerResponse, status: number, body: unknown): void {
  const json = JSON.stringify(body);
  res.writeHead(status, { "content-type": "application/json; charset=utf-8", "content-length": Buffer.byteLength(json) });
  res.end(json);
}

async function runHttp(port: number): Promise<void> {
  const sessions = new Map<string, { transport: StreamableHTTPServerTransport; plugin?: PluginDefinition }>();
  const httpServer = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url ?? "/", `http://${req.headers.host ?? "127.0.0.1"}`);

    if (req.method === "GET" && (url.pathname === "/healthz" || url.pathname === "/readyz")) {
      writeJson(res, 200, { status: "ready", service: "open-software-studio", plugins: plugins.map(({ slug, displayName }) => ({ slug, displayName })) });
      return;
    }

    const isAggregate = url.pathname === "/mcp" || url.pathname === "/mcp/";
    if (!isAggregate && !url.pathname.startsWith("/mcp/")) {
      writeJson(res, 404, { error: "Use /mcp/<plugin-slug> for MCP or /healthz for readiness." });
      return;
    }

    const plugin = resolvePlugin(url.pathname);
    if (!plugin && !isAggregate) {
      writeJson(res, 404, { error: "Unknown plugin", plugins: plugins.map(({ slug }) => slug) });
      return;
    }

    const sessionId = req.headers["mcp-session-id"];
    if (typeof sessionId === "string" && sessions.has(sessionId)) {
      const session = sessions.get(sessionId)!;
      if (plugin && session.plugin && session.plugin.slug !== plugin.slug) {
        writeJson(res, 409, { error: "MCP session is bound to a different plugin path." });
        return;
      }
      await session.transport.handleRequest(req, res);
      return;
    }

    const server = plugin ? createPluginServer(plugin) : createStudioServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (id) => sessions.set(id, { transport, plugin }),
      onsessionclosed: (id) => sessions.delete(id),
    });

    res.on("close", () => {
      if (!res.writableEnded) void transport.close();
    });
    await server.connect(transport);
    await transport.handleRequest(req, res);
  });

  httpServer.listen(port, "127.0.0.1", () => {
    console.error(`Open Software Studio MCP ready on http://127.0.0.1:${port}`);
  });
}

const args = process.argv.slice(2);
const stdio = args.includes("--stdio");
const pluginIndex = args.indexOf("--plugin");
const pluginSlug = pluginIndex >= 0 ? args[pluginIndex + 1] : undefined;
const portIndex = args.indexOf("--port");
const port = portIndex >= 0 ? Number(args[portIndex + 1]) : Number(process.env.PORT ?? 8791);

if (stdio) {
  await runStdio(pluginSlug ?? "execution-guard");
} else {
  await runHttp(port);
}
