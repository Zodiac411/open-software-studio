# Pilot A — greenfield

- Project: `PRJ-PILOT-A`
- Goal: return a deterministic greeting from a trimmed display name.
- Non-goals: persistence, networking, localization, and UI.
- Requirement: `REQ-PILOT-A-001` — `greeting(" Ada ")` returns `"Hello, Ada!"`.
- Proof: E2 unit command and a fresh Studio handoff.
- Review: independent fresh context; executor cannot accept.
