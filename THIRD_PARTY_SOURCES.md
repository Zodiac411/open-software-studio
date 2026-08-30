# Third-party sources

No third-party code or skill text is copied into this repository. The
following sources were selected by SD-DOC-034 and the existing source
register. Revisions are pinned to the read-time GitHub `HEAD` observed on
2026-08-30. Methods are clean-room adaptations; copied files are none.

| Project | Repository / pinned revision | License | Concept used | Copying / attribution |
|---|---|---|---|---|
| OpenAI Plugins | `openai/plugins` `1e285826e604f66f7208f7ac4dba0fe8341d1f57` | MIT | manifest, marketplace, skill folder conventions | no code/text copied; retain attribution here |
| Ponytail | `DietrichGebert/ponytail` `2ed6c52c9d7e5e56942508591085fd45dea277d3` | MIT | necessity and reuse ladder | clean-room adaptation only |
| GitHub Spec Kit | `github/spec-kit` `51e52be6c3b26fed3ff5424c671f4a559519a759` | MIT | specification-to-plan convergence | clean-room adaptation only |
| OpenSpec | `Fission-AI/OpenSpec` `a0ddb60d040c61f4907436a9d91310934b1dda63` | MIT | current truth versus active change | clean-room adaptation only |
| Agent_Do | `Mekawey0/Agent_Do` `4c0ecbe4403520bb24c7c8ff64c8092bfc50db42` | MIT | file-backed coordination and bounded handoff | clean-room adaptation only |
| agent-handoff | `WillowRyu/agent-handoff` `6179248b0a644cc8695f9f9dedd883587c4d4378` | MIT | plan/execute/verify separation | clean-room adaptation only |
| gstack | `garrytan/gstack` `07b59e396c6be5a86619a43151cb9ed62a15ae69` | MIT | focused review workflow ideas | clean-room adaptation only |
| codex-skills-kit | `TAKEOFF69/codex-skills-kit` `51645ad29d63fbbb301e42d8497c4fe80e09bac9` | MIT code; CC BY 4.0 skill/example/fixture content | seeded proof and closeout concepts | no source content copied; attribution retained |
| Planning with Files | `OthmanAdi/planning-with-files` `d5d35e6a2316459418e7381faa2682b2894d02c1` | MIT | plan/findings/progress recovery and doctor | mapped into `.project`; no second task system |
| GitHub Awesome Copilot | `github/awesome-copilot` `f11a4e441c5ff061b4f8ae37952be8c602e4034e` | MIT | evidence-first codebase mapping and issue planning | selected concepts only |
| Business Analysis Skills | `45ck/business-analysis-skills` `4eedd98f84c7546d56ea6aab077e3846767e758a` | MIT | requirement quality lenses | reimplemented as internal lenses |
| PM Skills | `phuryn/pm-skills` `18468a95b427e70e258b51389796367c6f684e7d` | MIT | assumption, outcome, pre-mortem, and red-team lenses | selected concepts only |
| Agent Skills | `neurofoo/agent-skills` `0e7ac2aa4d094352a082ebeedf1dbb4c52b77782` | MIT | reasoning lens selection | selected concepts only |
| Prove It | `Pablo-aps/prove-it` `4c5a6426a620019239b094f8cd0721ee25af59d4` | Apache-2.0 | adversarial completion verdict | clean-room adaptation only |
| Penpot | `penpot/penpot` `2ce202c7d85afc524829e3b666a44dffa8d51f13` | MPL-2.0 | optional open design-tool adapter candidate | not bundled |
| Storybook | `storybookjs/storybook` `8256cee6c95cf35dc8113cf179c9b7bea487f327` | MIT | optional component evidence candidate | not bundled |
| Playwright | `microsoft/playwright` `de214f440b7e34937fe4886f046b78b757136087` | Apache-2.0 | browser-verification guidance | not bundled |
| SearXNG | `searxng/searxng` `d226b78bc4c9ab93a84849b8ad128a68c41be17c` | AGPL-3.0 | optional self-hosted research candidate | not bundled |
| shadcn/ui | `shadcn-ui/ui` `683a5a9b370acdb7785a0529434e6a3b8c7e0441` | MIT | registry-first reuse order | not bundled |
| Addy Osmani Agent Skills | `addyosmani/agent-skills` `d2c37ef6225dd8726cdd369a8030307f48592d26` | MIT | source/incremental/context/debug/review concepts | clean-room adaptation only |
| Backlog.md | `MrLesk/Backlog.md` `3d73793b96e3a200411e21675f9adc95338267de` | MIT | optional portable task projection | not enabled in V2 core |
| Beads | `gastownhall/beads` `cbfc505e39a60514c57dcdb5afe155c8659647ba` | MIT | optional dependency graph adapter | not enabled for Lite or Standard |
| Symphony | `openai/symphony` `8001b52e3062495a16e520e4ceaf8f9de868c4d0` | Apache-2.0 | optional autonomous execution adapter | not enabled in V2 core |
| GitHub MCP Server | `github/github-mcp-server` `febc3293a4feb70e62399f39a26b082f78b9b176` | MIT | optional portable GitHub adapter | not bundled when native tooling is available |
| Blackline Agent Skills | `BlacklineCloud/agent-skills` `6a95391ad5f0a398c33f14d5aeb902bb1f9d13c0` | MIT | canonical source and generated marketplace patterns | clean-room adaptation only |

“Reviewed” is evidence-scoped: it does not endorse or require an upstream
project. Studio bundles no upstream files. Optional adapters remain disabled
by default and must be independently licensed, pinned, and reviewed before
activation.
