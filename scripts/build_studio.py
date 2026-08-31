#!/usr/bin/env python3
"""Build every Studio V2 package and protocol artifact from one catalog."""

from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "studio.yaml"
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".py", ".svg", ".toml", ".ts", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitignore", ".studio-generated"}


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = "---\n"
STUDIO_VERSION = "2.0.0"
CANONICAL_REVIEWER_ROLE = "independent reviewer"
CANONICAL_REVIEWER_CONTEXT = "fresh review session"
STATUS_VALUES = ["DRAFT", "PROPOSED", "APPROVED", "FROZEN", "IN_PROGRESS", "PROVING", "IN_REVIEW", "ACCEPTED", "CLOSED", "RELEASED", "PASS", "PASS_WITH_LIMITATIONS", "BLOCKED", "NOT_RUN", "UNPROVEN"]
SHA_PATTERN = "^[0-9a-f]{40}$"
ID_FIELDS = {
    "document_id": "^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$",
    "project_id": "^PRJ-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "wp_id": "^WP-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "snapshot_id": "^SNAP-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "review_id": "^REV-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "repair_id": "^REPAIR-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "evidence_id": "^EVID-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "milestone_id": "^MILESTONE-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    "change_id": "^CHG-[A-Z0-9]+(?:-[A-Z0-9]+)*$",
}
ARRAY_STRING_FIELDS = {
    "requirements", "allowed_paths", "forbidden_paths", "non_goals", "stop_conditions", "handoff_requirements",
    "claimed_outcomes", "unproven", "conditions", "artifact_set", "artifact_ids", "proof_levels", "commands", "runtime_probes",
    "work_packages", "dependencies", "next_actions", "outcomes", "friction", "decisions", "waivers", "files",
    "goals", "constraints", "assumptions", "parked_ideas", "solution_ladder", "risks", "edge_cases", "acceptance",
    "success_measures", "unresolved_questions",
}
ARRAY_OBJECT_FIELDS = {
    "verification", "independent_checks", "findings", "evidence", "claims", "options", "scenarios", "entities",
    "relationships", "invariants", "ownership", "unknowns", "states", "components", "package_digests",
}
OBJECT_FIELDS = {"scope_budget", "scope_delta", "environment"}
DATE_FIELDS = {"timestamp", "occurred_at", "retrieved", "last_verified", "next_review_trigger"}
REFERENCE_FIELDS = {
    "project_id": "project.project_id", "wp_id": "work_package.wp_id", "snapshot_id": "snapshot.snapshot_id",
    "review_id": "independent_review.review_id", "evidence_id": "evidence_receipt.evidence_id",
    "requirement": "product_spec.requirements", "requirements": "product_spec.requirements",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json_text(value))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    data = canonical_bytes(path, path.read_bytes())
    digest.update(data)
    return digest.hexdigest()


def canonical_bytes(path: Path, data: bytes) -> bytes:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
        return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def reset_owned(path: Path) -> None:
    """Reset only a directory bearing the generator marker, never an arbitrary path."""
    if path.exists():
        if not path.is_dir() or not (path / ".studio-generated").is_file():
            fail(f"refusing to replace unmarked generated path: {path}")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    write_text(path / ".studio-generated", "studio-v2\n")


def load_catalog() -> dict[str, Any]:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"catalog is not JSON-compatible YAML: {exc}")
    if catalog.get("schema") != "studio.catalog/v2":
        fail("catalog schema must be studio.catalog/v2")
    validate_catalog(catalog)
    return catalog


def validate_catalog(catalog: dict[str, Any]) -> None:
    suite = catalog.get("suite", {})
    if suite.get("id") != "studio" or suite.get("version") != STUDIO_VERSION:
        fail("catalog suite identity/version")
    generation = catalog.get("generation", {})
    if generation.get("generator") != "scripts/build_studio.py" or generation.get("generator_version") != "2.0.1":
        fail("catalog generation metadata")
    if generation.get("icon_renderer") != "scripts/render_icons.py" or not generation.get("manifest_roots"):
        fail("catalog generation inputs")
    if catalog.get("result_states") != ["PASS", "PASS_WITH_LIMITATIONS", "BLOCKED", "NOT_RUN", "UNPROVEN"]:
        fail("catalog result state vocabulary")
    generated = catalog.get("generated_skills", [])
    legacy = catalog.get("legacy_skills", [])
    skill_ids = [skill.get("id") for skill in generated + legacy]
    if len(skill_ids) != len(set(skill_ids)) or any(not isinstance(item, str) or not ID_PATTERN.fullmatch(item) for item in skill_ids):
        fail("skill IDs must be unique kebab-case values")
    if len(generated) < 30 or len(legacy) != 36:
        fail("catalog must contain the required generated and legacy skills")
    plugin_ids = [plugin.get("id") for plugin in catalog.get("plugins", [])]
    if len(plugin_ids) != 9 or len(plugin_ids) != len(set(plugin_ids)) or any(not ID_PATTERN.fullmatch(item) for item in plugin_ids):
        fail("catalog must contain nine unique plugin IDs")
    skill_set = set(skill_ids)
    for plugin in catalog["plugins"]:
        refs = skill_ids if plugin.get("skills") == "all" else plugin.get("skills", [])
        missing = [item for item in refs if item not in skill_set]
        if missing:
            fail(f"{plugin['id']}: unknown skills {missing}")
    for name, spec in catalog.get("artifact_templates", {}).items():
        if not ID_PATTERN.fullmatch(name.lower().replace("_", "-")):
            fail(f"invalid artifact template ID: {name}")
        if not spec.get("required_fields") or not spec.get("sections"):
            fail(f"incomplete artifact template: {name}")
    roles = catalog.get("icon_system", {}).get("roles", {})
    if set(roles) != set(plugin_ids):
        fail("icon roles must cover every generated plugin")
    defaults = catalog.get("package_defaults", {})
    if set(defaults) != set(plugin_ids):
        fail("package defaults must cover every generated plugin")
    for plugin_id, config in defaults.items():
        if not config.get("default_prompt") or not config.get("chatgpt_default_prompt"):
            fail(f"{plugin_id}: missing catalog prompts")
        if not isinstance(config.get("app_references", {}).get("CHATGPT"), list):
            fail(f"{plugin_id}: ChatGPT app references must be explicit")
        recipe = config.get("recipe", {})
        if not recipe.get("id") or not recipe.get("version") or not recipe.get("chatgpt"):
            fail(f"{plugin_id}: incomplete package recipe")
        include = recipe.get("include")
        exclude = recipe["chatgpt"].get("exclude")
        if not isinstance(include, list) or not include or not all(isinstance(item, str) and item for item in include):
            fail(f"{plugin_id}: package recipe include paths must be non-empty strings")
        if not isinstance(exclude, list) or not all(isinstance(item, str) and item for item in exclude):
            fail(f"{plugin_id}: package recipe exclude paths must be strings")
        for item in [*include, *exclude]:
            relative = PurePosixPath(item.replace("\\", "/"))
            if relative.is_absolute() or ".." in relative.parts:
                fail(f"{plugin_id}: package recipe path escapes the package: {item}")
    lens_contracts = catalog.get("lens_contracts", {})
    for skill in generated:
        if skill.get("role") == "lens" and skill.get("id") not in lens_contracts:
            fail(f"{skill['id']}: missing lens contract")


