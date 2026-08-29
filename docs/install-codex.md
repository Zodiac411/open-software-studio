# Install in Codex

Use the repository marketplace at `.agents/plugins/marketplace.json`. Its entries resolve `./plugins/<name>` relative to this repository. Web App Builder and Execution Guard are explicitly product-gated to `CODEX`; the other five are not.

Validate after checkout:

```powershell
python scripts/validate_suite.py
```

For every substantive Codex task, enable Execution Guard, then enable the domain plugin needed for the task. “Always use” means always route through its small router—not load every skill.
