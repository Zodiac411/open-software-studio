---
name: test-for-behavior
description: Design or review tests that prove user-observable behavior rather than implementation shape.
---
# Test for behavior

Use when behavior changes or a regression guard is required. Identify the observable contract and the defect a test must detect. Prefer existing targeted tests; add at most a focused main path and critical failure case when existing coverage misses the change. Demonstrate sensitivity where practical.

Do not add test infrastructure or mirror private implementation. Exit with the behavior and evidence each test proves. Reject: “the test passes” when it would also pass with the defect.
