# Studio V2 architecture

Studio V2 is one catalog-generated workflow exposed through an umbrella package
and eight focused satellites. The packages share versioned artifacts and
project-local state; they do not depend on hidden conversation history.

```text
Studio Plan     -> scope, requirements, architecture, bounded plans
Studio Design   -> experience, interaction, accessibility, visual system
Studio Research -> current external evidence and source quality
Studio Docs     -> durable artifacts, IDs, traceability, and handoffs
Studio Review   -> independent findings, acceptance, and repair gates
Studio Build    -> approved repository implementation
Studio Verify   -> execution discipline and direct proof
Studio Track    -> confirmation-gated GitHub projections
Studio          -> routing and the complete bounded delivery loop
```

`catalog/studio.yaml` owns package identity, routing inventory, artifact
versions, profiles, archetypes, recipes, and source provenance. The build
renders the Codex marketplace, ChatGPT skills-first archive, schemas,
templates, icons, and evaluation fixtures deterministically.

`.project/` is the portable workflow authority. Requirements, snapshots, work
packages, evidence, findings, reviews, repairs, and release receipts bind to
explicit identifiers and Git revisions. GitHub and Google Drive are external
projections or evidence sources; neither silently overrides local state.

All external writes require confirmation. Review is independent of execution,
release requires a current accepted review, and Studio never merges
automatically.

The seven pre-V2 package directories remain compatibility sources. Their
specialist skills may be reused by V2 packages, but this document and
`docs/studio-v2.md` define the current architecture.
