# Architecture

Open Software Studio separates decisions from execution:

```text
Research Engineer -> evidence
Project Architect -> product and technical decisions
Interface Studio -> experience decisions
Project Docs -> portable linked artifacts
Web App Builder -> repository implementation
Engineering Guard -> independent critique
Execution Guard -> how Codex works throughout
```

Each plugin has a light router and a few specialist skills. A router selects one specialist by default, two only when the request crosses a real boundary, and never loads its full methodology speculatively. `shared/` is the only cross-plugin contract: plugins communicate through Markdown artifacts and stable IDs, not hidden conversation state.

Execution Guard is deliberately not a planner or implementation framework. Its `pragmatic-core` and `prove-it` gate govern execution; Web App Builder owns the implementation workflow.
