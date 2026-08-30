#!/usr/bin/env python3
"""Build every Studio V2 package and protocol artifact from one catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "studio.yaml"


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = "---\n"


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
    digest.update(path.read_bytes())
    return digest.hexdigest()


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
    if suite.get("id") != "studio" or suite.get("version") != "2.0.0":
        fail("catalog suite identity/version")
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


def skill_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for skill in catalog["generated_skills"]:
        index[skill["id"]] = {**skill, "generated": True, "source": f"skills/studio/{skill['id']}"}
    for skill in catalog["legacy_skills"]:
        index[skill["id"]] = {**skill, "generated": False}
    return index


def render_generated_skills(catalog: dict[str, Any]) -> None:
    root = ROOT / "skills" / "studio"
    if root.exists() and not (root / ".studio-generated").is_file():
        fail(f"refusing to replace unmarked generated skills path: {root}")
    reset_owned(root)
    for skill in catalog["generated_skills"]:
        title = skill["id"].replace("-", " ").title()
        outputs = ", ".join(f"`{value}`" for value in skill["outputs"])
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
                "## Procedure",
                "",
                "1. Identify the active profile, archetype, phase, work package, authority map, and next valid transition.",
                "2. Apply the smallest adequate solution ladder and record why higher machinery is not required.",
                "3. Make requirements, acceptance, scope, proof level, and stop conditions observable.",
                "4. Preserve security, accessibility, correctness, validation, error handling, and data-loss protection.",
                "5. Return one of `PASS`, `PASS_WITH_LIMITATIONS`, `BLOCKED`, `NOT_RUN`, or `UNPROVEN`, with named evidence and one next action.",
                "",
                "## Human gates",
                "",
                "Pause for identity, OAuth/account selection, permission changes, external writes, custom-instruction changes, merge, or release. Never request or handle passwords, MFA codes, cookies, recovery codes, tokens, or API keys.",
                "",
            ]
        )
        write_text(root / skill["id"] / "SKILL.md", body)


def template_text(name: str, spec: dict[str, Any]) -> str:
    lines = [
        FRONTMATTER,
        "schema: studio.artifact-template/v2",
        f"artifact_type: {name}",
        "authority: Studio catalog",
        "status: DRAFT",
        "version: 2.0",
        "---",
        f"# {name}",
        "",
        "Fill only the fields required for the current profile and next phase.",
        "Never invent missing facts; use `TBD` or `UNPROVEN` with an owner and next action.",
        "",
        "## Required fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in spec["required_fields"])
    for section in spec["sections"]:
        lines.extend(["", f"## {section}", "", "- "])
    return "\n".join(lines) + "\n"


def render_templates(catalog: dict[str, Any]) -> None:
    root = ROOT / "templates" / "studio-v2"
    reset_owned(root)
    for name, spec in catalog["artifact_templates"].items():
        write_text(root / f"{name.lower()}.md", template_text(name, spec))


def schema_for(name: str, required: list[str], title: str, properties: dict[str, Any] | None = None) -> dict[str, Any]:
    common: dict[str, Any] = {
        "document_id": {"type": "string", "pattern": "^[A-Z][A-Z0-9-]+$"},
        "project_id": {"type": "string", "pattern": "^PRJ-[A-Z0-9-]+$"},
        "status": {"type": "string"},
        "version": {"type": "string", "pattern": "^2\\."},
        "owner": {"type": "string"},
        "authority": {"type": "string"},
        "sources": {"type": "array", "items": {"type": "string"}},
        "verification": {"enum": ["E0", "E1", "E2", "E3", "E4", "E5", "verified", "partial", "unverified", "not-applicable"]},
    }
    if properties:
        common.update(properties)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"studio://schemas/v2/{name}.schema.json",
        "title": title,
        "type": "object",
        "additionalProperties": True,
        "properties": common,
        "required": required,
    }


def render_schemas(catalog: dict[str, Any]) -> None:
    root = ROOT / "schemas" / "v2"
    reset_owned(root)
    artifacts = catalog["artifact_templates"]
    for name, spec in artifacts.items():
        write_json(root / f"{name.lower()}.schema.json", schema_for(name, spec["required_fields"], f"Studio V2 {name} artifact"))

    special: dict[str, dict[str, Any]] = {
        "project": schema_for(
            "project",
            ["project_id", "profile", "archetype", "phase", "status", "active_wp", "authorities"],
            "Studio V2 project control plane",
            {"profile": {"enum": ["lite", "standard", "full"]}, "archetype": {"enum": catalog["archetypes"]}, "phase": {"type": "string"}, "active_wp": {"type": ["string", "null"]}, "authorities": {"type": "object"}},
        ),
        "state": schema_for(
            "state",
            ["project_id", "phase", "status", "active_wp", "current_sha", "next_action"],
            "Studio V2 state projection",
            {"phase": {"type": "string"}, "active_wp": {"type": ["string", "null"]}, "current_sha": {"type": ["string", "null"], "pattern": "^([0-9a-f]{40})?$"}, "next_action": {"type": "string"}},
        ),
        "event": schema_for("event", ["event_id", "project_id", "event_type", "occurred_at", "actor"], "Studio V2 state event", {"event_id": {"type": "string", "pattern": "^EV-[0-9]{3,}$"}, "event_type": {"type": "string"}, "occurred_at": {"type": "string", "format": "date-time"}, "actor": {"type": "string"}}),
        "snapshot": schema_for("snapshot", ["snapshot_id", "project_id", "base_sha", "status", "approved_by"], "Studio V2 frozen snapshot", {"snapshot_id": {"type": "string", "pattern": "^SNAP-[0-9]{3,}$"}, "base_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"}, "approved_by": {"type": "string"}}),
        "finding": schema_for("finding", ["finding_id", "severity", "requirement", "evidence", "repair_acceptance"], "Studio V2 review finding", {"finding_id": {"type": "string", "pattern": "^FIND-[0-9]{3,}$"}, "severity": {"enum": ["BLOCKING", "IMPORTANT", "OPTIONAL"]}, "requirement": {"type": "string"}, "evidence": {"type": "string"}, "repair_acceptance": {"type": "string"}}),
    }
    for name, schema in special.items():
        write_json(root / f"{name}.schema.json", schema)
    write_json(
        root / "state-transitions.json",
        {
            "schema": "studio.state-transitions/v2",
            "states": ["INTAKE", "SHAPED", "PLANNED", "FROZEN", "IMPLEMENTING", "PROVING", "IN_REVIEW", "REPAIR", "ACCEPTED", "CLOSED", "RELEASED"],
            "transitions": {
                "INTAKE": ["SHAPED"],
                "SHAPED": ["PLANNED", "INTAKE"],
                "PLANNED": ["FROZEN", "SHAPED"],
                "FROZEN": ["IMPLEMENTING", "PLANNED"],
                "IMPLEMENTING": ["PROVING", "REPAIR", "FROZEN"],
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
            "defaultPrompt": [f"Use {display} for this bounded software task.", "Read the current Studio state before acting."],
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
        package_info[plugin_id] = {"display_name": plugin["display_name"], "version": catalog["suite"]["version"], "skills": skill_ids, "legacy_aliases": plugin["legacy_aliases"], "path": str(package.relative_to(ROOT)).replace("\\", "/")}
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
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 0
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def zip_package(source: Path, package_id: str, output: Path, display_name: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = "studio" if package_id == "studio-delivery" else package_id
    manifest = json.loads((source / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if "mcpServers" in manifest or "apps" in manifest:
        fail(f"{package_id}: default ChatGPT package cannot declare MCP/apps")
    paths = [path for path in source.rglob("*") if path.is_file() and ".studio-generated" not in path.parts and path.name not in {".studio-generated", ".mcp.json", ".app.json"}]
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
        f"  default_prompt: {json.dumps(f'Use {display_name} for this bounded software task.')}",
        "",
    ]).encode("utf-8")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            relative = path.relative_to(source).as_posix()
            zip_entry(archive, f"{root_name}/{relative}", path.read_bytes())
        zip_entry(archive, f"{root_name}/SKILL.md", wrapper)
        zip_entry(archive, f"{root_name}/agents/openai.yaml", openai_yaml)


def package_chatgpt(catalog: dict[str, Any], package_info: dict[str, dict[str, Any]]) -> dict[str, str]:
    root = ROOT / "dist" / "chatgpt"
    reset_owned(root)
    hashes: dict[str, str] = {}
    for plugin_id, info in package_info.items():
        output = root / "studio.zip" if plugin_id == "studio-delivery" else root / "satellites" / f"{plugin_id}.zip"
        zip_package(ROOT / "generated" / "codex" / "plugins" / plugin_id, plugin_id, output, info["display_name"])
        hashes[str(output.relative_to(ROOT)).replace("\\", "/")] = sha256(output)
    write_json(root / "package-source.json", {"schema": "studio.chatgpt-packages/v2", "version": catalog["suite"]["version"], "default": "dist/chatgpt/studio.zip", "mcp_declared": False, "packages": hashes})
    return hashes


def render_catalog_outputs(catalog: dict[str, Any], package_info: dict[str, dict[str, Any]], archive_hashes: dict[str, str]) -> None:
    generated = ROOT / "generated" / "catalog"
    reset_owned(generated)
    write_json(generated / "package-table.json", {"schema": "studio.package-table/v2", "version": catalog["suite"]["version"], "packages": package_info})
    write_json(generated / "compatibility-aliases.json", {"schema": "studio.compatibility/v2", "version": catalog["suite"]["version"], "aliases": [{"package": p["id"], "display_name": p["display_name"], "aliases": p["legacy_aliases"]} for p in catalog["plugins"]]})
    write_json(generated / "archive-hashes.json", {"schema": "studio.archive-hashes/v2", "version": catalog["suite"]["version"], "archives": archive_hashes})
    source_files: dict[str, str] = {"catalog/studio.yaml": sha256(CATALOG_PATH)}
    index = skill_index(catalog)
    for skill_id, skill in index.items():
        source = ROOT / "skills" / "studio" / skill_id if skill.get("generated") else ROOT / skill["source"]
        for path in sorted(source.rglob("*")):
            if path.is_file():
                source_files[str(path.relative_to(ROOT)).replace("\\", "/")] = sha256(path)
    write_json(generated / "source-manifest.json", {"schema": "studio.source-manifest/v2", "version": catalog["suite"]["version"], "files": source_files, "copied_files": [], "modifications": "Generated packages copy repository-owned source skills; no third-party files or text are copied."})
    lines = ["# Studio V2 package table", "", "Generated from `catalog/studio.yaml`.", "", "| Package | Display name | Skills | Legacy aliases |", "|---|---|---:|---|"]
    for info in package_info.values():
        lines.append(f"| `{info['path']}` | {info['display_name']} | {len(info['skills'])} | {', '.join(info['legacy_aliases'])} |")
    write_text(generated / "package-table.md", "\n".join(lines) + "\n")


def generate_routing_cases(catalog: dict[str, Any]) -> None:
    path = ROOT / "evals" / "routing" / "cases.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    for skill in catalog["generated_skills"]:
        existing[skill["id"]] = {
            "positive": f"Use ${skill['id']} to {skill['focus']}.",
            "negative": "Rename an unrelated file and do not plan or review a software workflow.",
            "ambiguous": "I have a software idea; help me figure out the next step.",
        }
    write_json(path, dict(sorted(existing.items())))


def generate_seeded_fixtures(catalog: dict[str, Any]) -> None:
    root = ROOT / "evals" / "studio"
    reset_owned(root)
    write_json(root / "valid-work-package.json", {"document_id": "WP-001", "project_id": "PRJ-SD-001", "wp_id": "WP-SD-001", "status": "FROZEN", "snapshot_id": "SNAP-001", "base_sha": "d697efc16d86835ff3941f54b05e560b91a4a125", "primary_outcome": "Validate one bounded Studio package build.", "requirements": ["REQ-001"], "allowed_paths": ["scripts/", "catalog/"], "forbidden_paths": [".codex/", "secrets/"], "scope_budget": {"primary_outcomes": 1, "subsystems": 2, "new_dependencies": 0}, "acceptance": ["generator exits zero"], "verification": [{"level": "E2", "command": "python scripts/build_studio.py"}], "non_goals": ["merge", "release"], "stop_conditions": ["base SHA changes"], "rollback": "revert branch", "handoff_requirements": ["head SHA", "evidence"]})
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="validate the catalog and generated package shape without rewriting outputs")
    parser.add_argument("--render-icons", action="store_true", help="regenerate the checked-in Opal Seed raster and vector source assets before packaging")
    args = parser.parse_args()
    catalog = load_catalog()
    if args.check_only:
        print("PASS: Studio catalog is structurally valid")
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
