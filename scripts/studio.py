#!/usr/bin/env python3
"""Small, fail-closed mechanics for the Studio V2 file-backed control plane."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from copy import deepcopy
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


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def schema_errors(value: Any, schema: dict[str, Any], location: str = "$") -> list[str]:
    """Validate the JSON Schema subset emitted by build_studio.py."""
    errors: list[str] = []
    expected = schema.get("type")
    expected_types = expected if isinstance(expected, list) else [expected] if isinstance(expected, str) else []
    if expected_types and not any(schema_type_matches(value, item) for item in expected_types):
        return [f"{location}: expected {' or '.join(expected_types)}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}")
    if isinstance(schema.get("enum"), list) and value not in schema["enum"]:
        errors.append(f"{location}: value is not in the allowed enum")
    if isinstance(value, str):
        if isinstance(schema.get("minLength"), int) and len(value) < schema["minLength"]:
            errors.append(f"{location}: string is too short")
        if isinstance(schema.get("pattern"), str) and not re.search(schema["pattern"], value):
            errors.append(f"{location}: value does not match {schema['pattern']}")
        if schema.get("format") == "date-time" and parse_timestamp(value) == 0.0:
            errors.append(f"{location}: expected an ISO date-time")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(schema.get("minimum"), (int, float)) and value < schema["minimum"]:
            errors.append(f"{location}: value is below minimum {schema['minimum']}")
    if isinstance(value, list):
        if isinstance(schema.get("minItems"), int) and len(value) < schema["minItems"]:
            errors.append(f"{location}: array has fewer than {schema['minItems']} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, item_schema, f"{location}[{index}]"))
    if isinstance(value, dict):
        properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
        required = schema.get("required") if isinstance(schema.get("required"), list) else []
        errors.extend(f"{location}.{key}: required field is missing" for key in required if key not in value)
        for key, item in value.items():
            child_schema = properties.get(key)
            if isinstance(child_schema, dict):
                errors.extend(schema_errors(item, child_schema, f"{location}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{location}.{key}: unknown field")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(schema_errors(item, schema["additionalProperties"], f"{location}.{key}"))
    prohibited = schema.get("not")
    if isinstance(prohibited, dict):
        alternatives = prohibited.get("anyOf") if isinstance(prohibited.get("anyOf"), list) else [prohibited]
        if any(not schema_errors(value, item, location) for item in alternatives if isinstance(item, dict)):
            errors.append(f"{location}: value matches a prohibited shape")
    alternatives = schema.get("anyOf")
    if isinstance(alternatives, list) and alternatives and not any(not schema_errors(value, item, location) for item in alternatives if isinstance(item, dict)):
        errors.append(f"{location}: value does not match any allowed shape")
    return errors


def document_schema_errors(value: dict[str, Any], schema_name: str) -> list[str]:
    path = ROOT / "schemas" / "v2" / f"{schema_name}.schema.json"
    if not path.is_file():
        return [f"schema is missing: {path}"]
    try:
        schema = read_json(path)
    except ValueError as exc:
        return [str(exc)]
    return schema_errors(value, schema)


def write_json(path: Path, value: Any) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str, overwrite: bool = True) -> None:
    if path.exists() and not overwrite:
        return
    atomic_write(path, value)


def atomic_write(path: Path, value: str) -> None:
    """Replace one file without exposing a partially-written document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_bundle(files: dict[Path, str]) -> None:
    """Commit related recovery files together and restore old bytes on failure."""
    originals = {path: path.read_bytes() if path.exists() else None for path in files}
    temporary_paths: dict[Path, Path] = {}
    try:
        for path, value in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
            temporary_path = Path(temporary)
            temporary_paths[path] = temporary_path
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(value)
                handle.flush()
                os.fsync(handle.fileno())
        for path, temporary in temporary_paths.items():
            os.replace(temporary, path)
    except Exception:
        for path, original in originals.items():
            if original is None:
                path.unlink(missing_ok=True)
            else:
                fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.restore.", suffix=".tmp", dir=path.parent)
                try:
                    with os.fdopen(fd, "wb") as handle:
                        handle.write(original)
                        handle.flush()
                        os.fsync(handle.fileno())
                    os.replace(temporary, path)
                finally:
                    if os.path.exists(temporary):
                        os.unlink(temporary)
        raise
    finally:
        for temporary in temporary_paths.values():
            if temporary.exists():
                temporary.unlink()


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


def dirty_paths(project: Path) -> list[str]:
    status = git(project, "status", "--porcelain=v1", "--untracked-files=all")
    dirty: list[str] = []
    for line in (status or "").splitlines():
        path = line[3:].replace("\\", "/") if len(line) > 3 else line
        paths = [item.strip(' "') for item in path.split(" -> ")]
        if paths and all(item == ".project" or item.startswith(".project/") for item in paths):
            continue
        if line.strip():
            dirty.append(line)
    return dirty


def source_sha(project: Path, state: dict[str, Any] | None = None) -> str | None:
    """Return the immutable checkpoint, retained for compatibility."""
    declared = state.get("source_checkpoint_sha") if state else None
    return declared or (state or {}).get("current_sha") or current_sha(project)


def live_head(project: Path) -> str | None:
    return current_sha(project)