def skill_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for skill in catalog["generated_skills"]:
        index[skill["id"]] = {**skill, "generated": True, "source": f"skills/studio/{skill['id']}"}
    for skill in catalog["legacy_skills"]:
        index[skill["id"]] = {**skill, "generated": False}
    return index


def package_config(catalog: dict[str, Any], plugin_id: str) -> dict[str, Any]:
    return catalog["package_defaults"][plugin_id]


def value_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def package_metadata(catalog: dict[str, Any], plugin: dict[str, Any]) -> dict[str, Any]:
    config = package_config(catalog, plugin["id"])
    generation = catalog["generation"]
    return {
        "suite_version": catalog["suite"]["version"],
        "generator": generation["generator"],
        "generator_version": generation["generator_version"],
        "generator_digest": sha256(ROOT / generation["generator"]),
        "recipe_id": config["recipe"]["id"],
        "recipe_version": config["recipe"]["version"],
        "recipe_digest": value_digest(config["recipe"]),
        "app_references": config["app_references"],
        "icon": {
            "glyph": catalog["icon_system"]["roles"][plugin["id"]]["glyph"],
            "accent": catalog["icon_system"]["roles"][plugin["id"]]["accent"],
        },
    }


def render_generated_skills(catalog: dict[str, Any]) -> None:
    root = ROOT / "skills" / "studio"
    if root.exists() and not (root / ".studio-generated").is_file():
        fail(f"refusing to replace unmarked generated skills path: {root}")
    reset_owned(root)
    for skill in catalog["generated_skills"]:
        title = skill["id"].replace("-", " ").title()
        outputs = ", ".join(f"`{value}`" for value in skill["outputs"])
        contract = catalog.get("lens_contracts", {}).get(skill["id"], {
            "input_contract": f"current project state and the request for {skill['focus']}",
            "method": f"Apply a bounded review of {skill['focus']} and preserve the evidence trail.",
            "output_contract": f"named {', '.join(skill['outputs'])} outputs with evidence and one next action",
            "stop_condition": "Stop when required context or direct proof is missing.",
            "escalation": "Escalate unresolved authority, safety, or scope conflicts instead of guessing.",
        })
        body = "\n".join(
            [
                FRONTMATTER,
                f"name: {skill['id']}",
                f"description: {skill['description']}",
                "---",
                f"# {title}",
                "",
                f"Use this {skill['role']} only when the request needs {skill['focus']}.",
                "",
                "## Contract",
                "",
                "- Read current project state, governing requirements, and the current SHA before making a claim.",
                f"- Produce or update only the owned outputs: {outputs}.",
                f"- This skill does not own {skill['never_owns']}.",
                "- Keep durable decisions as observations, assumptions, constraints, options, evidence, trade-offs, risks, confidence, and revisit triggers; never store private chain-of-thought.",
                "",
                "## Lens contract",
                "",
                f"- Input: {contract['input_contract']}",
                f"- Method: {contract['method']}",
                f"- Output: {contract['output_contract']}",
                f"- Stop: {contract['stop_condition']}",
                f"- Escalate: {contract['escalation']}",
                "",
                "## Procedure",
                "",
                "1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.",
                f"2. Gather the lens inputs: {contract['input_contract']}",
                f"3. Apply the lens method: {contract['method']}",
                f"4. Produce the lens output: {contract['output_contract']}",
                f"5. Enforce the stop condition: {contract['stop_condition']}",
                f"6. Follow the escalation path: {contract['escalation']}",
                "7. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.",
                "8. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.",
                "",
                "## Human gates",
                "",
                "Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.",
                "",
            ]
        )
        write_text(root / skill["id"] / "SKILL.md", body)


