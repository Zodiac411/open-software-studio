# Studio V2 version-metadata handoff

- work_package: `WP-SD-VERSION-METADATA`
- implementation_checkpoint_sha: `17e9407569eb642e11d86def752c22ae6b638337`
- branch: `studio-v2-bootstrap`
- allowed_paths: `scripts/build_studio.py`, `scripts/validate_studio.py`, generated package outputs, ChatGPT package outputs, and setup receipts
- change: expose the canonical suite version as `Studio v2.0.0` in generated package descriptions and enforce the label in validation
- evidence: two deterministic builds; `validate_studio.py`; `validate_suite.py`; `run_evals.py`; fresh ChatGPT Skills UI; fresh `@Studio` routing chat; fresh safe write-gate chat
- reviewer_action: inspect the generator diff, current SHA, regenerated archives, validators, and package hashes before reading the executor conclusion
- next_action: rerun fresh remote ChatGPT Review against the published implementation checkpoint and current evidence-only tip
