"""Focused stdlib regressions for the Studio V2 control-plane invariants."""

from __future__ import annotations

import hashlib
import json
import argparse
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIO = ROOT / "scripts" / "studio.py"
sys.path.insert(0, str(ROOT / "scripts"))
import studio  # noqa: E402
from studio import artifact_evidence_digest, schema_errors  # noqa: E402


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
            "project_id": state["project_id"],
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
            "artifact_ids": ["WP-001", f"HANDOFF-{reviewed_head[:12].upper()}"],
            "evidence_digest": artifact_evidence_digest(self.project, ["WP-001", f"HANDOFF-{reviewed_head[:12].upper()}"])[0],
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
        events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        self.assertIn(("IN_REVIEW", "ACCEPTED"), [(event["from_phase"], event["to_phase"]) for event in events])
        self.assertIn(("ACCEPTED", "CLOSED"), [(event["from_phase"], event["to_phase"]) for event in events])
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
        malformed["reviewer_actor_id"] = "reviewer"
        malformed["reviewer_context"] = "fresh implementation session"
        path.write_text(json.dumps(malformed, indent=2) + "\n", encoding="utf-8")
        _, provenance_result = self.cli("review", "validate", check=False)
        self.assertEqual(provenance_result["result"], "BLOCKED")
        self.assertIn("reviewer_context must be", str(provenance_result["message"]))
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

    def test_review_binds_active_implementer_and_project(self) -> None:
        self.prepare_handoff()
        path = self.review()
        original = json.loads(path.read_text(encoding="utf-8"))
        for field, expected_message in (
            ("implementer_actor_id", "review implementer actor does not match the active work package"),
            ("implementer_session_id", "review implementer session does not match the active work package"),
            ("project_id", "review project_id does not match the active project state"),
        ):
            malformed = dict(original)
            malformed[field] = "mismatched-value"
            path.write_text(json.dumps(malformed, indent=2) + "\n", encoding="utf-8")
            _, result = self.cli("review", "validate", check=False)
            self.assertEqual(result["result"], "BLOCKED")
            self.assertIn(expected_message, str(result["message"]))

    def test_plan_bundle_rolls_back_on_injected_replace_failure(self) -> None:
        state_path = self.project / ".project" / "state.json"
        active_plan_path = self.project / ".project" / "session" / "active-plan.md"
        progress_path = self.project / ".project" / "session" / "progress.md"
        events_path = self.project / ".project" / "events.jsonl"
        wp_path = self.project / ".project" / "work-packages" / "WP-001.json"
        before = {path: path.read_bytes() for path in (state_path, active_plan_path, progress_path, events_path)}
        real_replace = studio.os.replace
        calls = 0

        def replace_with_one_injected_failure(source: str, destination: str) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected atomic bundle failure")
            real_replace(source, destination)

        with mock.patch.object(studio.os, "replace", side_effect=replace_with_one_injected_failure):
            with self.assertRaises(OSError):
                studio.plan_project(argparse.Namespace(project=str(self.project)))
        self.assertGreaterEqual(calls, 2)
        self.assertFalse(wp_path.exists())
        self.assertEqual(before, {path: path.read_bytes() for path in before})

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

    def test_release_rejects_post_review_artifact_mutation(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        handoff_path = next((self.project / ".project" / "handoffs").glob("HANDOFF-*.json"))
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        handoff["claimed_outcomes"].append("mutated after review")
        handoff_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
        _, result = self.cli("release", "--approved-by", "owner", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("evidence digest", str(result["message"]))
        state = json.loads((self.project / ".project" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["phase"], "CLOSED")

    def test_release_rejects_corrupt_projection_before_mutation(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        state_path = self.project / ".project" / "state.json"
        receipt_root = self.project / ".project" / "artifacts"
        before = state_path.read_bytes()
        progress_path = self.project / ".project" / "session" / "progress.md"
        progress = progress_path.read_text(encoding="utf-8")
        progress_path.write_text(progress.replace("- State projection: phase=CLOSED", "- State projection: phase=INTAKE", 1), encoding="utf-8")
        _, result = self.cli("release", "--approved-by", "owner", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("coherent state, projections, and event history", str(result["message"]))
        self.assertEqual(before, state_path.read_bytes())
        self.assertFalse(any(receipt_root.glob("RELEASE-*.json")))

    def test_doctor_rejects_non_monotonic_or_illegal_events(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        events_path = self.project / ".project" / "events.jsonl"
        events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        events[-1]["sequence"] = events[-2]["sequence"]
        events[-1]["event_id"] = events[-2]["event_id"]
        events_path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        _, result = self.cli("doctor", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("event sequence", json.dumps(result["checks"]))
        events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        events[-1]["sequence"] = events[-2]["sequence"] + 1
        events[-1]["event_id"] = f"EVT-{events[-1]['sequence']:06d}"
        events[-1]["to_phase"] = "INTAKE"
        events_path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        _, illegal_result = self.cli("doctor", check=False)
        self.assertEqual(illegal_result["result"], "BLOCKED")
        self.assertIn("illegal state transition", json.dumps(illegal_result["checks"]))

    def test_doctor_rejects_event_sequence_starting_after_one(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        events_path = self.project / ".project" / "events.jsonl"
        events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        events[0]["sequence"] = 2
        events[0]["event_id"] = "EVT-000002"
        events_path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        _, result = self.cli("doctor", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("event sequence must start at 1", json.dumps(result["checks"]))

    def test_doctor_rejects_noncontiguous_event_sequences(self) -> None:
        self.prepare_handoff()
        self.review()
        self.cli("close")
        events_path = self.project / ".project" / "events.jsonl"
        events = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        events[1]["sequence"] = 3
        events[1]["event_id"] = "EVT-000003"
        events_path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        _, result = self.cli("doctor", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("event sequence is not contiguous", json.dumps(result["checks"]))

    def test_evidence_validation_rejects_observed_payload_mutation(self) -> None:
        self.cli("evidence", "add", "--evidence-id", "EVID-DIGEST", "--requirement", "REQ-001", "--level", "E2", "--command-or-probe", "git status --short", "--observed", "original output")
        path = self.project / ".project" / "evidence" / "EVID-DIGEST.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["observed"] = "mutated output"
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        _, result = self.cli("evidence", "validate", check=False)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("observed output digest", str(result["message"]))

    def test_schema_validator_enforces_min_properties(self) -> None:
        self.assertTrue(schema_errors({}, {"type": "object", "minProperties": 1}))

    def test_generic_plan_track_and_evidence_round_trip(self) -> None:
        self.cli("plan")
        _, blocked = self.cli("track", check=False)
        self.assertEqual(blocked["result"], "BLOCKED")
        self.assertIn("frozen approved work package", str(blocked["message"]))
        self.cli("freeze", "--approved-by", "owner")
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
