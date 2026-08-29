# Contributing

Keep a change small and evidence-backed. Do not add a skill merely because a topic exists: identify its distinct failure mode, prove it is not covered, and add a routing case that would fail without it.

Before a pull request, run `python scripts/validate_suite.py` and `python scripts/run_evals.py`. Preserve source attribution in `THIRD_PARTY_SOURCES.md`; clean-room adaptation is preferred over copying.
