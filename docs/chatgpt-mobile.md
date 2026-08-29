# ChatGPT web and mobile compatibility

**Verified from current OpenAI documentation:** plugins may be surface- or workspace-limited; their availability depends on plan, role, region, and capability. The documentation describes use in ChatGPT only where the relevant controls are available; it does not promise identical web and iOS installation/management flows.

**Design decision:** Project Architect, Interface Studio, Engineering Guard, Research Engineer, and Project Docs have useful skills-only core workflows. They do not assume shell access, localhost, a filesystem, MCP server, or desktop application.

**Limitation:** ChatGPT mobile/iOS access and plugin management are not verified as equivalent to web. Do not promise import, installation, @-mention controls, or admin settings parity on iOS; use the controls actually exposed by the account/surface. Codex-first plugins are not intended for mobile repository work.

Current product reference: [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex/).
