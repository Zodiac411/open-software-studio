# Plugin coordination

| Request | Owner | Explicitly not owner |
|---|---|---|
| Current tools, libraries, or ecosystem evidence | Research Engineer | Project Architect |
| Product scope, requirements, or architecture | Project Architect | Interface Studio |
| Experience, screen behavior, accessibility, visual direction | Interface Studio | Web App Builder |
| Formal documents and linked handoffs | Project Docs | Project Architect |
| Independent risk/quality critique | Engineering Guard | Execution Guard |
| Repository implementation | Web App Builder | Execution Guard |
| Grounding, restraint, debugging discipline, completion evidence | Execution Guard | Web App Builder |

When an implementation discovers an architecture conflict, it creates an architecture-change request instead of silently changing the architecture. A Project Architect decision and Project Docs artifact unblock the builder.
