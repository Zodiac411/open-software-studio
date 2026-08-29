# Artifact contract

Artifacts are plain Markdown. Use the smallest useful document set; a small project usually needs `PROJECT.md`, `SPEC.md`, and `IMPLEMENTATION-PLAN.md`, not an empty file for every category.

Every significant record may include this frontmatter:

```yaml
id: ADR-001
type: decision
status: accepted
owner: product
sources: [research/react-state-2026-08.md]
links: { requirements: [REQ-002], tasks: [TASK-004] }
verification: verified
supersedes: []
superseded_by: []
updated: 2026-08-29
```

Stable prefixes: `REQ`, `ADR`, `UX`, `COMP`, `TASK`, `RISK`, and `TEST`. A link is optional unless it is needed to justify a decision or verify work.
