# Pilot B — brownfield

- Project: `PRJ-PILOT-B`
- Goal: preserve the existing billing formatter while correcting cents output.
- Non-goals: currency conversion, localization, persistence, and UI.
- Requirement: `REQ-PILOT-B-001` — `format_cents(1234)` returns `"$12.34"`.
- Planted defect: the current formatter rounds to whole dollars.
- Review: the defect must be identified by an independent reviewer before repair.
