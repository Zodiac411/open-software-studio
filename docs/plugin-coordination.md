# Studio V2 coordination

| Request | Primary package | Boundary |
|---|---|---|
| Complete bounded delivery loop or ambiguous Studio request | Studio | Routes to focused packages; does not bypass their gates. |
| Product scope, requirements, architecture, or work packages | Studio Plan | Does not implement unapproved repository changes. |
| Experience, interaction, accessibility, or visual direction | Studio Design | Does not own repository delivery evidence. |
| Current tools, libraries, or ecosystem evidence | Studio Research | Does not turn evidence into an unapproved architecture decision. |
| Formal artifacts, stable IDs, traceability, or handoffs | Studio Docs | Does not invent missing decisions. |
| Independent risk, quality, or acceptance review | Studio Review | Must not implement or accept its own repair. |
| Approved repository implementation | Studio Build | Must not silently change frozen requirements or self-accept. |
| Grounding, debugging, tests, and completion proof | Studio Verify | Governs execution quality; does not own product scope. |
| GitHub issue and milestone projection | Studio Track | Plans read-only by default; writes require exact confirmation. |

When implementation discovers a requirements or architecture conflict, it
creates a typed change proposal rather than silently changing the frozen
decision. Studio Plan decides the change, Studio Docs records it, Studio Build
implements it, Studio Verify proves it, and a fresh Studio Review accepts or
rejects it at the current SHA.

The legacy Project Architect, Interface Studio, Research Engineer, Project
Docs, Engineering Guard, Web App Builder, and Execution Guard package IDs are
compatibility aliases for the corresponding V2 responsibilities.
