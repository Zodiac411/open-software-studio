#!/usr/bin/env python3
"""Validate the catalog, generated packages, portable archive, and seeded gates."""

from __future__ import annotations

import json
import struct
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
RESULT_STATES = ["PASS", "PASS_WITH_LIMITATIONS", "BLOCKED", "NOT_RUN", "UNPROVEN"]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path}: expected an object")
    return value


def check_png(path: Path, expected: int | None = None, enforce_budget: bool = True) -> None:
    raw = path.read_bytes()
    if raw[:8] != PNG_SIGNATURE or raw[12:16] != b"IHDR" or len(raw) < 26:
        fail(f"{path}: invalid PNG")
    width, height, depth, color = struct.unpack(">IIBB", raw[16:26])
    if width != height or depth != 8 or color not in (2, 6):
        fail(f"{path}: expected square true-color PNG")
    if expected is not None and width != expected:
        fail(f"{path}: expected {expected}px, got {width}px")
    if enforce_budget and path.stat().st_size > 10 * 1024:
        fail(f"{path}: exceeds the 10KB icon budget")


def check_manifest(path: Path, plugin: dict[str, Any]) -> set[str]:
    manifest = read_json(path)
    if manifest.get("name") != plugin["id"] or manifest.get("version") != "2.0.0":
        fail(f"{path}: package identity/version")
    if manifest.get("skills") != "./skills/":
        fail(f"{path}: skills path")
    if "mcpServers" in manifest or "apps" in manifest:
        fail(f"{path}: generated package declares MCP/app surfaces")
    interface = manifest.get("interface", {})
    if interface.get("displayName") != plugin["display_name"] or not interface.get("defaultPrompt"):
        fail(f"{path}: interface display name/default prompt")
    if not {"composerIcon", "logo", "logoDark"}.issubset(interface):
        fail(f"{path}: icon fields")
    package = path.parent.parent
    for field in ("composerIcon", "logo", "logoDark"):
        asset = package / interface[field].removeprefix("./")
        if not asset.is_file():
            fail(f"{path}: missing {field}: {asset}")
        check_png(asset)
    return {item.parent.name for item in (package / "skills").glob("*/SKILL.md")}


def main() -> None:
    catalog = read_json(ROOT / "catalog" / "studio.yaml")
    if catalog.get("schema") != "studio.catalog/v2":
        fail("catalog schema")
    if catalog.get("result_states") != RESULT_STATES:
        fail("result state vocabulary")
    plugins = catalog.get("plugins", [])
    if len(plugins) != 9:
        fail("catalog must describe nine packages")
    generated = catalog.get("generated_skills", [])
    legacy = catalog.get("legacy_skills", [])
    skill_index = {item["id"]: item for item in generated + legacy}
    if len(skill_index) != len(generated) + len(legacy):
        fail("catalog skill IDs are duplicated")
    if "CURRENT_STATE" not in catalog.get("artifact_templates", {}):
        fail("CURRENT_STATE must be a catalog artifact template")

    marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    if marketplace.get("name") != "studio-v2" or {item.get("name") for item in marketplace.get("plugins", [])} != {item["id"] for item in plugins}:
        fail("generated marketplace does not match catalog")

    package_skill_sets: dict[str, set[str]] = {}
    for plugin in plugins:
        package = ROOT / "generated" / "codex" / "plugins" / plugin["id"]
        manifest_path = package / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            fail(f"{plugin['id']}: generated manifest missing")
        actual = check_manifest(manifest_path, plugin)
        refs = set(skill_index) if plugin.get("skills") == "all" else set(plugin.get("skills", []))
        if actual != refs:
            fail(f"{plugin['id']}: skill set differs from catalog")
        package_skill_sets[plugin["id"]] = actual
        dist_package = ROOT / "dist" / "marketplace" / "plugins" / plugin["id"]
        if not (dist_package / ".codex-plugin" / "plugin.json").is_file():
            fail(f"{plugin['id']}: marketplace distribution missing")

    studio = ROOT / "dist" / "codex" / "studio"
    if not (studio / ".codex-plugin" / "plugin.json").is_file():
        fail("Codex umbrella distribution missing")
    package_source = read_json(ROOT / "dist" / "chatgpt" / "package-source.json")
    if package_source.get("default") != "dist/chatgpt/studio.zip" or package_source.get("mcp_declared") is not False:
        fail("ChatGPT package source contract")
    archive = ROOT / "dist" / "chatgpt" / "studio.zip"
    if not archive.is_file():
        fail("dist/chatgpt/studio.zip missing")
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        if "studio/SKILL.md" not in names or "studio/agents/openai.yaml" not in names:
            fail("ChatGPT archive is not skills-first")
        if any(name.endswith((".mcp.json", ".app.json")) for name in names):
            fail("ChatGPT archive contains a server/app declaration")
        for name in names:
            info = bundle.getinfo(name)
            if info.date_time != (1980, 1, 1, 0, 0, 0):
                fail(f"ChatGPT archive entry is not deterministic: {name}")
            if name.endswith((".json", ".yaml", ".md")) and b"mcpServers" in bundle.read(name):
                fail(f"ChatGPT archive declares MCP: {name}")

    icon_root = ROOT / "brand" / "icon-system" / "generated"
    roles = catalog["icon_system"]["roles"]
    for role in roles:
        for size in (24, 32, 48, 64, 128, 256, 512):
            path = icon_root / f"{role}-{size}.png"
            if not path.is_file():
                fail(f"missing icon: {path}")
            check_png(path, size, enforce_budget=False)
    if not (ROOT / "brand" / "icon-system" / "contact-sheet.png").is_file():
        fail("icon contact sheet missing")

    cases = read_json(ROOT / "evals" / "routing" / "cases.json")
    if set(cases) != set(skill_index):
        fail("routing cases do not cover the catalog skill index")
    seeded = ROOT / "evals" / "studio"
    for name in ("valid-work-package.json", "invalid-self-accept-review.json", "golden-review-trap.json", "benchmark-cases.json"):
        if not (seeded / name).is_file():
            fail(f"seeded Studio gate missing: {name}")
    invalid_review = read_json(seeded / "invalid-self-accept-review.json")
    if invalid_review.get("reviewer_role") != "executor" or invalid_review.get("disposition") != "ACCEPT":
        fail("self-accept review trap lost its invalid shape")
    benchmarks = json.loads((seeded / "benchmark-cases.json").read_text(encoding="utf-8"))
    if len(benchmarks) < 6 or {item.get("family") for item in benchmarks} != {"catalog", "state", "evidence", "permissions", "review", "rollback"}:
        fail("seeded Studio benchmark coverage")

    legacy_dirs = [ROOT / "plugins" / item["id"] for item in catalog["legacy_plugins"]]
    if not all(path.is_dir() for path in legacy_dirs):
        fail("legacy package source directories must remain available")
    print(f"PASS: catalog, 9 generated packages, {len(skill_index)} skills, V2 schemas, icons, archive, routing, and seeded gates validated")


if __name__ == "__main__":
    main()
