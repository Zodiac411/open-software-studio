# Studio V2 version-metadata handoff

- work_package: `WP-SD-VERSION-METADATA`
- head_sha: `55d4ab31c10d5ac22f0f3232bccd7d261fdea9b1`
- branch: `studio-v2-bootstrap`
- allowed_paths: `scripts/build_studio.py`, `scripts/validate_studio.py`, generated package outputs, ChatGPT package outputs, and setup receipts
- change: expose the canonical suite version as `Studio v2.0.0` in generated package descriptions and enforce the label in validation
- evidence: two deterministic builds; `validate_studio.py`; `validate_suite.py`; `run_evals.py`; fresh ChatGPT Skills UI; fresh `@Studio` routing chat; fresh safe write-gate chat
- reviewer_action: inspect the generator diff, current SHA, regenerated archives, validators, and package hashes before reading the executor conclusion
- next_action: publish the reviewed source checkpoint only after explicit owner approval, then rerun fresh remote ChatGPT Review