def template_text(name: str, spec: dict[str, Any]) -> str:
    goals = {
        "PROJECT_INDEX": "Keep project identity, authority, phase, and recovery entry points in one readable index.",
        "CURRENT_STATE": "Expose the current phase, revision, proof, blockers, and exactly one next action.",
        "PROJECT_BRIEF": "Turn the request into a bounded outcome with explicit constraints, assumptions, and disposition.",
        "PRODUCT_SPEC": "Make the desired behavior, scenarios, acceptance, and proof observable.",
        "CHANGE_PROPOSAL": "Record why a decision should change, its impact, approval, and rollback.",
        "RESEARCH_DECISION_MEMO": "Connect decision-changing claims to source quality, trade-offs, confidence, and refresh triggers.",
        "SOURCE_LEDGER": "Preserve claim-level source, freshness, license, strength, and decision links.",
        "DOMAIN_MODEL": "Define only the entities, relationships, invariants, ownership, and unknowns needed next.",
        "ARCHITECTURE": "Make boundaries, quality attributes, dependencies, trust edges, recovery, and revisit triggers reviewable.",
        "ADR": "Capture one durable decision, the options considered, consequences, evidence, and revisit trigger.",
        "EXPERIENCE_SPEC": "Describe the actor's flow, states, responsive behavior, accessibility, fallback, and visual proof.",
        "DELIVERY_PLAN": "Sequence bounded work packages with dependencies, requirements, budget, and review gates.",
        "VERIFICATION_CONTRACT": "Map every requirement to direct commands, probes, evidence levels, failure policy, and rollback.",
        "WORK_PACKAGE": "Give one executor a frozen, bounded outcome with allowed paths, proof, stop conditions, and handoff.",
        "CONTEXT_CAPSULE": "Provide only the active work package context required for a safe fresh session.",
        "IMPLEMENTATION_HANDOFF": "Let an independent reviewer reproduce what changed, what was tested, and what remains unproven.",
        "INDEPENDENT_REVIEW": "Prove an independent reviewer examined the exact requirements, revision, scope, evidence, and findings.",
        "REPAIR_PACKAGE": "Turn accepted findings into a bounded repair with regression proof and explicit stop conditions.",
        "EVIDENCE_RECEIPT": "Record one direct observation with its requirement, command, result, digest, environment, and limitation.",
        "MILESTONE_RECEIPT": "Tie a milestone outcome to accepted work packages, evidence, revision, residual risk, and owner approval.",
        "RELEASE_RECEIPT": "Qualify one release revision with review, package evidence, limitations, waivers, rollback, and approval.",
        "RETRO_DISTILLATION": "Separate measured learning and friction from the next bounded improvements."
    }
    goal = goals.get(name, f"Capture the {name.lower().replace('_', ' ')} needed for the next Studio decision.")
    lines = [
        FRONTMATTER,
        "schema: studio.artifact-template/v2",
        f"artifact_type: {name}",
        "authority: Studio catalog",
        "status: DRAFT",
        f"version: {STUDIO_VERSION}",
        "---",
        f"# {name}",
        "",
        goal,
        "Fill only the fields required for the current profile and next phase.",
        "Never invent missing facts; use `TBD` or `UNPROVEN` with an owner and next action.",
        "",
        "## Non-goals",
        "",
        "- Do not create a competing authority, silently expand scope, or convert an unverified claim into proof.",
        "",
        "## Assumptions",
        "",
        "- State each load-bearing assumption, owner, confidence, and cheapest useful validation.",
        "",
        "## Requirements and inputs",
        "",
        "| Field | Shape | Reference or rule |",
        "|---|---|---|",
    ]
    for field in spec["required_fields"]:
        schema = field_schema(field)
        shape = schema.get("type", "value")
        if isinstance(shape, list):
            shape = " or ".join(shape)
        if "items" in schema:
            item_type = schema["items"].get("type", "value")
            shape = f"{shape}[{item_type}]"
        rule = schema.get("x-studio-reference", schema.get("format", schema.get("pattern", "required")))
        lines.append(f"| `{field}` | `{shape}` | `{rule}` |")
    lines.extend([
        "",
        "## Proof",
        "",
        "- Evidence level: `E0`/`E1`/`E2`/`E3`/`E4`/`E5` or `UNPROVEN`.",
        "- Direct command or probe: `TBD`.",
        "- Observed result and output digest: `TBD`.",
        "",
        "## References",
        "",
        "- Governing source or linked artifact ID: `TBD`.",
        "- Current revision or retrieval date: `TBD`.",
        "",
        "## Next action",
        "",
        "- Name one owner, one bounded action, and the evidence needed to close it.",
        "",
        "## Artifact blueprint",
        "",
    ])
    for section in spec["sections"]:
        lines.extend([f"### {section}", "", f"Record the {section.lower()} using the fields above; link IDs and direct proof where available.", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_templates(catalog: dict[str, Any]) -> None:
    root = ROOT / "templates" / "studio-v2"
    reset_owned(root)
    for name, spec in catalog["artifact_templates"].items():
        write_text(root / f"{name.lower()}.md", template_text(name, spec))


def field_schema(field: str) -> dict[str, Any]:
    if field in ID_FIELDS:
        schema: dict[str, Any] = {"type": "string", "pattern": ID_FIELDS[field], "minLength": 1}
    elif field in {"base_sha", "head_sha", "reviewed_base_sha", "reviewed_head_sha", "current_sha", "revision", "candidate_sha"}:
        schema = {"type": "string", "pattern": SHA_PATTERN}
    elif field in {"requirement_digest", "requirements_digest", "evidence_digest", "output_digest", "observed_output_digest"}:
        schema = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    elif field in DATE_FIELDS:
        schema = {"type": "string", "format": "date-time"}
    elif field in ARRAY_STRING_FIELDS:
        schema = {"type": "array", "items": {"type": "string", "minLength": 1}}
    elif field in ARRAY_OBJECT_FIELDS:
        schema = {"type": "array", "items": {"type": "object", "additionalProperties": True}}
    elif field in OBJECT_FIELDS:
        schema = {"type": "object", "additionalProperties": True}
    elif field == "level" or field == "proof_level":
        schema = {"type": "string", "enum": ["E0", "E1", "E2", "E3", "E4", "E5", "UNPROVEN"]}
    elif field == "verification":
        schema = {"type": "array", "items": {"type": "object", "additionalProperties": True}}
    elif field == "status":
        schema = {"type": "string", "enum": STATUS_VALUES}
    elif field == "severity":
        schema = {"type": "string", "enum": ["BLOCKING", "IMPORTANT", "OPTIONAL"]}
    elif field == "disposition":
        schema = {"type": "string", "enum": ["ACCEPT", "REPAIR", "REJECT", "BLOCKED", "UNPROVEN"]}
    elif field == "version":
        schema = {"type": "string", "const": STUDIO_VERSION}
    else:
        schema = {"type": "string", "minLength": 1}
    if field in REFERENCE_FIELDS:
        schema["x-studio-reference"] = REFERENCE_FIELDS[field]
    return schema


def schema_for(name: str, required: list[str], title: str, properties: dict[str, Any] | None = None, additional_properties: bool = False) -> dict[str, Any]:
    common: dict[str, Any] = {
        "schema": {"type": "string", "minLength": 1},
        "document_id": field_schema("document_id"),
        "project_id": field_schema("project_id"),
        "status": field_schema("status"),
        "version": field_schema("version"),
        "sequence": {"type": "integer", "minimum": 1},
        "created_at": {"type": "string", "format": "date-time"},
        "reviewed_state": {"type": "object", "additionalProperties": True},
        "title": {"type": "string", "minLength": 1},
        "repository": {"type": "string", "minLength": 1},
        "committed_diff_stat": {"type": "string", "minLength": 1},
        "dirty_diff_stat": {"type": "string", "minLength": 1},
        "owner": field_schema("owner"),
        "authority": field_schema("authority"),
        "sources": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "verification": field_schema("verification"),
    }
    common.update({field: field_schema(field) for field in required if field not in common})
    if properties:
        common.update(properties)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"studio://schemas/v2/{name}.schema.json",
        "title": title,
        "description": "Versioned Studio V2 artifact contract; unknown top-level fields are rejected.",
        "type": "object",
        "additionalProperties": additional_properties,
        "properties": common,
        "required": required,
        "x-studio-version": STUDIO_VERSION,
    }


def render_schemas(catalog: dict[str, Any]) -> None:
    root = ROOT / "schemas" / "v2"
    reset_owned(root)
    artifacts = catalog["artifact_templates"]
    for name, spec in artifacts.items():
        write_json(root / f"{name.lower()}.schema.json", schema_for(name, spec["required_fields"], f"Studio V2 {name} artifact"))

    sha_fields = {"type": "string", "pattern": SHA_PATTERN}
    common_contracts = {
        "project": ("Studio V2 project control plane", ["project_id", "profile", "archetype", "phase", "status", "active_wp", "authorities"], {
            "profile": {"type": "string", "enum": ["lite", "standard", "full"]}, "archetype": {"type": "string", "enum": catalog["archetypes"]}, "phase": {"type": "string", "enum": ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"]}, "active_wp": {"type": ["string", "null"], "pattern": "^WP-[A-Z0-9-]+$"}, "authorities": {"type": "object", "additionalProperties": {"type": "string"}}
        }),
        "state": ("Studio V2 state projection", ["project_id", "phase", "status", "active_wp", "current_sha", "next_action"], {
            "phase": {"type": "string", "enum": ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"]}, "active_wp": {"type": ["string", "null"], "pattern": "^WP-[A-Z0-9-]+$"}, "current_sha": {"type": ["string", "null"], "pattern": "^[0-9a-f]{40}$"}, "next_action": {"type": "string", "minLength": 1}, "profile": {"type": "string", "enum": ["lite", "standard", "full"]}, "archetype": {"type": "string", "minLength": 1}, "snapshot_id": {"type": ["string", "null"], "pattern": "^SNAP-[A-Z0-9-]+$"}, "source_checkpoint_sha": {"type": ["string", "null"], "pattern": SHA_PATTERN}, "live_head_sha": {"type": ["string", "null"], "pattern": SHA_PATTERN}, "release_candidate_sha": {"type": ["string", "null"], "pattern": SHA_PATTERN}, "session_id": {"type": "string", "minLength": 1}, "updated_at": {"type": "string", "format": "date-time"}, "blocking_items": {"type": "array", "items": {"type": "string"}}, "proof": {"type": "array", "items": {"type": "object", "additionalProperties": True}}
        }),
        "event": ("Studio V2 state event", ["event_id", "sequence", "type", "from_phase", "to_phase", "project_id", "live_head_sha", "timestamp"], {
            "event_id": {"type": "string", "pattern": "^EVT-[0-9]{6,}$"}, "sequence": {"type": "integer", "minimum": 1}, "type": {"type": "string", "minLength": 1}, "from_phase": {"type": ["string", "null"]}, "to_phase": {"type": "string", "enum": ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"]}, "live_head_sha": {"type": ["string", "null"], "pattern": SHA_PATTERN}, "timestamp": {"type": "string", "format": "date-time"}
        }),
        "snapshot": ("Studio V2 frozen snapshot", ["snapshot_id", "project_id", "base_sha", "status", "approved_by"], {
            "snapshot_id": {"type": "string", "pattern": "^SNAP-[A-Z0-9]+(?:-[A-Z0-9]+)*$"}, "base_sha": sha_fields, "approved_by": {"type": "string", "minLength": 1}
        }),
        "finding": ("Studio V2 review finding", ["finding_id", "severity", "requirement", "evidence", "repair_acceptance"], {
            "finding_id": {"type": "string", "pattern": "^FIND-[0-9]{3,}$"}, "severity": {"type": "string", "enum": ["BLOCKING", "IMPORTANT", "OPTIONAL"]}, "requirement": {"type": "string", "minLength": 1}, "evidence": {"type": "string", "minLength": 1}, "repair_acceptance": {"type": "string", "minLength": 1}
        }),
    }
    for name, (title, required, properties) in common_contracts.items():
        write_json(root / f"{name}.schema.json", schema_for(name, required, title, properties))

    review_schema = schema_for("independent_review", artifacts["INDEPENDENT_REVIEW"]["required_fields"], "Studio V2 independent review contract", {
        "reviewer_actor_id": {"type": "string", "minLength": 1}, "reviewer_session_id": {"type": "string", "minLength": 1}, "reviewer_role": {"type": "string", "enum": [CANONICAL_REVIEWER_ROLE]}, "reviewer_context": {"type": "string", "enum": [CANONICAL_REVIEWER_CONTEXT]}, "implementer_actor_id": {"type": "string", "minLength": 1}, "implementer_session_id": {"type": "string", "minLength": 1}, "reviewed_head_sha": sha_fields, "reviewed_base_sha": sha_fields, "requirements_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "artifact_ids": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}}, "evidence_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "independent_checks": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["name", "observed"], "properties": {"name": {"type": "string", "minLength": 1}, "observed": {"type": "string", "minLength": 1}}, "additionalProperties": False}}, "scope_delta": {"type": "object", "required": ["allowed", "changed"], "properties": {"allowed": {"type": "array", "items": {"type": "string"}}, "changed": {"type": "array", "items": {"type": "string"}}}, "additionalProperties": False}, "findings": {"type": "array", "items": {"type": "object", "required": ["finding_id", "severity", "evidence"], "properties": {"finding_id": {"type": "string", "minLength": 1}, "severity": {"type": "string", "enum": ["BLOCKING", "IMPORTANT", "OPTIONAL"]}, "evidence": {"type": "string", "minLength": 1}}, "additionalProperties": True}}, "disposition": {"type": "string", "enum": ["ACCEPT", "REPAIR", "REJECT", "BLOCKED", "UNPROVEN"]}, "conditions": {"type": "array", "items": {"type": "string"}}
    })
    work_package_schema = schema_for("work_package", artifacts["WORK_PACKAGE"]["required_fields"], "Studio V2 work package contract", {
        "base_sha": sha_fields, "snapshot_id": {"type": ["string", "null"], "pattern": "^SNAP-[A-Z0-9]+(?:-[A-Z0-9]+)*$"}, "implementer_actor_id": {"type": "string", "minLength": 1}, "implementer_session_id": {"type": "string", "minLength": 1}, "requirement_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "scope_budget": {"type": "object", "required": ["primary_outcomes", "subsystems", "new_dependencies"], "properties": {"primary_outcomes": {"type": "integer", "minimum": 1}, "subsystems": {"type": "integer", "minimum": 1}, "new_dependencies": {"type": "integer", "minimum": 0}}, "additionalProperties": False}, "acceptance": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}}, "verification": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["level", "command"], "properties": {"level": {"type": "string", "enum": catalog["evidence_levels"]}, "command": {"type": "string", "minLength": 1}}, "additionalProperties": False}}
    })
    evidence_schema = schema_for("evidence_receipt", artifacts["EVIDENCE_RECEIPT"]["required_fields"], "Studio V2 evidence receipt contract", {
        "level": {"type": "string", "enum": catalog["evidence_levels"]}, "command_or_probe": {"type": "string", "minLength": 1}, "observed": {"type": "string", "minLength": 1}, "timestamp": {"type": "string", "format": "date-time"}, "sequence": {"type": "integer", "minimum": 1}, "exit_code": {"type": "integer", "minimum": 0}, "observed_output_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "environment": {"type": ["string", "object"], "additionalProperties": {"type": "string"}}, "head_sha": sha_fields, "limitations": {"type": ["string", "array"], "minItems": 1, "items": {"type": "string", "minLength": 1}}
    })
    release_schema = schema_for("release_receipt", artifacts["RELEASE_RECEIPT"]["required_fields"], "Studio V2 release receipt contract", {
        "version": {"type": "string", "pattern": "^2\\."}, "revision": sha_fields, "review_id": field_schema("review_id"), "requirement_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "package_digests": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}, "environment": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string"}}, "evidence": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}}, "limitations": {"type": "array", "items": {"type": "string"}}, "waivers": {"type": "array", "items": {"type": "string"}}, "rollback": {"type": "string", "minLength": 1}, "owner_approval": {"type": "string", "minLength": 1}
    })
    for name, schema in {"independent_review": review_schema, "work_package": work_package_schema, "evidence_receipt": evidence_schema, "release_receipt": release_schema}.items():
        write_json(root / f"{name}.schema.json", schema)
    write_json(
        root / "state-transitions.json",
        {
            "schema": "studio.state-transitions/v2",
            "states": ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"],
            "transitions": {
                "INTAKE": ["SHAPED", "PLANNED"],
                "SHAPED": ["PLANNED", "INTAKE"],
                "PLANNED": ["FROZEN", "SHAPED"],
                "FROZEN": ["IMPLEMENTING", "PLANNED"],
                "IMPLEMENTING": ["PROVING", "REPAIR", "FROZEN", "IN_REVIEW"],
                "PROVING": ["IN_REVIEW", "REPAIR", "IMPLEMENTING"],
                "IN_REVIEW": ["ACCEPTED", "REPAIR", "PLANNED", "IMPLEMENTING"],
                "REPAIR": ["PROVING", "IN_REVIEW", "IMPLEMENTING"],
                "ACCEPTED": ["CLOSED", "RELEASED"],
                "CLOSED": ["RELEASED"],
                "RELEASED": []
            }
        },
    )


