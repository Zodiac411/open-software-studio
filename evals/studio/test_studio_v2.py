"""Focused stdlib regressions for the Studio V2 control-plane invariants."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIO = ROOT / "scripts" / "studio.py"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


class StudioV2RegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "studio-tests@example.invalid")
        self.git("config", "user.name", "Studio Tests")
        (self.project / "README.md").write_text("# Generic project\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-m", "initial")
        self.cli("init", "--project-id", "PRJ-GENERIC")
        metadata_path = self.project / ".project" / "project.yaml"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update({
            "title": "Lantern",
            "primary_outcome": "Deliver the lantern workflow",
            "requirements": ["REQ-LANTERN"],
            "verification_commands": ["git status --short"],
            "repository": "https://example.invalid/lantern.git",
        })
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(["git", "-C", str(self.project), *args], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def cli(self, *args: str, check: bool = True) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        result = subprocess.run([sys.executable, str(STUDIO), "--project", str(self.project), *args], capture_output=True, text=True)
        if check:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result, json.loads(result.stdout)

    def prepare_handoff(self) -> tuple[dict[str, object], str]:
        self.cli("plan")
        self.cli("freeze", "--approved-by", "owner")
        self.cli("context")
        (self.project / "feature.py").write_text("VALUE = 'lantern'\n", encoding="utf-8")
        self.git("add", "feature.py")
        self.git("commit", "-m", "implement lantern workflow")
        _, result = self.cli("handoff")
        handoff = json.loads(Path(str(result["path"])).read_text(encoding="utf-8"))
        return handoff, self.git("rev-parse", "HEAD")

    def review(self, *, actor: str = "reviewer", session: str = "review-session", head: str | None = None) -> Path:
        state = json.loads((self.project / ".project" / "state.json").read_text(encoding="utf-8"))
        wp = json.loads((self.project / ".project" / "work-packages" / "WP-001.json").read_text(encoding="utf-8"))
        reviewed_head = head or self.git("rev-parse", "HEAD")
        value = {
            "schema": "studio.review/v2",
            "document_id": "REV-001",
            "review_id": "REV-001",
            "sequence": 1,
            "reviewer_role": "independent reviewer",
            "reviewer_context": "fresh review session",
            "reviewer_actor_id": actor,
            "reviewer_session_id": session,
            "implementer_actor_id": wp["implementer_actor_id"],
            "implementer_session_id": wp["implementer_session_id"],
            "reviewed_base_sha": wp["base_sha"],
            "reviewed_head_sha": reviewed_head,
            "wp_id": wp["wp_id"],
            "requirements": wp["requirements"],
            "requirements_digest": digest(wp["requirements"]),
            "artifact_ids": ["WP-001", "HANDOFF"],
            "evidence_digest": digest(["reviewed the base-to-head diff", "ran the recorded verification command"]),
            "independent_checks": [
                {"name": "base-to-head diff", "observed": "reviewed independently"},
                {"name": "verification command", "observed": "ran independently"},
            ],
            "scope_delta": {"allowed": ["feature.py"], "changed": ["feature.py"]},
            "findings": [],
            "disposition": "ACCEPT",
            "conditions": [],
            "reviewed_state": {"phase": state["phase"], "head_sha": reviewed_head},
            "created_at": "2026-08-31T00:00:00Z",
        }
        path = self.project / ".project" / "reviews" / "REV-001.json"
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def test_happy_transition_and_idempotent_close(self) -> None:
        _, doctor = self.cli("doctor")
        self.assertEqual(doctor["result"], "PASS")
        handoff, head = self.prepare_handoff()
        snapshot = json.loads((self.project / ".project" / "snapshots" / "SNAP-001.json").read_text())
        self.assertEqual(handoff["base_sha"], snapshot["base_sha"])
        self.assertIn("feature.py", handoff["files"])
        self.review()
        self.cli("review", "validate")
        self.cli("close")
        state_path = self.project / ".project" / "state.json"
        progress_path = self.project / ".project" / "session" / "progress.md"
        events_path = self.project / ".project" / "events.jsonl"
        before = (state_path.read_bytes(), progress_path.read_bytes(), events_path.read_bytes())
        _, second = self.cli("close")
        self.assertFalse(second["changed"])
        self.assertEqual(before, (state_path.read_bytes(), progress_path.read_bytes(), events_path.read_bytes()))
        _, release = self.cli("release", "--approved-by", "owner")
        released = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual((released["phase"], released["status"], released["live_head_sha"]), ("RELEASED", "PASS", head))
        receipt = Path(str(release["receipt"]))
        self.assertTrue(receipt.is_file())
        self.assertEqual(json.loads(receipt.read_text(encoding="utf-8"))["revision"], head)

    def test_self_review_rejection(self) -> None:
        self.prepare_handoff()
        path = self.review(actor="project-executor", session="same implementation session")
        _, result = self.cli("review", "validate", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("reviewer and implementer actor must differ", str(result["message"]))
        malformed = json.loads(path.read_text(encoding="utf-8"))
        malformed["reviewer_role"] = []
        path.write_text(json.dumps(malformed, indent=2) + "\n", encoding="utf-8")
        malformed_result, typed = self.cli("review", "validate", check=False)
        self.assertEqual(malformed_result.returncode, 2)
        self.assertEqual(typed["result"], "BLOCKED")
        self.assertIn("expected string", str(typed["message"]))

    def test_stale_sha_rejection(self) -> None:
        self.cli("plan")
        self.cli("freeze", "--approved-by", "owner")
        self.cli("context")
        (self.project / "feature.py").write_text("VALUE = 'lantern'\n", encoding="utf-8")
        self.git("add", "feature.py")
        self.git("commit", "-m", "move head before context refresh")
        _, stale_context = self.cli("context", check=False)
        self.assertEqual(stale_context["result"], "BLOCKED")
        self.assertIn("context capsule is stale", str(stale_context["message"]))
        self.cli("handoff")
        self.review()
        (self.project / "later.txt").write_text("later\n", encoding="utf-8")
        self.git("add", "later.txt")
        self.git("commit", "-m", "move head")
        _, result = self.cli("review", "validate", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("review is stale", str(result["message"]))

    def test_release_failure_is_atomic(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        state_path = self.project / ".project" / "state.json"
        before = state_path.read_bytes()
        self.review(actor="project-executor", session="same implementation session")
        _, result = self.cli("release", "--approved-by", "owner", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(before, state_path.read_bytes())
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["phase"], "CLOSED")
        self.assertNotEqual(state["status"], "PASS")
        valid_review = self.review()
        self.assertTrue(valid_review.is_file())
        untracked = self.project / "unreviewed.txt"
        untracked.write_text("not reviewed\n", encoding="utf-8")
        _, dirty_result = self.cli("release", "--approved-by", "owner", check=False)
        self.assertEqual(dirty_result["result"], "BLOCKED")
        self.assertIn("uncommitted or untracked", str(dirty_result["message"]))
        self.assertEqual(before, state_path.read_bytes())

    def test_generic_plan_track_and_evidence_round_trip(self) -> None:
        self.cli("plan")
        work_package = json.loads((self.project / ".project" / "work-packages" / "WP-001.json").read_text(encoding="utf-8"))
        serialized = json.dumps(work_package)
        self.assertIn("Lantern", serialized)
        self.assertNotIn("open-software-studio", serialized)
        self.assertNotIn("validate_studio.py", serialized)
        _, track = self.cli("track")
        projection = json.loads(Path(str(track["path"])).read_text(encoding="utf-8"))
        self.assertEqual(projection["repository"], "https://example.invalid/lantern.git")
        self.assertEqual(projection["milestone"]["action"], "create")
        _, second_track = self.cli("track")
        projection = json.loads(Path(str(second_track["path"])).read_text(encoding="utf-8"))
        self.assertEqual(projection["milestone"]["action"], "no-op")
        _, apply_result = self.cli("track", "--apply", check=False)
        self.assertEqual(apply_result["result"], "BLOCKED")
        self.assertIn("no supported GitHub adapter", str(apply_result["message"]))
        self.cli("evidence", "add", "--evidence-id", "EVID-ROUNDTRIP", "--requirement", "REQ-LANTERN", "--level", "E2", "--command-or-probe", "git status --short", "--observed", "command completed")
        _, result = self.cli("evidence", "validate")
        self.assertEqual(result["result"], "PASS")

    def test_artifact_compiler_rejects_malformed_types_and_emits_portable_targets(self) -> None:
        malformed = self.project / "malformed.json"
        malformed.write_text(json.dumps({
            "document_id": 42,
            "project_id": "not-a-project-id",
            "primary_outcome": None,
            "target_actor": [],
            "desired_outcome": "usable output",
            "constraints": "none",
            "non_goals": "not-a-list",
            "assumptions": [],
            "parked_ideas": [],
            "solution_ladder": [],
            "disposition": "ACCEPT",
        }), encoding="utf-8")
        _, rejected = self.cli("artifact", "compile", "--type", "PROJECT_BRIEF", "--data", str(malformed), check=False)
        self.assertEqual(rejected["result"], "BLOCKED")
        self.assertIn("schema validation failed", str(rejected["message"]))

        valid = self.project / "valid.json"
        valid.write_text(json.dumps({
            "document_id": "BRIEF-001",
            "project_id": "PRJ-GENERIC",
            "primary_outcome": "Deliver the lantern workflow",
            "target_actor": "Lantern operator",
            "desired_outcome": "A directly verified workflow",
            "constraints": ["No external writes"],
            "non_goals": ["Release"],
            "assumptions": ["Git remains available"],
            "parked_ideas": ["Hosted integration"],
            "solution_ladder": ["Reuse the current CLI"],
            "disposition": "ACCEPT",
        }), encoding="utf-8")
        _, compiled = self.cli("artifact", "compile", "--type", "PROJECT_BRIEF", "--data", str(valid))
        for key in ("markdown", "sidecar", "yaml", "github_body", "google_docs_payload"):
            self.assertTrue(Path(str(compiled[key])).is_file(), key)


if __name__ == "__main__":
    unittest.main()
