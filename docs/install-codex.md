# Install Studio V2 in Codex

The generated local marketplace is `.agents/plugins/marketplace.json`. Build
and validate it before installation:

```powershell
python scripts/build_studio.py
python scripts/validate_suite.py
python scripts/run_evals.py
```

Inspect the installed CLI on the target host, then use its current syntax:

```powershell
codex plugin marketplace add <path-to-this-repository>
codex plugin add studio-delivery@studio-v2
codex plugin list -m studio-v2
```

The umbrella package is `studio-delivery`, displayed as `Studio`. Satellite
packages are generated from the same catalog. The seven pre-V2 package IDs are
kept as compatibility packages until independent parity review is complete;
do not remove them automatically.

The platform config is `~/.studio/config.yaml` (on Windows,
`%USERPROFILE%/.studio/config.yaml`) and contains only non-secret defaults:

```yaml
default_profile: standard
default_archetype: auto
review_mode: fresh_context
auto_merge: false
permission_posture: ask_before_writes
open_source_only: true
prefer_free: true
```

For a repository project, use the file-backed control plane:

```powershell
python scripts/studio.py --project . init
python scripts/studio.py --project . status
python scripts/studio.py --project . doctor
```

`studio.py` validates mechanics only. Meaning, scope, implementation, and
acceptance remain human/agent responsibilities; the executor cannot accept or
merge its own work.