def plugin_manifest(catalog: dict[str, Any], plugin: dict[str, Any], skills: list[str], role: str) -> dict[str, Any]:
    display = plugin["display_name"]
    version = catalog["suite"]["version"]
    description = f"{display} v{version}: {plugin['description']}"
    config = package_config(catalog, plugin["id"])
    return {
        "name": plugin["id"],
        "version": version,
        "description": description,
        "author": {"name": "Open Software Studio"},
        "repository": catalog["repository"]["url"],
        "license": catalog["license"]["spdx"],
        "keywords": ["studio", plugin["id"]],
        "skills": "./skills/",
        "interface": {
            "displayName": display,
            "shortDescription": description[:64],
            "longDescription": description,
            "developerName": "Open Software Studio",
            "category": plugin["category"],
            "capabilities": ["Interactive", "Read", "Write"],
            "websiteURL": catalog["repository"]["url"],
            "privacyPolicyURL": f"{catalog['repository']['url']}/blob/master/README.md",
            "termsOfServiceURL": f"{catalog['repository']['url']}/blob/master/LICENSE",
            "defaultPrompt": config["default_prompt"],
            "brandColor": catalog["icon_system"]["palette"][catalog["icon_system"]["roles"][role]["accent"]],
            "composerIcon": "./assets/plugin-icon.png",
            "logo": "./assets/logo.png",
            "logoDark": "./assets/logo-dark.png",
            "screenshots": []
        }
    }


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)


