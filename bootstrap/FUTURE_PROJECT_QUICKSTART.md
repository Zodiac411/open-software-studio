# Future-project quickstart

Use this exact prompt when starting a new Studio project:

> Use Studio for this bounded software task.
>
> Repository: https://github.com/Zodiac411/open-software-studio
>
> Drive workspace: https://drive.google.com/drive/folders/1GDlSRW9aJVOvCH-fiZcWPQYsQcUNYGXe
>
> Goal: [one measurable outcome]
>
> Non-goals: [what must remain untouched]
>
> Constraints: [platform, budget, security, accessibility, deadline, and
> compatibility constraints]
>
> Start with a read-only preflight. Read the current Studio state if
> .project/project.yaml exists. Produce a project brief with goals, non-goals,
> assumptions, requirements, proof levels, acceptance criteria, stop
> conditions, and exactly one next action. Ask before writes, external
> changes, account selection, OAuth, permission changes, merge, or release.
>
> Use one bounded work package. Generate a handoff from actual repository
> state. Have a fresh independent reviewer inspect the requirements, current
> SHA, diff, CI/runtime evidence, and permissions before reading the executor
> conclusion. Record typed findings. Repair only accepted findings, rerun
> verification, and obtain a fresh review. Never self-accept or auto-merge.

## Local commands

From a project containing .project:

1. python scripts/studio.py doctor
2. python scripts/studio.py init --project-id PRJ-EXAMPLE
3. python scripts/studio.py plan
4. python scripts/studio.py freeze --approved-by owner
5. python scripts/studio.py context
6. python scripts/studio.py wp validate
7. python scripts/studio.py evidence add --evidence-id EVID-EXAMPLE-001 --requirement REQ-EXAMPLE --level E2 --command-or-probe "python test_app.py" --observed "named assertion passed" --limitations "local proof"
8. python scripts/studio.py evidence validate
9. python scripts/studio.py handoff
10. python scripts/studio.py review validate
11. python scripts/studio.py repair validate
12. python scripts/studio.py close

Use the Codex Studio package from the configured studio-v2 marketplace. The
ChatGPT artifact is the skills-first dist/chatgpt/studio.zip package. Do not
claim @Studio until the visible ChatGPT invocation surface proves it. If the
personal Skills route is used and plugin mentions are unavailable, invoke the
explicit Studio skill shown by the UI and record that exact invocation.

Keep all writes confirmation-gated. Do not store passwords, MFA codes,
recovery codes, cookies, OAuth tokens, or API keys in project state.
