"""Local, redacted Session Intelligence summaries for one approved project."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


SAFE_SESSION_ID = re.compile(r"[A-Za-z0-9-]{8,128}\Z")
FRICTION_PATTERNS = {
    "error": re.compile(r"\b(error|failed|failure|exception)\b", re.IGNORECASE),
    "blocked": re.compile(r"\b(blocked|blocker|cannot proceed)\b", re.IGNORECASE),
    "timeout": re.compile(r"\b(timeout|timed out)\b", re.IGNORECASE),
}


class Refusal(ValueError):
    """A request that must not be widened or silently repaired."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Absolute project path to summarize.")
    parser.add_argument("--sessions-root", help="Explicit session index root; defaults to CODEX_HOME/sessions.")
    parser.add_argument("--archived-sessions-root", help="Explicit archived index root; defaults to CODEX_HOME/archived_sessions.")
    parser.add_argument("--session-id", action="append", default=[], help="Explicit session ID; repeatable.")
    parser.add_argument("--since-days", type=int, default=30, help="Lookback window in days (default: 30).")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="Optional explicit absolute path for a redacted artifact.")
    return parser.parse_args(argv)


def normalized_path(value: str | Path) -> str:
    return os.path.normcase(os.path.normpath(str(Path(value).expanduser().resolve(strict=False))))


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def metadata_from(record: dict[str, Any]) -> dict[str, Any] | None:
    value = record.get("session_meta")
    if not isinstance(value, dict):
        return None
    payload = value.get("payload", value)
    return payload if isinstance(payload, dict) else None


def text_from_event(record: dict[str, Any]) -> str:
    """Read only the narrow event-message field; never descend into tool payloads."""
    value = record.get("event_msg")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "message", "summary"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
    return ""


def classify_event(record: dict[str, Any]) -> list[str]:
    text = text_from_event(record)
    return [name for name, pattern in FRICTION_PATTERNS.items() if pattern.search(text)]


def candidate_files(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.rglob("*.jsonl") if path.is_file())


def session_roots(args: argparse.Namespace) -> list[tuple[str, Path]]:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return [
        ("sessions", Path(args.sessions_root) if args.sessions_root else codex_home / "sessions"),
        ("archived_sessions", Path(args.archived_sessions_root) if args.archived_sessions_root else codex_home / "archived_sessions"),
    ]


def scan_sessions(args: argparse.Namespace) -> tuple[list[dict[str, Any]], Counter[str], list[str]]:
    if args.since_days < 0:
        raise Refusal("--since-days must be zero or greater")
    project_path = Path(args.project).expanduser()
    if not project_path.is_absolute() or not project_path.is_dir():
        raise Refusal("--project must be an existing absolute project directory")
    requested = list(dict.fromkeys(args.session_id))
    if any(not SAFE_SESSION_ID.fullmatch(value) for value in requested):
        raise Refusal("each --session-id must be a safe session identifier")
    project = normalized_path(project_path)
    cutoff = datetime.now(UTC) - timedelta(days=args.since_days)
    found: dict[str, dict[str, Any]] = {}
    all_explicit: dict[str, dict[str, Any]] = {}

    for source, root in session_roots(args):
        for path in candidate_files(root):
            metadata: dict[str, Any] | None = None
            friction = Counter()
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line in lines:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(record, dict):
                    continue
                if metadata is None:
                    metadata = metadata_from(record)
                    if metadata is not None:
                        continue
                friction.update(classify_event(record))
            if metadata is None:
                continue
            session_id = metadata.get("id") or metadata.get("session_id")
            cwd = metadata.get("cwd") or metadata.get("project_cwd") or metadata.get("workspace_path")
            if not isinstance(session_id, str) or not SAFE_SESSION_ID.fullmatch(session_id) or not isinstance(cwd, str):
                continue
            timestamp = parse_timestamp(metadata.get("timestamp") or metadata.get("created_at") or metadata.get("started_at"))
            observed = {
                "session_id": session_id,
                "timestamp": timestamp.isoformat().replace("+00:00", "Z") if timestamp else None,
                "model": metadata.get("model") if isinstance(metadata.get("model"), str) else None,
                "source": source,
                "project_matches": normalized_path(cwd) == project,
                "within_window": timestamp is not None and timestamp >= cutoff,
                "friction": friction,
            }
            if session_id in requested:
                all_explicit[session_id] = observed
            if observed["project_matches"] and observed["within_window"]:
                found[session_id] = observed

    if requested:
        missing = [item for item in requested if item not in all_explicit]
        outside = [item for item in requested if item in all_explicit and not (all_explicit[item]["project_matches"] and all_explicit[item]["within_window"])]
        if missing or outside:
            labels = []
            if missing:
                labels.append("not found")
            if outside:
                labels.append("outside the approved project or lookback window")
            raise Refusal(f"requested session target is {' and '.join(labels)}")
        selected = [found[item] for item in requested]
    else:
        selected = [found[key] for key in sorted(found)]

    total_friction: Counter[str] = Counter()
    for item in selected:
        total_friction.update(item["friction"])
    limitations = [
        "Read only: metadata and generic event classifications were used; raw session bodies and tool payloads were excluded.",
        "Local observations do not prove live completion, external publication, or account state.",
    ]
    if not selected:
        limitations.append("No matching sessions were found in the approved project and lookback window.")
    return selected, total_friction, limitations


