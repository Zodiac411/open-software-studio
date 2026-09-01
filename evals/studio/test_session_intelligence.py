"""Focused behavior checks for the read-only Session Intelligence helper."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "plugins" / "studio-delivery" / "skills" / "studio-session-intelligence" / "session_intelligence.py"


class SessionIntelligenceTests(unittest.TestCase):
    def write_session(self, root: Path, *, session_id: str, cwd: Path, event: str, secret: str) -> None:
        path = root / f"{session_id}.jsonl"
        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        records = [
            {"session_meta": {"payload": {"id": session_id, "cwd": str(cwd), "timestamp": now, "model": "fixture-model"}}},
            {"event_msg": event, "tool_payload": {"credential": secret}},
            {"response_item": {"body": secret}},
        ]
        path.write_text("\n".join(json.dumps(item) for item in records) + "\n", encoding="utf-8")

    def invoke(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True, check=False)

    def test_project_selection_redacts_raw_session_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "project"
            other = root / "other"
            sessions = root / "sessions"
            archived = root / "archived"
            project.mkdir()
            other.mkdir()
            sessions.mkdir()
            archived.mkdir()
            self.write_session(sessions, session_id="11111111-1111-1111-1111-111111111111", cwd=project, event="The task failed with a timeout.", secret="target-secret")
            self.write_session(sessions, session_id="22222222-2222-2222-2222-222222222222", cwd=other, event="Blocked by unrelated work.", secret="other-secret")
            result = self.invoke("--project", str(project), "--sessions-root", str(sessions), "--archived-sessions-root", str(archived))
            self.assertEqual(result.returncode, 0, result.stderr)
            value = json.loads(result.stdout)
            self.assertEqual(value["result"], "PASS")
            self.assertEqual([item["session_id"] for item in value["retro_distillation"]["observed_sessions"]], ["11111111-1111-1111-1111-111111111111"])
            self.assertEqual(value["retro_distillation"]["recurring_friction"], {"error": 1, "timeout": 1})
            self.assertNotIn("target-secret", result.stdout)
            self.assertNotIn("other-secret", result.stdout)
            self.assertNotIn("22222222-2222-2222-2222-222222222222", result.stdout)

    def test_refuses_explicit_out_of_scope_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "project"
            other = root / "other"
            sessions = root / "sessions"
            archived = root / "archived"
            project.mkdir()
            other.mkdir()
            sessions.mkdir()
            archived.mkdir()
            self.write_session(sessions, session_id="33333333-3333-3333-3333-333333333333", cwd=other, event="Blocked by unrelated work.", secret="out-of-scope-secret")
            result = self.invoke("--project", str(project), "--sessions-root", str(sessions), "--archived-sessions-root", str(archived), "--session-id", "33333333-3333-3333-3333-333333333333")
            self.assertEqual(result.returncode, 2, result.stderr)
            value = json.loads(result.stdout)
            self.assertEqual(value["result"], "BLOCKED")
            self.assertNotIn("out-of-scope-secret", result.stdout)
            self.assertNotIn(str(other), result.stdout)


if __name__ == "__main__":
    unittest.main()