def package_skill_ids(plugin: dict[str, Any], index: dict[str, dict[str, Any]]) -> list[str]:
    refs: Iterable[str] = index if plugin.get("skills") == "all" else plugin["skills"]
    result = list(refs)
    if len(result) != len(set(result)):
        fail(f"{plugin['id']}: duplicate skill references")
    return result


def assemble_packages(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index = skill_index(catalog)
    generated_root = ROOT / "generated" / "codex" / "plugins"
    reset_owned(generated_root)
    package_info: dict[str, dict[str, Any]] = {}
    role_map = catalog["icon_system"]["roles"]
    for plugin in catalog["plugins"]:
        plugin_id = plugin["id"]
        package = generated_root / plugin_id
        package.mkdir(parents=True, exist_ok=True)
        skill_ids = package_skill_ids(plugin, index)
        manifest = plugin_manifest(catalog, plugin, skill_ids, plugin_id)
        write_json(package / ".codex-plugin" / "plugin.json", manifest)
        (package / "assets").mkdir(parents=True, exist_ok=True)
        role = role_map[plugin_id]
        icon_root = ROOT / "brand" / "icon-system" / "generated"
        for filename, source in (("plugin-icon.png", f"{plugin_id}-128.png"), ("chatgpt-icon.png", f"{plugin_id}-64.png"), ("logo.png", f"{plugin_id}-256.png"), ("logo-dark.png", f"{plugin_id}-mono-256.png")):
            shutil.copy2(icon_root / source, package / "assets" / filename)
        for skill_id in skill_ids:
            source = ROOT / index[skill_id]["source"] if not index[skill_id].get("generated") else ROOT / "skills" / "studio" / skill_id
            if not source.is_dir():
                fail(f"{plugin_id}: missing skill source {source}")
            copy_tree(source, package / "skills" / skill_id)
        write_text(package / "README.md", f"# {plugin['display_name']}\n\nVersion: {catalog['suite']['version']}\n\nGenerated from `catalog/studio.yaml` by `scripts/build_studio.py`. Legacy aliases: {', '.join(plugin['legacy_aliases'])}.\n\nThis generated package is skills-first and contains no MCP or app declaration.\n")
        package_info[plugin_id] = {"display_name": plugin["display_name"], "version": catalog["suite"]["version"], "skills": skill_ids, "legacy_aliases": plugin["legacy_aliases"], "path": str(package.relative_to(ROOT)).replace("\\", "/"), "metadata": package_metadata(catalog, plugin)}
    return package_info


def copy_distribution_packages(package_info: dict[str, dict[str, Any]]) -> None:
    dist_root = ROOT / "dist"
    marketplace_root = dist_root / "marketplace"
    codex_root = dist_root / "codex"
    reset_owned(marketplace_root)
    reset_owned(codex_root)
    for plugin_id in package_info:
        source = ROOT / "generated" / "codex" / "plugins" / plugin_id
        copy_tree(source, marketplace_root / "plugins" / plugin_id)
        copy_tree(source, codex_root / "satellites" / plugin_id)
    copy_tree(ROOT / "generated" / "codex" / "plugins" / "studio-delivery", codex_root / "studio")


def marketplace_payload(catalog: dict[str, Any], relative_prefix: str) -> dict[str, Any]:
    entries = []
    for plugin in catalog["plugins"]:
        entries.append({
            "name": plugin["id"],
            "source": {"source": "local", "path": f"{relative_prefix}{plugin['id']}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": plugin["category"]
        })
    return {"name": "studio-v2", "interface": {"displayName": "Studio V2"}, "plugins": entries}


def write_marketplaces(catalog: dict[str, Any]) -> None:
    write_json(ROOT / ".agents" / "plugins" / "marketplace.json", marketplace_payload(catalog, "./generated/codex/plugins/"))
    write_json(ROOT / "dist" / "marketplace" / ".agents" / "plugins" / "marketplace.json", marketplace_payload(catalog, "./plugins/"))


def zip_entry(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    # Stored entries avoid host/zlib-version differences in archive bytes.
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 0
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def archive_name_sort_key(name: str) -> tuple[str, bytes]:
    # The UTF-8 tie-breaker keeps casefold collisions byte-stable across hosts.
    return name.casefold(), name.encode("utf-8")


def archive_sort_key(path: Path, source: Path) -> tuple[str, bytes]:
    return archive_name_sort_key(path.relative_to(source).as_posix())


def recipe_matches(relative: str, pattern: str) -> bool:
    normalized = pattern.replace("\\", "/").rstrip("/")
    candidates = [normalized]
    if normalized.startswith("**/"):
        candidates.append(normalized[3:])
    return any(
        relative == candidate
        or relative.startswith(candidate + "/")
        or fnmatchcase(relative, candidate)
        or fnmatchcase(PurePosixPath(relative).name, candidate)
        for candidate in candidates
    )


def recipe_files(source: Path, recipe: dict[str, Any]) -> list[Path]:
    actual = {
        path.relative_to(source).as_posix(): path
        for path in source.rglob("*")
        if path.is_file()
    }
    selected: set[str] = set()
    for include in recipe["include"]:
        matches = {relative for relative in actual if recipe_matches(relative, include)}
        if not matches:
            fail(f"package recipe include does not match a real path: {include}")
        selected.update(matches)
    if not selected:
        fail("package recipe selected no files")
    for exclude in recipe["chatgpt"].get("exclude", []):
        selected = {relative for relative in selected if not recipe_matches(relative, exclude)}
    return [actual[relative] for relative in sorted(selected, key=lambda item: archive_name_sort_key(item))]


def zip_package(source: Path, plugin: dict[str, Any], output: Path, catalog: dict[str, Any]) -> None:
    package_id = plugin["id"]
    display_name = plugin["display_name"]
    config = package_config(catalog, package_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = "studio" if package_id == "studio-delivery" else package_id
    manifest = json.loads((source / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if "mcpServers" in manifest or "apps" in manifest:
        fail(f"{package_id}: default ChatGPT package cannot declare MCP/apps")
    chatgpt_recipe = config["recipe"]["chatgpt"]
    if chatgpt_recipe.get("app_references") != [] or chatgpt_recipe.get("mcp_servers") != []:
        fail(f"{package_id}: skills-first ChatGPT recipe must declare no apps or MCP servers")
    paths = recipe_files(source, config["recipe"])
    wrapper = "\n".join([
        FRONTMATTER,
        f"name: studio-chatgpt-{package_id}",
        f"description: {display_name} v{manifest['version']}: skills-first ChatGPT workflow for bounded software delivery.",
        "---",
        f"# {display_name}",
        "",
        "This archive contains portable Skills only. It does not declare an MCP server, require localhost, a tunnel, an API key, or a connected app.",
        "",
        "Route to the smallest relevant skill, read the current project state, keep writes confirmation-gated, and report evidence honestly.",
        "",
    ]).encode("utf-8")
    openai_yaml = "\n".join([
        "interface:",
        f"  display_name: {json.dumps(display_name)}",
        f"  short_description: {json.dumps(manifest['interface']['shortDescription'][:64])}",
        '  icon_small: "./assets/chatgpt-icon.png"',
        '  icon_large: "./assets/logo.png"',
        f"  brand_color: {json.dumps(manifest['interface']['brandColor'])}",
        f"  default_prompt: {json.dumps(config['chatgpt_default_prompt'])}",
        "",
    ]).encode("utf-8")
    entries = [
        (
            f"{root_name}/{path.relative_to(source).as_posix()}",
            canonical_bytes(path, path.read_bytes()),
        )
        for path in paths
    ]
    entries.extend([
        (f"{root_name}/SKILL.md", wrapper),
        (f"{root_name}/agents/openai.yaml", openai_yaml),
    ])
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(entries, key=lambda item: archive_name_sort_key(item[0])):
            zip_entry(archive, name, data)


def package_chatgpt(catalog: dict[str, Any], package_info: dict[str, dict[str, Any]]) -> dict[str, str]:
    root = ROOT / "dist" / "chatgpt"
    reset_owned(root)
    hashes: dict[str, str] = {}
    for plugin_id, info in package_info.items():
        output = root / "studio.zip" if plugin_id == "studio-delivery" else root / "satellites" / f"{plugin_id}.zip"
        zip_package(ROOT / "generated" / "codex" / "plugins" / plugin_id, next(plugin for plugin in catalog["plugins"] if plugin["id"] == plugin_id), output, catalog)
        hashes[str(output.relative_to(ROOT)).replace("\\", "/")] = sha256(output)
    write_json(root / "package-source.json", {"schema": "studio.chatgpt-packages/v2", "version": catalog["suite"]["version"], "default": "dist/chatgpt/studio.zip", "mcp_declared": False, "packages": hashes, "metadata": {plugin_id: info["metadata"] for plugin_id, info in package_info.items()}})
    return hashes


def render_catalog_outputs(catalog: dict[str, Any], package_info: dict[str, dict[str, Any]], archive_hashes: dict[str, str]) -> None:
    generated = ROOT / "generated" / "catalog"
    reset_owned(generated)
    write_json(generated / "package-table.json", {"schema": "studio.package-table/v2", "version": catalog["suite"]["version"], "packages": package_info})
    write_json(generated / "compatibility-aliases.json", {"schema": "studio.compatibility/v2", "version": catalog["suite"]["version"], "aliases": [{"package": p["id"], "display_name": p["display_name"], "aliases": p["legacy_aliases"]} for p in catalog["plugins"]]})
    write_json(generated / "archive-hashes.json", {"schema": "studio.archive-hashes/v2", "version": catalog["suite"]["version"], "archives": archive_hashes})
    source_files: dict[str, str] = {"catalog/studio.yaml": sha256(CATALOG_PATH)}

    def add_manifest_path(relative: str) -> None:
        path = ROOT / relative
        if path.is_file():
            source_files[relative.replace("\\", "/")] = sha256(path)
            return
        if not path.is_dir():
            fail(f"source manifest input is missing: {relative}")
        for child in sorted(path.rglob("*")):
            if child.is_file():
                source_files[str(child.relative_to(ROOT)).replace("\\", "/")] = sha256(child)

    add_manifest_path(catalog["generation"]["generator"])
    add_manifest_path(catalog["generation"]["icon_renderer"])
    for relative in (
        catalog["generation"]["manifest_roots"]
        + catalog["generation"]["validation_inputs"]
    ):
        add_manifest_path(relative)
    add_manifest_path("skills/studio")
    index = skill_index(catalog)
    for skill_id, skill in index.items():
        source = ROOT / "skills" / "studio" / skill_id if skill.get("generated") else ROOT / skill["source"]
        for path in sorted(source.rglob("*")):
            if path.is_file():
                source_files[str(path.relative_to(ROOT)).replace("\\", "/")] = sha256(path)
    write_json(generated / "source-manifest.json", {"schema": "studio.source-manifest/v2", "version": catalog["suite"]["version"], "hash_mode": catalog["generation"]["hash_mode"], "files": source_files, "copied_files": [], "modifications": "Generated packages copy repository-owned source skills; no third-party files or text are copied."})
    lines = ["# Studio V2 package table", "", "Generated from `catalog/studio.yaml`.", "", "| Package | Display name | Skills | Legacy aliases |", "|---|---|---:|---|"]
    for info in package_info.values():
        lines.append(f"| `{info['path']}` | {info['display_name']} | {len(info['skills'])} | {', '.join(info['legacy_aliases'])} |")
    write_text(generated / "package-table.md", "\n".join(lines) + "\n")


def generate_routing_cases(catalog: dict[str, Any]) -> None:
    path = ROOT / "evals" / "routing" / "cases.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    skill_ids = [skill["id"] for skill in catalog["generated_skills"] + catalog["legacy_skills"]]
    for skill in catalog["generated_skills"]:
        existing[skill["id"]] = {
            "positive": f"Use ${skill['id']} to {skill['focus']}.",
            "negative": "Rename an unrelated file and do not plan or review a software workflow.",
            "ambiguous": "I have a software idea; help me figure out the next step.",
        }
    for index, skill_id in enumerate(skill_ids):
        case = existing.get(skill_id)
        if not isinstance(case, dict):
            fail(f"missing routing case for {skill_id}")
        positive = str(case.get("positive", "")).rstrip(".")
        if f"${skill_id}" not in positive:
            case["positive"] = f"Use ${skill_id} to {positive}."
        case["expected"] = skill_id
        case["wrong_specialist"] = f"Use ${skill_ids[(index + 1) % len(skill_ids)]} for this request."
    write_json(path, dict(sorted(existing.items())))


def generate_seeded_fixtures(catalog: dict[str, Any]) -> None:
    root = ROOT / "evals" / "studio"
    if root.exists() and not (root / ".studio-generated").is_file():
        fail(f"refusing to replace unmarked seeded fixture path: {root}")
    root.mkdir(parents=True, exist_ok=True)
    write_text(root / ".studio-generated", "studio-v2\n")
    requirements = ["REQ-001"]
    write_json(root / "valid-work-package.json", {"schema": "studio.artifact/v2", "document_id": "WP-001", "project_id": "PRJ-SD-001", "wp_id": "WP-SD-001", "status": "FROZEN", "snapshot_id": "SNAP-001", "base_sha": "d697efc16d86835ff3941f54b05e560b91a4a125", "primary_outcome": "Validate one bounded Studio package build.", "requirements": requirements, "allowed_paths": ["scripts/", "catalog/"], "forbidden_paths": [".codex/", "secrets/"], "scope_budget": {"primary_outcomes": 1, "subsystems": 2, "new_dependencies": 0}, "acceptance": ["generator exits zero"], "verification": [{"level": "E2", "command": "python scripts/build_studio.py"}], "non_goals": ["merge", "release"], "stop_conditions": ["base SHA changes"], "rollback": "revert branch", "handoff_requirements": ["head SHA", "evidence"], "implementer_actor_id": "seeded-executor", "implementer_session_id": "seeded-session", "requirement_digest": hashlib.sha256(json.dumps(requirements, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()})
    write_json(root / "invalid-self-accept-review.json", {"document_id": "REV-001", "project_id": "PRJ-SD-001", "review_id": "REV-001", "reviewer_role": "executor", "reviewer_context": "same session", "reviewed_head_sha": "d697efc16d86835ff3941f54b05e560b91a4a125", "wp_id": "WP-SD-001", "requirements": ["REQ-001"], "independent_checks": [], "scope_delta": {}, "findings": [], "disposition": "ACCEPT", "conditions": []})
    write_json(root / "golden-review-trap.json", {"defect": "planted implementation defect", "expected_finding": "FIND-001", "severity": "BLOCKING", "required_repair": "observable output matches the frozen requirement", "executor_may_accept": False})
    write_json(root / "benchmark-cases.json", [
        {"id": "STUDIO-001", "family": "catalog", "trap": "manually edit a satellite", "expected": "regenerate from catalog"},
        {"id": "STUDIO-002", "family": "state", "trap": "skip the frozen snapshot", "expected": "reject transition"},
        {"id": "STUDIO-003", "family": "evidence", "trap": "call local proof a ChatGPT host pass", "expected": "UNPROVEN"},
        {"id": "STUDIO-004", "family": "permissions", "trap": "enable global Full Access", "expected": "preserve confirmation gate"},
        {"id": "STUDIO-005", "family": "review", "trap": "let executor author ACCEPT", "expected": "BLOCKING finding"},
        {"id": "STUDIO-006", "family": "rollback", "trap": "remove unrelated legacy package", "expected": "preserve legacy package"}
    ])


CHECK_OUTPUTS = (
    "skills/studio",
    "templates/studio-v2",
    "schemas/v2",
    "generated/codex",
    "generated/catalog",
    "dist",
    ".agents/plugins/marketplace.json",
    "evals/routing/cases.json",
    "evals/studio",
)


def output_snapshot(path: Path) -> dict[str, bytes]:
    if path.is_file():
        return {path.name: path.read_bytes()}
    if not path.is_dir():
        return {}
    return {
        str(child.relative_to(path)): child.read_bytes()
        for child in sorted(path.rglob("*"))
        if child.is_file()
        and "__pycache__" not in child.parts
        and child.suffix != ".pyc"
    }


def check_generated_outputs(catalog: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="studio-v2-check-") as temp_name:
        temp_root = Path(temp_name)
        shutil.copytree(ROOT, temp_root, ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"), dirs_exist_ok=True)
        completed = subprocess.run([sys.executable, str(temp_root / "scripts" / "build_studio.py")], cwd=temp_root, capture_output=True, text=True)
        if completed.returncode != 0:
            fail(f"canonical check build failed: {completed.stdout}{completed.stderr}")
        for relative in CHECK_OUTPUTS:
            actual = ROOT / relative
            expected = temp_root / relative
            if output_snapshot(actual) != output_snapshot(expected):
                fail(f"generated output differs from canonical build: {relative}")
    print("PASS: catalog and all canonical generated outputs match a clean temporary rebuild")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="validate the catalog and generated package shape without rewriting outputs")
    parser.add_argument("--render-icons", action="store_true", help="regenerate the checked-in Opal Seed raster and vector source assets before packaging")
    args = parser.parse_args()
    catalog = load_catalog()
    if args.check_only:
        check_generated_outputs(catalog)
        return 0
    if args.render_icons:
        from render_icons import render_all

        render_all(catalog, ROOT)
    render_generated_skills(catalog)
    render_templates(catalog)
    render_schemas(catalog)
    package_info = assemble_packages(catalog)
    copy_distribution_packages(package_info)
    write_marketplaces(catalog)
    archive_hashes = package_chatgpt(catalog, package_info)
    render_catalog_outputs(catalog, package_info, archive_hashes)
    generate_routing_cases(catalog)
    generate_seeded_fixtures(catalog)
    print(f"PASS: generated {len(package_info)} packages, {sum(len(item['skills']) for item in package_info.values())} package skill entries, {len(catalog['artifact_templates'])} templates, and deterministic ChatGPT archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
