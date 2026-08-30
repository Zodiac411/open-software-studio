#!/usr/bin/env python3
"""Small, fail-closed mechanics for the Studio V2 file-backed control plane."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "studio.yaml"
TRANSITIONS = ROOT / "schemas" / "v2" / "state-transitions.json"
RESULTS = ["PASS", "PASS_WITH_LIMITATIONS", "BLOCKED", "NOT_RUN", "UNPROVEN"]
PHASES = ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"]
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]+$")


def fail(message: str, result: str = "BLOCKED") -> int:
    print(json.dumps({"result": result, "message": message}, sort_keys=True))
    return 2 if result == "BLOCKED" else 0


def emit(result: str, message: str, **values: Any) -> int:
    if result not in RESULTS:
        raise ValueError(result)
    print(json.dumps({"result": result, "message": message, **values}, indent=2, sort_keys=True))
    return 2 if result == "BLOCKED" else 0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def project_root(value: str) -> Path:
    return Path(value).expanduser().resolve()


def control_root(project: Path) -> Path:
    return project / ".project"


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str, overwrite: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(value, encoding="utf-8", newline="\n")


def git(project: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True, check=False)
    except OSError:
        return None
    if proc.returncode:
        return None
    return proc.stdout.strip()


def current_sha(project: Path) -> str | None:
    return git(project, "rev-parse", "HEAD")


def require_state(project: Path) -> tuple[Path, dict[str, Any]] | None:
    path = control_root(project) / "state.json"
    if not path.is_file():
        return None
    try:
        return path, read_json(path)
    except ValueError:
        return None


def save_state(path: Path, state: dict[str, Any], project: Path, **updates: Any) -> None:
    state.update(updates)
    state["updated_at"] = utc_now()
    live = current_sha(project)
    if live:
        state["current_sha"] = live
    write_json(path, state)


def init_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    control = control_root(project)
    state_path = control / "state.json"
    if state_path.exists():
        missing = [name for name in ("active-plan.md", "findings.md", "progress.md") if not (control / "session" / name).is_file()]
        if missing:
            return fail(f"existing Studio state is incomplete; missing recovery files: {', '.join(missing)}")
        return emit("PASS_WITH_LIMITATIONS", "Studio project already initialized; existing state was preserved", project=str(project), changed=False, next_action="read .project/session/active-plan.md")

    project_id = args.project_id.upper()
    if not ID_PATTERN.fullmatch(project_id):
        return fail("project id must be an uppercase stable identifier")
    profile = args.profile
    archetype = args.archetype
    sha = current_sha(project)
    state = {
        "schema": "studio.state/v2",
        "project_id": project_id,
        "profile": profile,
        "archetype": archetype,
        "phase": "INTAKE",
        "status": "PASS",
        "active_wp": None,
        "current_sha": sha,
        "snapshot_id": None,
        "next_action": "shape the request and record non-goals before implementation",
        "blocking_items": [],
        "proof": [{"level": "E2", "observed": "Studio control plane initialized by scripts/studio.py init"}],
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    control.mkdir(parents=True, exist_ok=True)
    write_json(control / "project.yaml", {
        "schema": "studio.project/v2",
        "project_id": project_id,
        "profile": profile,
        "archetype": archetype,
        "authorities": {"repository": str(project), "machine_state": ".project", "human_task_view": "GitHub Issues/Milestones (confirmation-gated)"},
        "non_goals": ["automatic merge", "automatic release", "unconfirmed external writes"],
    })
    write_json(state_path, state)
    for directory in ("session", "snapshots", "work-packages", "evidence", "handoffs", "reviews", "repairs", "artifacts", "tracking"):
        (control / directory).mkdir(parents=True, exist_ok=True)
    write_text(control / "session" / "active-plan.md", "# Active Studio plan\n\n<!-- STUDIO-RECOVERY: initialized; replace with the approved plan. -->\n\n- Phase: INTAKE\n- Next action: shape the request and record non-goals.\n", overwrite=False)
    write_text(control / "session" / "findings.md", "# Studio findings\n\n<!-- STUDIO-RECOVERY: append typed findings; do not use this file as acceptance. -->\n", overwrite=False)
    write_text(control / "session" / "progress.md", "# Studio progress\n\n<!-- STUDIO-RECOVERY: append observed progress and evidence only. -->\n", overwrite=False)
    write_text(control / "events.jsonl", "", overwrite=False)
    return emit("PASS", "Studio project initialized", project=str(project), project_id=project_id, current_sha=sha, next_action=state["next_action"])


def load_catalog() -> dict[str, Any]:
    value = json.loads(CATALOG.read_text(encoding="utf-8"))
    if value.get("schema") != "studio.catalog/v2":
        raise ValueError("catalog schema is not studio.catalog/v2")
    return value


def doctor(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    checks: list[dict[str, Any]] = []

    def check(name: str, okay: bool, detail: str) -> None:
        checks.append({"name": name, "result": "PASS" if okay else "BLOCKED", "detail": detail})

    try:
        catalog = load_catalog()
        check("catalog", catalog.get("suite", {}).get("version") == "2.0.0", "catalog/studio.yaml")
        check("catalog-family", len(catalog.get("plugins", [])) == 9, "nine generated plugin entries")
        check("schemas", (ROOT / "schemas" / "v2" / "state-transitions.json").is_file(), "schemas/v2")
        check("marketplace", json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")).get("name") == "studio-v2", "generated marketplace")
        chatgpt = ROOT / "dist" / "chatgpt" / "studio.zip"
        check("chatgpt-archive", chatgpt.is_file() and chatgpt.stat().st_size > 0, "dist/chatgpt/studio.zip")
        check("icons", all((ROOT / "brand/icon-system/generated" / f"studio-delivery-{size}.png").is_file() for size in (24, 32, 64, 128, 256, 512)), "Opal Seed raster sizes")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(f"doctor could not inspect generated Studio state: {exc}")

    state = require_state(project)
    if state is None:
        checks.append({"name": "project-state", "result": "NOT_RUN", "detail": "no .project/state.json in target directory; fail-open outside Studio projects"})
    else:
        _, value = state
        live = current_sha(project)
        check("project-state", value.get("schema") == "studio.state/v2", ".project/state.json")
        check("sha-freshness", not live or value.get("current_sha") in (None, live), f"state={value.get('current_sha')} live={live}")
        check("recovery-files", all((control_root(project) / "session" / name).is_file() for name in ("active-plan.md", "findings.md", "progress.md")), ".project/session")
    blocked = [item for item in checks if item["result"] == "BLOCKED"]
    return emit("BLOCKED" if blocked else "PASS", "Studio doctor completed", checks=checks, next_action="repair the named check" if blocked else "read the active project state before acting")


def plan_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio plan")
    state_path, state = pair
    if state.get("phase") not in ("INTAKE", "SHAPED", "PLANNED"):
        return fail(f"cannot plan from phase {state.get('phase')}; use the current next action")
    wp_path = control_root(project) / "work-packages" / "WP-001.json"
    if not wp_path.exists():
        sha = current_sha(project)
        write_json(wp_path, {
            "schema": "studio.artifact/v2",
            "document_id": "WP-001",
            "project_id": state["project_id"],
            "wp_id": "WP-001",
            "status": "PLANNED",
            "snapshot_id": None,
            "base_sha": sha,
            "primary_outcome": "Complete one bounded Studio proof slice.",
            "requirements": ["REQ-CATALOG", "REQ-PROTOCOL"],
            "allowed_paths": ["scripts/", "catalog/", "schemas/", "skills/", "templates/"],
            "forbidden_paths": [".codex/", "secrets/", "credentials/"],
            "scope_budget": {"primary_outcomes": 1, "subsystems": 3, "new_dependencies": 0},
            "acceptance": ["named validators pass", "independent review is fresh and non-self-accepting"],
            "verification": [{"level": "E2", "command": "python scripts/validate_studio.py"}],
            "non_goals": ["merge", "release", "unapproved external writes"],
            "stop_conditions": ["base SHA changes", "new dependency is required", "scope budget is exceeded"],
            "rollback": "review bootstrap/ROLLBACK.md",
            "handoff_requirements": ["base SHA", "head SHA", "diff", "commands", "limitations", "reviewer action"],
        })
    save_state(state_path, state, project, phase="PLANNED", status="PASS", active_wp="WP-001", next_action="review and freeze WP-001")
    return emit("PASS", "bounded work package is planned", work_package=str(wp_path), next_action="studio freeze --approved-by <owner>")


def freeze_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init and studio plan before studio freeze")
    if not args.approved_by:
        return fail("freezing requires an explicit owner approval label")
    state_path, state = pair
    if state.get("phase") != "PLANNED":
        return fail(f"freeze requires PLANNED state, found {state.get('phase')}")
    sha = current_sha(project)
    if not sha:
        return fail("freeze requires a Git repository HEAD")
    snapshot = {"schema": "studio.snapshot/v2", "snapshot_id": "SNAP-001", "project_id": state["project_id"], "base_sha": sha, "status": "FROZEN", "approved_by": args.approved_by, "created_at": utc_now()}
    write_json(control_root(project) / "snapshots" / "SNAP-001.json", snapshot)
    wp_path = control_root(project) / "work-packages" / "WP-001.json"
    if wp_path.is_file():
        wp = read_json(wp_path)
        wp.update({"status": "FROZEN", "snapshot_id": "SNAP-001", "base_sha": sha})
        write_json(wp_path, wp)
    save_state(state_path, state, project, phase="FROZEN", status="PASS", snapshot_id="SNAP-001", next_action="compile a fresh context capsule")
    return emit("PASS", "snapshot frozen", snapshot_id="SNAP-001", base_sha=sha, approved_by=args.approved_by, next_action="studio context")


def context_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio context")
    state_path, state = pair
    if state.get("phase") not in ("FROZEN", "IMPLEMENTING", "PROVING", "REPAIR"):
        return fail(f"context requires a frozen or active work package, found {state.get('phase')}")
    wp_path = control_root(project) / "work-packages" / f"{state.get('active_wp', 'WP-001')}.json"
    if not wp_path.is_file():
        return fail("active work package is missing")
    wp = read_json(wp_path)
    capsule = "\n".join([
        "# Studio context capsule",
        "",
        f"- Project: `{state['project_id']}`",
        f"- Work package: `{wp.get('wp_id')}`",
        f"- Snapshot: `{state.get('snapshot_id')}`",
        f"- Current SHA: `{current_sha(project)}`",
        f"- Active goal: {wp.get('primary_outcome')}",
        f"- Requirements: {', '.join(wp.get('requirements', []))}",
        f"- Allowed paths: {', '.join(wp.get('allowed_paths', []))}",
        f"- Forbidden paths: {', '.join(wp.get('forbidden_paths', []))}",
        f"- Acceptance: {'; '.join(wp.get('acceptance', []))}",
        f"- Stop conditions: {'; '.join(wp.get('stop_conditions', []))}",
        "",
        "Read `.project/session/findings.md` and `.project/session/progress.md` before acting. Do not merge or self-accept.",
        "",
    ])
    write_text(control_root(project) / "session" / "context-capsule.md", capsule)
    save_state(state_path, state, project, phase="IMPLEMENTING", status="PASS", next_action="implement only the active work package")
    return emit("PASS", "fresh context capsule compiled", path=str(control_root(project) / "session" / "context-capsule.md"), next_action=state["next_action"])


def validate_work_package(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    path = project_root(args.path) if args.path else control_root(project) / "work-packages" / "WP-001.json"
    if not path.is_file():
        return fail(f"work package not found: {path}", "NOT_RUN")
    try:
        value = read_json(path)
    except ValueError as exc:
        return fail(str(exc))
    required = ["document_id", "project_id", "wp_id", "status", "base_sha", "primary_outcome", "requirements", "allowed_paths", "forbidden_paths", "scope_budget", "acceptance", "verification", "non_goals", "stop_conditions", "rollback", "handoff_requirements"]
    missing = [key for key in required if key not in value]
    if missing:
        return fail(f"work package missing fields: {', '.join(missing)}")
    if not isinstance(value["requirements"], list) or len(value["requirements"]) == 0 or value["scope_budget"].get("primary_outcomes") != 1:
        return fail("work package must have requirements and one primary outcome")
    state_pair = require_state(project)
    if state_pair and value.get("snapshot_id") and value.get("base_sha") != state_pair[1].get("current_sha"):
        return fail("frozen work package base SHA does not match project state")
    return emit("PASS", "work package mechanics are valid", path=str(path), wp_id=value["wp_id"], base_sha=value["base_sha"])


def add_evidence(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before adding evidence")
    evidence_id = args.evidence_id.upper()
    if not re.fullmatch(r"EVID-[A-Z0-9-]+", evidence_id):
        return fail("evidence id must match EVID-...")
    value = {"schema": "studio.evidence/v2", "document_id": evidence_id, "evidence_id": evidence_id, "project_id": pair[1]["project_id"], "requirement": args.requirement, "level": args.level, "command_or_probe": args.command_or_probe, "observed": args.observed, "timestamp": utc_now(), "limitations": args.limitations}
    path = control_root(project) / "evidence" / f"{evidence_id}.json"
    if path.exists() and not args.replace:
        return fail(f"evidence already exists; use --replace only for this named local receipt")
    write_json(path, value)
    return emit("PASS", "evidence receipt recorded", path=str(path), evidence_id=evidence_id, level=args.level)


def validate_evidence(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    root = control_root(project) / "evidence"
    files = sorted(root.glob("*.json")) if root.is_dir() else []
    if not files:
        return emit("NOT_RUN", "no project evidence receipts exist", next_action="record named evidence before claiming completion")
    required = ["evidence_id", "requirement", "level", "command_or_probe", "observed", "timestamp", "limitations"]
    errors: list[str] = []
    for path in files:
        try:
            value = read_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        errors.extend(f"{path.name}: missing {key}" for key in required if not value.get(key))
        if value.get("level") not in {f"E{index}" for index in range(6)}:
            errors.append(f"{path.name}: evidence level must be E0 through E5")
    if errors:
        return fail("; ".join(errors))
    return emit("PASS", "evidence receipts are mechanically valid", count=len(files), levels=sorted({read_json(path)["level"] for path in files}))


def compile_artifact(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    try:
        catalog = load_catalog()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(str(exc))
    artifact_type = args.artifact_type.upper()
    specs = catalog.get("artifact_templates", {})
    if artifact_type not in specs:
        return fail(f"unknown artifact type: {artifact_type}")
    data: dict[str, Any] = {}
    if args.data:
        try:
            data = read_json(project_root(args.data))
        except ValueError as exc:
            return fail(str(exc))
    required = specs[artifact_type]["required_fields"]
    missing = [key for key in required if key not in data]
    if missing:
        return fail(f"artifact data missing fields: {', '.join(missing)}")
    template = ROOT / "templates" / "studio-v2" / f"{artifact_type.lower()}.md"
    if not template.is_file():
        return fail(f"generated template missing: {template}")
    output = project_root(args.output) if args.output else control_root(project) / "artifacts" / f"{artifact_type.lower()}.md"
    try:
        output.relative_to(project)
    except ValueError:
        return fail("artifact output must remain inside the project directory")
    lines = ["---", "schema: studio.artifact/v2", f"artifact_type: {artifact_type}", "status: DRAFT", "version: 2.0", "---", f"# {artifact_type}", "", "## Compiled fields", ""]
    lines.extend(f"- `{key}`: {json.dumps(data[key], ensure_ascii=False, sort_keys=True)}" for key in required)
    lines.extend(["", "## Template guidance", "", template.read_text(encoding="utf-8")])
    write_text(output, "\n".join(lines).rstrip() + "\n")
    sidecar = output.with_suffix(".json")
    write_json(sidecar, {"schema": "studio.artifact-instance/v2", "artifact_type": artifact_type, "version": "2.0", "data": data})
    return emit("PASS", "artifact compiled from the catalog template", markdown=str(output), sidecar=str(sidecar), artifact_type=artifact_type)


def handoff_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio handoff")
    state_path, state = pair
    sha = current_sha(project)
    if not sha:
        return fail("handoff requires a Git HEAD")
    wp_id = state.get("active_wp") or "WP-001"
    snapshot_path = control_root(project) / "snapshots" / f"{state.get('snapshot_id', 'SNAP-001')}.json"
    snapshot = read_json(snapshot_path) if snapshot_path.is_file() else {}
    diff = git(project, "diff", "--stat") or "clean or unavailable"
    review_id = f"HANDOFF-{sha[:12].upper()}"
    value = {"schema": "studio.handoff/v2", "document_id": review_id, "wp_id": wp_id, "base_sha": snapshot.get("base_sha"), "head_sha": sha, "branch": git(project, "branch", "--show-current"), "claimed_outcomes": ["current repository state is packaged for independent review"], "files": [line.strip() for line in diff.splitlines() if line.strip()], "commands": ["python scripts/build_studio.py", "python scripts/validate_studio.py", "python scripts/run_evals.py"], "evidence": [{"level": "E2", "observed": "handoff generated from live Git state"}], "scope_delta": {"status": "REVIEW_REQUIRED"}, "unproven": ["fresh ChatGPT installation and review", "mobile availability", "external write smoke test"], "next_action": "independent fresh-context review", "reviewer_action": "inspect requirements, current SHA, diff, CI/runtime evidence before this conclusion", "created_at": utc_now()}
    path = control_root(project) / "handoffs" / f"{review_id}.json"
    write_json(path, value)
    write_text(path.with_suffix(".md"), "# Studio implementation handoff\n\n" + "\n".join(f"- {key}: `{json.dumps(value[key], ensure_ascii=False)}`" for key in ("wp_id", "head_sha", "branch", "next_action", "reviewer_action")) + "\n")
    save_state(state_path, state, project, phase="IN_REVIEW", status="PASS_WITH_LIMITATIONS", next_action="independent fresh-context review")
    return emit("PASS_WITH_LIMITATIONS", "implementation handoff generated; acceptance remains independent", path=str(path), head_sha=sha, next_action=state["next_action"])


def latest_json(root: Path, prefix: str) -> Path | None:
    files = sorted(root.glob(f"{prefix}*.json")) if root.is_dir() else []
    return files[-1] if files else None


def transition_allowed(source: str, target: str) -> bool:
    transitions = read_json(TRANSITIONS).get("transitions", {})
    return target in transitions.get(source, [])


def validate_review(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    path = project_root(args.path) if args.path else latest_json(control_root(project) / "reviews", "REV-")
    if not path or not path.is_file():
        return emit("NOT_RUN", "no independent review receipt exists", next_action="run a fresh reviewer")
    try:
        value = read_json(path)
    except ValueError as exc:
        return fail(str(exc))
    errors: list[str] = []
    if value.get("reviewer_role", "").lower() == "executor" or value.get("reviewer_context", "").lower() in {"same session", "executor session"}:
        errors.append("executor or same-session review cannot accept work")
    live = current_sha(project)
    if live and value.get("reviewed_head_sha") != live:
        errors.append(f"review is stale: reviewed {value.get('reviewed_head_sha')} but live HEAD is {live}")
    if not value.get("independent_checks"):
        errors.append("review must name independent checks")
    if value.get("disposition") not in {"ACCEPT", "REPAIR", "BLOCKED"}:
        errors.append("review disposition must be ACCEPT, REPAIR, or BLOCKED")
    if value.get("disposition") == "ACCEPT" and any(finding.get("severity") == "BLOCKING" for finding in value.get("findings", [])):
        errors.append("review with a BLOCKING finding cannot ACCEPT")
    if errors:
        return fail("; ".join(errors))
    return emit("PASS", "independent review receipt is mechanically valid", path=str(path), disposition=value["disposition"])


def validate_repair(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    path = project_root(args.path) if args.path else latest_json(control_root(project) / "repairs", "REPAIR-")
    if not path or not path.is_file():
        return emit("NOT_RUN", "no repair package exists", next_action="create one only for an accepted finding")
    try:
        value = read_json(path)
    except ValueError as exc:
        return fail(str(exc))
    required = ["repair_id", "accepted_findings", "allowed_paths", "forbidden_paths", "required_behavior", "regression_proof", "evidence", "non_goals", "repair_budget", "stop_conditions"]
    missing = [key for key in required if not value.get(key)]
    if missing:
        return fail(f"repair package missing fields: {', '.join(missing)}")
    return emit("PASS", "bounded repair package is mechanically valid", path=str(path), repair_id=value["repair_id"])


def close_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio close")
    state_path, state = pair
    handoffs = sorted((control_root(project) / "handoffs").glob("*.json"))
    if not handoffs:
        return fail("close requires an implementation handoff")
    phase = state.get("phase")
    if phase == "IN_REVIEW":
        review = latest_json(control_root(project) / "reviews", "REV-")
        if not review:
            return fail("close requires a current independent ACCEPT review")
        value = read_json(review)
        live = current_sha(project)
        if value.get("disposition") != "ACCEPT" or value.get("reviewed_head_sha") != live:
            return fail("close requires a current independent ACCEPT review")
        if not transition_allowed("IN_REVIEW", "ACCEPTED") or not transition_allowed("ACCEPTED", "CLOSED"):
            return fail("state transition matrix does not permit review acceptance and close")
        phase = "ACCEPTED"
    elif phase not in ("ACCEPTED", "CLOSED"):
        return fail(f"close requires ACCEPTED or CLOSED state, found {phase}")
    if phase == "ACCEPTED" and not transition_allowed("ACCEPTED", "CLOSED"):
        return fail("state transition matrix does not permit close")
    progress = control_root(project) / "session" / "progress.md"
    existing = progress.read_text(encoding="utf-8") if progress.is_file() else "# Studio progress\n"
    marker = f"\n- Session close observed at {utc_now()}; next action remains independent acceptance or release approval.\n"
    if marker not in existing:
        write_text(progress, existing.rstrip() + marker)
    save_state(state_path, state, project, phase="CLOSED", status="PASS_WITH_LIMITATIONS", next_action="validate independent review and obtain release approval")
    return emit("PASS_WITH_LIMITATIONS", "session closed with acceptance and release still gated", next_action=state["next_action"])


def release_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio release")
    if not args.approved_by:
        return fail("release requires explicit owner approval")
    state = pair[1]
    if state.get("phase") != "CLOSED":
        return fail(f"release requires CLOSED state, found {state.get('phase')}")
    review = latest_json(control_root(project) / "reviews", "REV-")
    if not review:
        return fail("release requires an independent review")
    value = read_json(review)
    live = current_sha(project)
    if value.get("disposition") != "ACCEPT" or value.get("reviewed_head_sha") != live:
        return fail("release requires a current independent ACCEPT review")
    state_path = pair[0]
    save_state(state_path, state, project, phase="RELEASED", status="PASS", next_action="maintain the released revision")
    return emit("PASS", "release gate validated; no publish or merge was performed", approved_by=args.approved_by, revision=live)


def track_plan(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio track")
    state = pair[1]
    wp = control_root(project) / "work-packages" / f"{state.get('active_wp', 'WP-001')}.json"
    if not wp.is_file():
        return fail("tracking requires an active work package")
    value = read_json(wp)
    plan = {"schema": "studio.github-projection/v2", "authority": ".project", "confirmation_required": True, "repository": "Zodiac411/open-software-studio", "milestone": {"title": f"Studio V2 / {state['project_id']}", "action": "create-or-reconcile only after explicit approval"}, "issues": [{"title": f"{value['wp_id']}: {value['primary_outcome']}", "labels": ["studio", "work-package"], "body": {"requirements": value["requirements"], "acceptance": value["acceptance"], "base_sha": value["base_sha"]}}], "writes_performed": False}
    path = control_root(project) / "tracking" / "github-plan.json"
    write_json(path, plan)
    if args.apply:
        return fail("external GitHub reconciliation is confirmation-gated; review .project/tracking/github-plan.json and approve the exact writes")
    return emit("PASS_WITH_LIMITATIONS", "GitHub milestone and issue reconciliation plan generated; no external write performed", path=str(path), next_action="obtain explicit approval before applying the exact plan")


def status_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return emit("NOT_RUN", "target is not initialized as a Studio project", next_action="studio init")
    _, state = pair
    live = current_sha(project)
    if live and state.get("current_sha") not in (None, live):
        return emit("BLOCKED", "project state is stale against the live repository", state=state, live_sha=live, next_action="refresh context and review the SHA change")
    return emit(state.get("status", "UNPROVEN"), "current Studio state", phase=state.get("phase"), active_wp=state.get("active_wp"), current_sha=live or state.get("current_sha"), next_action=state.get("next_action"), blocking_items=state.get("blocking_items", []))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--project", default=".", help="project root containing .project")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    init = commands.add_parser("init")
    init.add_argument("--project-id", default="PRJ-STUDIO-LOCAL")
    init.add_argument("--profile", choices=("lite", "standard", "full"), default="standard")
    init.add_argument("--archetype", default="auto")
    commands.add_parser("status")
    commands.add_parser("plan")
    freeze = commands.add_parser("freeze")
    freeze.add_argument("--approved-by")
    commands.add_parser("context")
    wp = commands.add_parser("wp")
    wp_sub = wp.add_subparsers(dest="wp_command", required=True)
    wp_validate = wp_sub.add_parser("validate")
    wp_validate.add_argument("--path")
    evidence = commands.add_parser("evidence")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    evidence_validate = evidence_sub.add_parser("validate")
    add = evidence_sub.add_parser("add")
    add.add_argument("--evidence-id", required=True)
    add.add_argument("--requirement", required=True)
    add.add_argument("--level", required=True, choices=tuple(f"E{index}" for index in range(6)))
    add.add_argument("--command-or-probe", dest="command_or_probe", required=True)
    add.add_argument("--observed", required=True)
    add.add_argument("--limitations", default="")
    add.add_argument("--replace", action="store_true")
    artifact = commands.add_parser("artifact")
    artifact_sub = artifact.add_subparsers(dest="artifact_command", required=True)
    compile_parser = artifact_sub.add_parser("compile")
    compile_parser.add_argument("--type", dest="artifact_type", required=True)
    compile_parser.add_argument("--data")
    compile_parser.add_argument("--output")
    commands.add_parser("handoff")
    review = commands.add_parser("review")
    review_sub = review.add_subparsers(dest="review_command", required=True)
    review_validate = review_sub.add_parser("validate")
    review_validate.add_argument("--path")
    repair = commands.add_parser("repair")
    repair_sub = repair.add_subparsers(dest="repair_command", required=True)
    repair_validate = repair_sub.add_parser("validate")
    repair_validate.add_argument("--path")
    commands.add_parser("close")
    release = commands.add_parser("release")
    release.add_argument("--approved-by")
    track = commands.add_parser("track")
    track.add_argument("--apply", action="store_true")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "doctor": return doctor(args)
        if args.command == "init": return init_project(args)
        if args.command == "status": return status_project(args)
        if args.command == "plan": return plan_project(args)
        if args.command == "freeze": return freeze_project(args)
        if args.command == "context": return context_project(args)
        if args.command == "wp": return validate_work_package(args)
        if args.command == "evidence": return add_evidence(args) if args.evidence_command == "add" else validate_evidence(args)
        if args.command == "artifact": return compile_artifact(args)
        if args.command == "handoff": return handoff_project(args)
        if args.command == "review": return validate_review(args)
        if args.command == "repair": return validate_repair(args)
        if args.command == "close": return close_project(args)
        if args.command == "release": return release_project(args)
        if args.command == "track": return track_plan(args)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        return fail(str(exc))
    return fail("unknown Studio command")


if __name__ == "__main__":
    raise SystemExit(main())