def candidate_head(project: Path, state: dict[str, Any]) -> str | None:
    return state.get("release_candidate_sha") or state.get("live_head_sha") or state.get("current_sha") or live_head(project)


def sha_digest(values: Any) -> str:
    return hashlib.sha256(json.dumps(values, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def parse_timestamp(value: Any) -> float:
    if not isinstance(value, str):
        return 0.0
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def record_sequence(root: Path) -> int:
    highest = 0
    if root.is_dir():
        for path in root.glob("*.json"):
            try:
                sequence = read_json(path).get("sequence")
            except ValueError:
                continue
            if isinstance(sequence, int) and not isinstance(sequence, bool):
                highest = max(highest, sequence)
    return highest


def next_event_sequence(project: Path) -> int:
    path = control_root(project) / "events.jsonl"
    highest = 0
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                sequence = json.loads(line).get("sequence")
            except json.JSONDecodeError:
                continue
            if isinstance(sequence, int) and not isinstance(sequence, bool):
                highest = max(highest, sequence)
    return highest + 1


def render_active_plan(project: Path, state: dict[str, Any]) -> str:
    wp_id = state.get("active_wp") or "none"
    wp_path = control_root(project) / "work-packages" / f"{wp_id}.json"
    wp = read_json(wp_path) if wp_path.is_file() else {}
    requirements = wp.get("requirements", [])
    return "\n".join([
        "# Active project plan",
        "",
        "<!-- STUDIO-RECOVERY: generated from state.json and the active work package. -->",
        f"- Phase: {state.get('phase')}",
        f"- Status: {state.get('status')}",
        f"- Active work package: {wp_id}",
        f"- Live HEAD: {state.get('live_head_sha') or state.get('current_sha')}",
        f"- Source checkpoint: {state.get('source_checkpoint_sha')}",
        f"- Next action: {state.get('next_action')}",
        f"- Requirements: {', '.join(str(item) for item in requirements)}",
        "",
    ])


def render_context(project: Path, state: dict[str, Any]) -> str:
    wp_id = state.get("active_wp") or "WP-001"
    wp_path = control_root(project) / "work-packages" / f"{wp_id}.json"
    wp = read_json(wp_path) if wp_path.is_file() else {}
    return "\n".join([
        "# Project context capsule",
        "",
        f"- Project: `{state.get('project_id')}`",
        f"- Phase: `{state.get('phase')}`",
        f"- Work package: `{wp.get('wp_id', wp_id)}`",
        f"- Snapshot: `{state.get('snapshot_id')}`",
        f"- Live HEAD: `{state.get('live_head_sha') or state.get('current_sha')}`",
        f"- Active goal: {wp.get('primary_outcome', state.get('next_action'))}",
        f"- Requirements: {', '.join(str(item) for item in wp.get('requirements', []))}",
        f"- Allowed paths: {', '.join(str(item) for item in wp.get('allowed_paths', []))}",
        f"- Forbidden paths: {', '.join(str(item) for item in wp.get('forbidden_paths', []))}",
        f"- Acceptance: {'; '.join(str(item) for item in wp.get('acceptance', []))}",
        f"- Stop conditions: {'; '.join(str(item) for item in wp.get('stop_conditions', []))}",
        "",
        "Read `.project/session/findings.md` and `.project/session/progress.md` before acting. Do not merge or self-accept.",
        "",
    ])


def transition(project: Path, state_path: Path, state: dict[str, Any], event_type: str, extra_files: dict[Path, str] | None = None, **updates: Any) -> tuple[dict[str, Any], bool]:
    """Apply one idempotent state transition and refresh recovery projections."""
    next_state = deepcopy(state)
    next_state.update(updates)
    live = live_head(project)
    if live:
        next_state["live_head_sha"] = live
        next_state["current_sha"] = live
        next_state["release_candidate_sha"] = live
    next_state["updated_at"] = utc_now()
    next_state.setdefault("source_checkpoint_sha", state.get("source_checkpoint_sha") or state.get("current_sha"))
    target_phase = next_state.get("phase")
    already_applied = state.get("phase") == target_phase and all(state.get(key) == value for key, value in updates.items())
    if already_applied:
        return state, False

    sequence = next_event_sequence(project)
    event = {
        "schema": "studio.event/v2",
        "event_id": f"EVT-{sequence:06d}",
        "sequence": sequence,
        "type": event_type,
        "from_phase": state.get("phase"),
        "to_phase": next_state.get("phase"),
        "project_id": next_state.get("project_id"),
        "live_head_sha": live,
        "timestamp": next_state["updated_at"],
    }
    events_path = control_root(project) / "events.jsonl"
    existing_events = events_path.read_text(encoding="utf-8") if events_path.is_file() else ""
    progress_path = control_root(project) / "session" / "progress.md"
    existing_progress = progress_path.read_text(encoding="utf-8") if progress_path.is_file() else "# Project progress\n"
    progress_marker = f"<!-- STUDIO-EVENT: {event['event_id']} -->"
    if progress_marker not in existing_progress:
        existing_progress = existing_progress.rstrip() + f"\n\n{progress_marker}\n- State projection: phase={next_state.get('phase')} live_head={next_state.get('live_head_sha')}\n- {event_type}: {next_state.get('phase')} at {next_state.get('live_head_sha')}\n"
    files = {
        state_path: json.dumps(next_state, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        control_root(project) / "session" / "active-plan.md": render_active_plan(project, next_state),
        progress_path: existing_progress,
        events_path: existing_events + json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n",
    }
    context_path = control_root(project) / "session" / "context-capsule.md"
    if context_path.is_file():
        files[context_path] = render_context(project, next_state)
    if extra_files:
        files.update(extra_files)
    atomic_bundle(files)
    return next_state, True


def require_state(project: Path) -> tuple[Path, dict[str, Any]] | None:
    path = control_root(project) / "state.json"
    if not path.is_file():
        return None
    try:
        return path, read_json(path)
    except ValueError:
        return None


def save_state(path: Path, state: dict[str, Any], project: Path, **updates: Any) -> None:
    event_type = updates.pop("_event_type", "state.updated")
    extra_files = updates.pop("_extra_files", None)
    next_state, _ = transition(project, path, state, event_type, extra_files=extra_files, **updates)
    state.clear()
    state.update(next_state)


def init_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    control = control_root(project)
    state_path = control / "state.json"
    if state_path.exists():
        missing = [name for name in ("active-plan.md", "findings.md", "progress.md") if not (control / "session" / name).is_file()]
        if missing:
            return fail(f"existing Studio state is incomplete; missing recovery files: {', '.join(missing)}")
        return emit("PASS_WITH_LIMITATIONS", "Studio project already initialized; existing state was preserved", project=str(project), changed=False, next_action="read .project/session/active-plan.md")

    project_id = (args.project_id or f"PRJ-{re.sub(r'[^A-Za-z0-9]+', '-', project.name).strip('-')}").upper()
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
        "source_checkpoint_sha": sha,
        "live_head_sha": sha,
        "release_candidate_sha": sha,
        "current_sha": sha,
        "session_id": f"SESSION-{sha[:12].upper() if sha else project_id}",
        "snapshot_id": None,
        "next_action": "shape the request and record non-goals before implementation",
        "blocking_items": [],
        "proof": [{"level": "E2", "observed": "Studio control plane initialized by scripts/studio.py init"}],
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    control.mkdir(parents=True, exist_ok=True)
    project_metadata_path = control / "project.yaml"
    metadata = read_json(project_metadata_path) if project_metadata_path.is_file() else {}
    metadata.update({
        "schema": "studio.project/v2",
        "project_id": project_id,
        "profile": profile,
        "archetype": archetype,
        "authorities": {"repository": str(project), "machine_state": ".project", "human_task_view": "GitHub Issues/Milestones (confirmation-gated)"},
        "non_goals": metadata.get("non_goals", ["automatic merge", "automatic release", "unconfirmed external writes"]),
    })
    write_json(project_metadata_path, metadata)
    write_json(state_path, state)
    for directory in ("session", "snapshots", "work-packages", "evidence", "handoffs", "reviews", "repairs", "artifacts", "tracking"):
        (control / directory).mkdir(parents=True, exist_ok=True)
    write_text(control / "session" / "active-plan.md", render_active_plan(project, state), overwrite=False)
    write_text(control / "session" / "findings.md", "# Project findings\n\n<!-- STUDIO-RECOVERY: append typed findings; do not use this file as acceptance. -->\n", overwrite=False)
    write_text(control / "session" / "progress.md", f"# Project progress\n\n<!-- STUDIO-RECOVERY: append observed progress and evidence only. -->\n\n<!-- STUDIO-EVENT: EVT-000001 -->\n- State projection: phase=INTAKE live_head={sha}\n- project.initialized: INTAKE at {sha}\n", overwrite=False)
    write_text(control / "events.jsonl", json.dumps({"schema": "studio.event/v2", "event_id": "EVT-000001", "sequence": 1, "type": "project.initialized", "from_phase": None, "to_phase": "INTAKE", "project_id": project_id, "live_head_sha": sha, "timestamp": state["created_at"]}, sort_keys=True) + "\n", overwrite=False)
    return emit("PASS", "Studio project initialized", project=str(project), project_id=project_id, current_sha=sha, next_action=state["next_action"])


def load_catalog() -> dict[str, Any]:
    value = json.loads(CATALOG.read_text(encoding="utf-8"))
    if value.get("schema") != "studio.catalog/v2":
        raise ValueError("catalog schema is not studio.catalog/v2")
    return value


def projection_errors(project: Path, state: dict[str, Any]) -> list[str]:
    errors = [f"state schema: {issue}" for issue in document_schema_errors(state, "state")]
    expected_phase = str(state.get("phase"))
    expected_live = state.get("live_head_sha") or state.get("current_sha")
    active_plan = control_root(project) / "session" / "active-plan.md"
    if not active_plan.is_file():
        errors.append("active plan is missing")
    else:
        text = active_plan.read_text(encoding="utf-8")
        if f"- Phase: {expected_phase}" not in text:
            errors.append("active plan phase disagrees with state")
        if expected_live and f"- Live HEAD: {expected_live}" not in text:
            errors.append("active plan live HEAD disagrees with state")
    context = control_root(project) / "session" / "context-capsule.md"
    if context.is_file():
        context_text = context.read_text(encoding="utf-8")
        if expected_live and f"- Live HEAD: `{expected_live}`" not in context_text:
            errors.append("context capsule live HEAD disagrees with state")
        if f"- Phase: `{expected_phase}`" not in context_text:
            errors.append("context capsule phase disagrees with state")
    progress = control_root(project) / "session" / "progress.md"
    if not progress.is_file():
        errors.append("progress projection is missing")
    elif expected_live and f"- State projection: phase={expected_phase} live_head={expected_live}" not in progress.read_text(encoding="utf-8"):
        errors.append("progress projection disagrees with state")
    events = control_root(project) / "events.jsonl"
    if not events.is_file():
        errors.append("event log is missing")
    else:
        parsed = []
        for line in events.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                errors.append("event log contains invalid JSON")
                continue
            if isinstance(item, dict):
                errors.extend(f"event schema: {issue}" for issue in document_schema_errors(item, "event"))
            else:
                errors.append("event log entries must be objects")
            if isinstance(item, dict) and isinstance(item.get("sequence"), int):
                parsed.append(item)
        if not parsed:
            errors.append("event log contains no typed events")
        elif parsed[-1].get("to_phase") != state.get("phase") or parsed[-1].get("live_head_sha") != expected_live:
            errors.append("latest event disagrees with state")
    return errors


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
        checkpoint = source_sha(project, value)
        state_schema_issues = document_schema_errors(value, "state")
        check("project-state", not state_schema_issues, "; ".join(state_schema_issues) or ".project/state.json conforms to schemas/v2/state.schema.json")
        expected_live = value.get("live_head_sha") or value.get("current_sha")
        check("sha-freshness", not live or expected_live == live, f"state={expected_live} source_checkpoint={checkpoint} live={live}")
        check("release-candidate", not live or (value.get("release_candidate_sha") or expected_live) == live, f"candidate={value.get('release_candidate_sha')} live={live}")
        check("recovery-files", all((control_root(project) / "session" / name).is_file() for name in ("active-plan.md", "findings.md", "progress.md")), ".project/session")
        errors = projection_errors(project, value)
        check("recovery-coherence", not errors, "; ".join(errors) or "state, projections, and typed events agree")
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
    metadata = read_json(control_root(project) / "project.yaml") if (control_root(project) / "project.yaml").is_file() else {}
    context: dict[str, Any] = {"metadata": metadata, "artifacts": {}}
    artifact_root = control_root(project) / "artifacts"
    for artifact_path in sorted(artifact_root.glob("*.json")) if artifact_root.is_dir() else []:
        try:
            artifact = read_json(artifact_path)
        except ValueError:
            continue
        context["artifacts"][artifact.get("artifact_type", artifact_path.stem)] = artifact.get("data", artifact)
    brief = context["artifacts"].get("PROJECT_BRIEF", {})
    product = context["artifacts"].get("PRODUCT_SPEC", {})
    title = metadata.get("title") or brief.get("title") or project.name
    outcome = metadata.get("primary_outcome") or brief.get("primary_outcome") or brief.get("desired_outcome") or f"Deliver the approved outcome for {title}."
    requirements = metadata.get("requirements") or product.get("requirements") or brief.get("requirements") or ["REQ-001"]
    if not isinstance(requirements, list):
        requirements = [requirements]
    requirements = [str(item) for item in requirements]
    allowed_paths = metadata.get("allowed_paths") or (["src/", "tests/"] if (project / "src").is_dir() else ["."])
    forbidden_paths = metadata.get("forbidden_paths") or [".git/", ".project/secrets/"]
    verification = metadata.get("verification_commands") or product.get("verification") or ["git status --short"]
    if not isinstance(verification, list):
        verification = [verification]
    repository = metadata.get("repository") or metadata.get("repository_url") or git(project, "remote", "get-url", "origin") or str(project)
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
            "title": title,
            "repository": repository,
            "primary_outcome": outcome,
            "requirements": requirements,
            "allowed_paths": allowed_paths,
            "forbidden_paths": forbidden_paths,
            "scope_budget": {"primary_outcomes": 1, "subsystems": 1, "new_dependencies": 0},
            "acceptance": metadata.get("acceptance", ["the stated outcome is directly verified", "an independent current review accepts the result"]),
            "verification": [{"level": "E2", "command": str(command)} for command in verification],
            "non_goals": metadata.get("non_goals", ["merge", "release", "unconfirmed external writes"]),
            "stop_conditions": metadata.get("stop_conditions", ["base SHA changes", "scope budget is exceeded"]),
            "rollback": metadata.get("rollback", "restore the previous commit or project checkpoint"),
            "handoff_requirements": ["base SHA", "head SHA", "diff", "commands", "limitations", "reviewer action"],
            "implementer_actor_id": metadata.get("implementer_actor_id", "project-executor"),
            "implementer_session_id": state.get("session_id"),
            "requirement_digest": sha_digest(requirements),
        })
    save_state(state_path, state, project, _event_type="plan.created", phase="PLANNED", status="PASS", active_wp="WP-001", next_action="review and freeze WP-001")
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
    sha = live_head(project)
    if not sha:
        return fail("freeze requires a Git repository HEAD")
    if state.get("phase") == "FROZEN" and state.get("snapshot_id") == "SNAP-001":
        return emit("PASS", "snapshot already frozen", snapshot_id="SNAP-001", base_sha=sha, changed=False, next_action="compile a fresh context capsule")
    snapshot = {"schema": "studio.snapshot/v2", "snapshot_id": "SNAP-001", "project_id": state["project_id"], "base_sha": sha, "status": "FROZEN", "approved_by": args.approved_by, "created_at": utc_now()}
    write_json(control_root(project) / "snapshots" / "SNAP-001.json", snapshot)
    wp_path = control_root(project) / "work-packages" / "WP-001.json"
    if wp_path.is_file():
        wp = read_json(wp_path)
        wp.update({"status": "FROZEN", "snapshot_id": "SNAP-001", "base_sha": sha})
        write_json(wp_path, wp)
    save_state(state_path, state, project, _event_type="snapshot.frozen", phase="FROZEN", status="PASS", snapshot_id="SNAP-001", next_action="compile a fresh context capsule")
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
    if state.get("phase") == "IMPLEMENTING" and (control_root(project) / "session" / "context-capsule.md").is_file():
        live = live_head(project)
        expected = state.get("live_head_sha") or state.get("current_sha")
        contradictions = projection_errors(project, state)
        if live and live != expected:
            contradictions.append(f"state live HEAD {expected} does not match Git HEAD {live}")
        if contradictions:
            return fail("context capsule is stale: " + "; ".join(contradictions))
        return emit("PASS", "context capsule already current", path=str(control_root(project) / "session" / "context-capsule.md"), changed=False, next_action=state["next_action"])
    save_state(state_path, state, project, _event_type="context.compiled", phase="IMPLEMENTING", status="PASS", next_action="implement only the active work package")
    write_text(control_root(project) / "session" / "context-capsule.md", render_context(project, state))
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
    schema_issues = document_schema_errors(value, "work_package")
    if schema_issues:
        return fail("; ".join(schema_issues))
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
    head = live_head(project)
    value = {"schema": "studio.evidence/v2", "document_id": evidence_id, "evidence_id": evidence_id, "project_id": pair[1]["project_id"], "requirement": args.requirement, "level": args.level, "command_or_probe": args.command_or_probe, "observed": args.observed, "timestamp": utc_now(), "limitations": args.limitations or "No additional limitations recorded.", "sequence": record_sequence(control_root(project) / "evidence") + 1, "head_sha": head, "exit_code": args.exit_code, "environment": args.environment, "observed_output_digest": sha_digest(args.observed)}
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
    required = ["evidence_id", "requirement", "level", "command_or_probe", "observed", "timestamp", "limitations", "sequence", "head_sha", "exit_code", "observed_output_digest"]
    errors: list[str] = []
    for path in files:
        try:
            value = read_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        errors.extend(f"{path.name}: {issue}" for issue in document_schema_errors(value, "evidence_receipt"))
        errors.extend(f"{path.name}: missing {key}" for key in required if key not in value or value[key] in (None, ""))
        if not isinstance(value.get("sequence"), int) or isinstance(value.get("sequence"), bool):
            errors.append(f"{path.name}: sequence must be an integer")
        if not isinstance(value.get("exit_code"), int) or isinstance(value.get("exit_code"), bool):
            errors.append(f"{path.name}: exit_code must be an integer")
        if value.get("level") not in {f"E{index}" for index in range(6)}:
            errors.append(f"{path.name}: evidence level must be E0 through E5")
        live = live_head(project)
        if live and value.get("head_sha") != live:
            errors.append(f"{path.name}: evidence is stale for live HEAD {live}")
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
    schema_issues = document_schema_errors(data, artifact_type.lower())
    if schema_issues:
        return fail("artifact schema validation failed: " + "; ".join(schema_issues))
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
    sidecar_value = {"schema": "studio.artifact-instance/v2", "artifact_type": artifact_type, "version": "2.0", "data": data}
    write_json(sidecar, sidecar_value)
    yaml_sidecar = output.with_suffix(".yaml")
    write_text(yaml_sidecar, json.dumps(sidecar_value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    github_body = output.with_name(f"{output.stem}.github.md")
    write_text(github_body, "# " + artifact_type + "\n\n" + "\n".join(f"- **{key}**: {json.dumps(data[key], ensure_ascii=False, sort_keys=True)}" for key in required) + "\n")
    google_docs = output.with_name(f"{output.stem}.google-docs.json")
    write_json(google_docs, {"schema": "studio.google-docs-payload/v2", "title": artifact_type, "body_markdown": output.read_text(encoding="utf-8"), "source_artifact": str(sidecar.name)})
    return emit("PASS", "artifact compiled from the catalog template", markdown=str(output), sidecar=str(sidecar), yaml=str(yaml_sidecar), github_body=str(github_body), google_docs_payload=str(google_docs), artifact_type=artifact_type)


def command_observation(project: Path, command: str) -> dict[str, Any]:
    try:
        argv = shlex.split(command, posix=False)
        proc = subprocess.run(argv, cwd=project, capture_output=True, text=True, check=False, timeout=60)
        output = (proc.stdout + proc.stderr).strip()
        return {"command": command, "exit_code": proc.returncode, "observed": output[-2000:] or "(no output)", "output_digest": sha_digest(output)}
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return {"command": command, "exit_code": None, "observed": f"not executed: {exc}", "output_digest": sha_digest(str(exc))}


def handoff_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio handoff")
    state_path, state = pair
    sha = live_head(project)
    if not sha:
        return fail("handoff requires a Git HEAD")
    wp_id = state.get("active_wp") or "WP-001"
    snapshot_path = control_root(project) / "snapshots" / f"{state.get('snapshot_id', 'SNAP-001')}.json"
    snapshot = read_json(snapshot_path) if snapshot_path.is_file() else {}
    review_id = f"HANDOFF-{sha[:12].upper()}"
    existing_handoff = control_root(project) / "handoffs" / f"{review_id}.json"
    if state.get("phase") == "IN_REVIEW" and existing_handoff.is_file():
        return emit("PASS_WITH_LIMITATIONS", "implementation handoff is already current", path=str(existing_handoff), head_sha=sha, changed=False, next_action=state.get("next_action"))
    base_sha = snapshot.get("base_sha") or state.get("source_checkpoint_sha")
    committed_diff = git(project, "diff", "--stat", f"{base_sha}..{sha}") if base_sha else None
    committed_files = git(project, "diff", "--name-only", f"{base_sha}..{sha}") if base_sha else None
    dirty_diff = git(project, "diff", "--stat") or "clean"
    wp_path = control_root(project) / "work-packages" / f"{wp_id}.json"
    wp = read_json(wp_path) if wp_path.is_file() else {}
    commands = [item.get("command") for item in wp.get("verification", []) if isinstance(item, dict) and item.get("command")]
    observations = [command_observation(project, command) for command in commands]
    value = {"schema": "studio.handoff/v2", "document_id": review_id, "wp_id": wp_id, "base_sha": base_sha, "head_sha": sha, "branch": git(project, "branch", "--show-current"), "claimed_outcomes": [str(wp.get("primary_outcome", "current repository state is packaged for independent review"))], "files": [line.strip() for line in (committed_files or "").splitlines() if line.strip()], "committed_diff_stat": committed_diff or "clean or unavailable", "dirty_diff_stat": dirty_diff, "commands": commands, "evidence": observations, "scope_delta": {"status": "REVIEW_REQUIRED", "base_sha": base_sha, "head_sha": sha}, "unproven": ["independent fresh-context review", "unconfirmed external writes"], "next_action": "independent fresh-context review", "reviewer_action": "inspect requirements, current SHA, committed diff, dirty state, and observed validation results before this conclusion", "created_at": utc_now(), "sequence": record_sequence(control_root(project) / "handoffs") + 1}
    schema_issues = document_schema_errors(value, "implementation_handoff")
    if schema_issues:
        return fail("handoff schema validation failed: " + "; ".join(schema_issues))
    path = control_root(project) / "handoffs" / f"{review_id}.json"
    write_json(path, value)
    write_text(path.with_suffix(".md"), "# Studio implementation handoff\n\n" + "\n".join(f"- {key}: `{json.dumps(value[key], ensure_ascii=False)}`" for key in ("wp_id", "head_sha", "branch", "next_action", "reviewer_action")) + "\n")
    save_state(state_path, state, project, _event_type="handoff.created", phase="IN_REVIEW", status="PASS_WITH_LIMITATIONS", release_candidate_sha=sha, next_action="independent fresh-context review")
    return emit("PASS_WITH_LIMITATIONS", "implementation handoff generated; acceptance remains independent", path=str(path), head_sha=sha, next_action=state["next_action"])


def latest_json(root: Path, prefix: str) -> Path | None:
    candidates: list[tuple[tuple[int, float, str], Path]] = []
    for path in root.glob(f"{prefix}*.json") if root.is_dir() else []:
        try:
            value = read_json(path)
        except ValueError:
            continue
        sequence = value.get("sequence")
        typed_sequence = sequence if isinstance(sequence, int) and not isinstance(sequence, bool) else -1
        timestamp = parse_timestamp(value.get("created_at") or value.get("timestamp"))
        candidates.append(((typed_sequence, timestamp, path.name), path))
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def transition_allowed(source: str, target: str) -> bool:
    transitions = read_json(TRANSITIONS).get("transitions", {})
    return target in transitions.get(source, [])


def review_errors(project: Path, value: dict[str, Any], state: dict[str, Any] | None = None, require_accept: bool = False) -> list[str]:
    required_strings = ["document_id", "review_id", "reviewer_role", "reviewer_context", "reviewer_actor_id", "reviewer_session_id", "implementer_actor_id", "implementer_session_id", "reviewed_base_sha", "reviewed_head_sha", "wp_id", "requirements_digest"]
    required_lists = ["requirements", "independent_checks", "findings", "conditions", "artifact_ids"]
    errors = document_schema_errors(value, "independent_review")
    errors.extend(f"missing {key}" for key in required_strings if not isinstance(value.get(key), str) or not value[key].strip())
    errors.extend(f"{key} must be a list" for key in required_lists if not isinstance(value.get(key), list))
    if value.get("schema") != "studio.review/v2":
        errors.append("review schema must be studio.review/v2")
    if value.get("disposition") not in {"ACCEPT", "REPAIR", "BLOCKED"}:
        errors.append("review disposition must be ACCEPT, REPAIR, or BLOCKED")
    if not value.get("requirements"):
        errors.append("review must name requirements")
    if not value.get("independent_checks"):
        errors.append("review must name independent checks")
    if not isinstance(value.get("scope_delta"), dict):
        errors.append("scope_delta must be an object")
    if value.get("reviewer_actor_id") == value.get("implementer_actor_id"):
        errors.append("reviewer and implementer actor must differ")
    if value.get("reviewer_session_id") == value.get("implementer_session_id"):
        errors.append("reviewer and implementer session must differ")
    raw_role = value.get("reviewer_role")
    raw_context = value.get("reviewer_context")
    role = raw_role.lower() if isinstance(raw_role, str) else ""
    context = raw_context.lower() if isinstance(raw_context, str) else ""
    if any(token in role for token in ("executor", "implementer")) or any(token in context for token in ("same session", "implementation session", "executor session")):
        errors.append("reviewer provenance identifies the implementation actor or session")
    live = live_head(project)
    candidate = candidate_head(project, state or {}) if state else live
    if live and value.get("reviewed_head_sha") != live:
        errors.append(f"review is stale: reviewed {value.get('reviewed_head_sha')} but live HEAD is {live}")
    if candidate and value.get("reviewed_head_sha") != candidate:
        errors.append(f"review does not match release candidate {candidate}")
    if state and state.get("active_wp") != value.get("wp_id"):
        errors.append("review does not target the active work package")
    wp = control_root(project) / "work-packages" / f"{value.get('wp_id', '')}.json"
    if wp.is_file():
        work_package = read_json(wp)
        expected_digest = sha_digest(work_package.get("requirements", []))
        if value.get("requirements_digest") != expected_digest:
            errors.append("review requirements digest does not match the active work package")
        if value.get("requirements") != work_package.get("requirements"):
            errors.append("review requirements do not match the active work package")
        base = work_package.get("base_sha")
        if base and value.get("reviewed_base_sha") != base:
            errors.append("review base SHA does not match the active work package")
        expected_artifacts = value.get("artifact_ids")
        if expected_artifacts is not None and not isinstance(expected_artifacts, list):
            errors.append("artifact_ids must be a list")
    if not value.get("artifact_ids"):
        errors.append("review must name the artifact set that was reviewed")
    if value.get("disposition") == "ACCEPT" and any(isinstance(finding, dict) and finding.get("severity") == "BLOCKING" for finding in value.get("findings", [])):
        errors.append("review with a BLOCKING finding cannot ACCEPT")
    dirty = dirty_paths(project)
    if dirty:
        errors.append("review/release candidate has uncommitted or untracked paths: " + ", ".join(dirty[:10]))
    if require_accept and value.get("disposition") != "ACCEPT":
        errors.append("current independent review must ACCEPT")
    return errors


def validate_review(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    path = project_root(args.path) if args.path else latest_json(control_root(project) / "reviews", "REV-")
    if not path or not path.is_file():
        return emit("NOT_RUN", "no independent review receipt exists", next_action="run a fresh reviewer")
    try:
        value = read_json(path)
    except ValueError as exc:
        return fail(str(exc))
    state_pair = require_state(project)
    state = state_pair[1] if state_pair else None
    errors = review_errors(project, value, state)
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
    review = latest_json(control_root(project) / "reviews", "REV-")
    if not review:
        return fail("close requires a current independent ACCEPT review")
    try:
        value = read_json(review)
    except ValueError as exc:
        return fail(str(exc))
    errors = review_errors(project, value, state, require_accept=True)
    if errors:
        return fail("; ".join(errors))
    phase = state.get("phase")
    if phase == "CLOSED":
        return emit("PASS_WITH_LIMITATIONS", "session is already closed", changed=False, next_action=state.get("next_action"))
    if phase == "IN_REVIEW":
        if not transition_allowed("IN_REVIEW", "ACCEPTED") or not transition_allowed("ACCEPTED", "CLOSED"):
            return fail("state transition matrix does not permit review acceptance and close")
        phase = "ACCEPTED"
    elif phase not in ("ACCEPTED", "CLOSED"):
        return fail(f"close requires ACCEPTED or CLOSED state, found {phase}")
    if phase == "ACCEPTED" and not transition_allowed("ACCEPTED", "CLOSED"):
        return fail("state transition matrix does not permit close")
    save_state(state_path, state, project, _event_type="session.closed", phase="CLOSED", status="PASS_WITH_LIMITATIONS", next_action="validate independent review and obtain release approval")
    return emit("PASS_WITH_LIMITATIONS", "session closed with acceptance and release still gated", next_action=state["next_action"])


def release_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return fail("run studio init before studio release")
    if not args.approved_by:
        return fail("release requires explicit owner approval")
    state = pair[1]
    review = latest_json(control_root(project) / "reviews", "REV-")
    if not review:
        return fail("release requires an independent review")
    try:
        value = read_json(review)
    except ValueError as exc:
        return fail(str(exc))
    errors = review_errors(project, value, state, require_accept=True)
    if errors:
        return fail("; ".join(errors))
    if state.get("phase") == "RELEASED":
        return emit("PASS", "release is already recorded; no publish or merge was performed", approved_by=args.approved_by, revision=live_head(project), changed=False)
    if state.get("phase") != "CLOSED":
        return fail(f"release requires CLOSED state, found {state.get('phase')}")
    state_path = pair[0]
    revision = live_head(project)
    if not revision:
        return fail("release requires a live Git HEAD")
    release_id = f"RELEASE-{revision[:12].upper()}"
    release_receipt = {
        "schema": "studio.release/v2",
        "document_id": release_id,
        "version": "2.0.0",
        "status": "RELEASED",
        "revision": revision,
        "review_id": value["review_id"],
        "requirement_digest": value["requirements_digest"],
        "package_digests": {"repository_tree": sha_digest(git(project, "ls-tree", "-r", "HEAD") or revision)},
        "environment": {"platform": sys.platform, "python": sys.version.split()[0]},
        "evidence": value.get("artifact_ids", []) or [value["review_id"]],
        "limitations": ["This local gate did not publish, merge, or change an external service."],
        "waivers": [],
        "rollback": "Restore the prior .project state and revert the release commit if publication occurs separately.",
        "owner_approval": args.approved_by,
        "created_at": utc_now(),
    }
    receipt_issues = document_schema_errors(release_receipt, "release_receipt")
    if receipt_issues:
        return fail("release receipt schema validation failed: " + "; ".join(receipt_issues))
    receipt_path = control_root(project) / "artifacts" / f"{release_id}.json"
    save_state(
        state_path,
        state,
        project,
        _event_type="release.completed",
        _extra_files={receipt_path: json.dumps(release_receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"},
        phase="RELEASED",
        status="PASS",
        next_action="maintain the released revision",
    )
    return emit("PASS", "release gate validated; no publish or merge was performed", approved_by=args.approved_by, revision=revision, receipt=str(receipt_path), changed=True)


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
    metadata_path = control_root(project) / "project.yaml"
    metadata = read_json(metadata_path) if metadata_path.is_file() else {}
    repository = metadata.get("repository") or metadata.get("repository_url") or value.get("repository") or git(project, "remote", "get-url", "origin") or str(project)
    title = metadata.get("title") or value.get("title") or project.name
    issue = {"title": f"{value['wp_id']}: {value['primary_outcome']}", "labels": [str(metadata.get("archetype", "project")), "work-package"], "body": {"project_id": state["project_id"], "requirements": value["requirements"], "acceptance": value["acceptance"], "base_sha": value["base_sha"], "allowed_paths": value["allowed_paths"]}}
    path = control_root(project) / "tracking" / "github-plan.json"
    previous = read_json(path) if path.is_file() else None
    action = "create" if previous is None else "no-op" if previous.get("repository") == repository and previous.get("issues") == [issue] else "update"
    plan = {"schema": "studio.github-projection/v2", "authority": ".project", "confirmation_required": True, "adapter": None, "repository": repository, "milestone": {"title": title, "action": action}, "issues": [issue], "actions": [{"type": action, "target": "milestone-and-issue", "reason": "desired projection compared with the previous local plan"}], "writes_performed": False}
    write_json(path, plan)
    if args.apply:
        return fail("no supported GitHub adapter is configured; the confirmation-gated plan was saved but no external write was attempted")
    return emit("PASS_WITH_LIMITATIONS", "GitHub milestone and issue reconciliation plan generated; no external write performed", path=str(path), next_action="obtain explicit approval before applying the exact plan")


def status_project(args: argparse.Namespace) -> int:
    project = project_root(args.project)
    pair = require_state(project)
    if pair is None:
        return emit("NOT_RUN", "target is not initialized as a Studio project", next_action="studio init")
    _, state = pair
    live = current_sha(project)
    checkpoint = source_sha(project, state)
    expected_live = state.get("live_head_sha") or state.get("current_sha")
    errors = []
    if live and expected_live != live:
        errors.append(f"state live HEAD {expected_live} does not match Git HEAD {live}")
    if live and (state.get("release_candidate_sha") or expected_live) != live:
        errors.append("release candidate is stale")
    errors.extend(projection_errors(project, state))
    if errors:
        return emit("BLOCKED", "project state or recovery projections are stale", state=state, source_checkpoint=checkpoint, live_evidence_head=live, contradictions=errors, next_action="refresh state and review the current SHA change")
    return emit(state.get("status", "UNPROVEN"), "current project state", phase=state.get("phase"), active_wp=state.get("active_wp"), current_sha=expected_live or live, source_checkpoint_sha=checkpoint, live_head_sha=live, release_candidate_sha=state.get("release_candidate_sha"), next_action=state.get("next_action"), blocking_items=state.get("blocking_items", []))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--project", default=".", help="project root containing .project")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    init = commands.add_parser("init")
    init.add_argument("--project-id")
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
    add.add_argument("--exit-code", type=int, default=0)
    add.add_argument("--environment", default="local")
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