def report(args: argparse.Namespace) -> dict[str, Any]:
    selected, friction, limitations = scan_sessions(args)
    result = "PASS" if selected else "PASS_WITH_LIMITATIONS"
    sessions = [
        {key: item[key] for key in ("session_id", "timestamp", "model", "source")}
        for item in selected
    ]
    return {
        "schema": "studio.session-intelligence/v1",
        "result": result,
        "scope": {
            "project": normalized_path(args.project),
            "since_days": args.since_days,
            "requested_session_ids": list(dict.fromkeys(args.session_id)),
        },
        "retro_distillation": {
            "observed_sessions": sessions,
            "recurring_friction": dict(sorted(friction.items())),
            "proposed_work_packages": [],
        },
        "context_capsule": {
            "evidence": [f"session:{item['session_id']}" for item in sessions],
            "limitations": limitations,
            "next_action": "Review the redacted findings and approve one bounded work package only if a recurring friction warrants change.",
        },
    }


def markdown(value: dict[str, Any]) -> str:
    scope = value["scope"]
    retro = value["retro_distillation"]
    capsule = value["context_capsule"]
    lines = [
        "# Session Intelligence",
        "",
        "## Result",
        "",
        str(value["result"]),
        "",
        "## Scope",
        "",
        f"- Project: `{scope['project']}`",
        f"- Lookback: {scope['since_days']} days",
        "",
        "## RETRO_DISTILLATION",
        "",
        "### Observed sessions",
        "",
    ]
    sessions = retro["observed_sessions"]
    lines.extend([f"- `session:{item['session_id']}` ({item['timestamp'] or 'timestamp unavailable'})" for item in sessions] or ["- None"])
    lines.extend(["", "### Recurring friction", ""])
    lines.extend([f"- {name}: {count}" for name, count in retro["recurring_friction"].items()] or ["- None observed"])
    lines.extend(["", "### Proposed work packages", "", "- None; this summary does not authorize changes.", "", "## CONTEXT_CAPSULE", "", "### Evidence"])
    lines.extend([f"- `{item}`" for item in capsule["evidence"]] or ["- None"])
    lines.extend(["", "### Limitations", ""])
    lines.extend([f"- {item}" for item in capsule["limitations"]])
    lines.extend(["", "### Next action", "", capsule["next_action"], ""])
    return "\n".join(lines)


def blocked(args: argparse.Namespace, message: str) -> dict[str, Any]:
    return {
        "schema": "studio.session-intelligence/v1",
        "result": "BLOCKED",
        "scope": {"project": normalized_path(args.project), "since_days": args.since_days, "requested_session_ids": list(dict.fromkeys(args.session_id))},
        "limitations": [message, "No session content was emitted."],
        "next_action": "Provide a valid session ID within the approved project and lookback window, or omit explicit session IDs.",
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.output:
            output = Path(args.output).expanduser()
            project = Path(args.project).expanduser()
            if not output.is_absolute() or not project.is_absolute():
                raise Refusal("--output and --project must be explicit absolute paths")
            try:
                output.resolve(strict=False).relative_to(project.resolve(strict=False))
            except ValueError as exc:
                raise Refusal("--output must stay within the approved project directory") from exc
        value = report(args)
        rendered = markdown(value) if args.format == "markdown" else json.dumps(value, indent=2) + "\n"
        if args.output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        sys.stdout.write(rendered)
        return 0
    except Refusal as exc:
        value = blocked(args, str(exc))
        rendered = markdown(value) if args.format == "markdown" else json.dumps(value, indent=2) + "\n"
        sys.stdout.write(rendered)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
