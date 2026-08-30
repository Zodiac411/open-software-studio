---
name: debug-root-cause
description: Stop speculative repair and localize an unexpected failure before another fix attempt.
---
# Debug root cause

Use immediately after unexpected behavior: **STOP -> PRESERVE -> REPRODUCE -> LOCALIZE -> HYPOTHESIZE -> TEST -> FIX -> GUARD -> VERIFY**. Change one causal variable where practical. After repeated failed hypotheses, reset assumptions and re-localize.

Do not stack fixes or delete failure evidence. Exit with reproduced evidence, causal rationale, and a verification result. Reject: “try this too” without a hypothesis.
