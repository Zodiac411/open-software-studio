---
name: artifact-selector
description: Choose the smallest document set needed to preserve a project's decisions and unblock implementation.
---
# Artifact selector

Classify the project and existing documents. Small: `PROJECT.md`, `SPEC.md`, `IMPLEMENTATION-PLAN.md`; medium adds requirements, architecture, design, tasks, test plan; complex adds API/data/ADRs/security/risks/runbook. Reuse and update an authoritative artifact instead of duplicating it.

Do not generate every possible file. Exit with rationale, source-of-truth locations, and absent-but-unneeded artifacts.
