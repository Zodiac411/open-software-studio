---
name: incremental-build
description: Split multi-file or risky implementation into falsifiable, verifiable slices.
---
# Incremental build

Use for multi-file work, migrations, features, or risky patches. Define the smallest vertical slice, implement it, run the decisive check, inspect the result, and only then expand. Keep each slice tied to a requirement.

Do not use to inflate trivial edits. Exit with evidence from an early slice or a localized blocker. Reject: “one big patch is faster” when an assumption can be cheaply falsified first.
