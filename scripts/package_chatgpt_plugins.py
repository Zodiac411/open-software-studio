#!/usr/bin/env python3
"""Build skills-only Open Software Studio plugin bundles for ChatGPT upload."""

from __future__ import annotations

import argparse
import json
import re
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAMES = (
    "project-architect",
    "interface-studio",
    "engineering-guard",
    "research-engineer",
    "project-docs",
    "web-app-builder",
)
DISPLAY_NAMES = {
    "project-architect": "Project Architect",
    "interface-studio": "Interface Studio",
    "engineering-guard": "Engineering Guard",
    "research-engineer": "Research Engineer",
    "project-docs": "Project Docs",
    "web-app-builder": "Web App Builder",
}
COLORS = {
    "project-architect": "#B69559",
    "interface-studio": "#D59A75",
    "engineering-guard": "#6BA69B",
    "research-engineer": "#416B8B",
    "project-docs": "#AD7941",
    "web-app-builder": "#46789A",
}
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD = re.compile(r"(?m)^(name|description):\s*(.+?)\s*$")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_ICON_BYTES = 10 * 1024


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def parse_skill(skill_file: Path) -> tuple[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        fail(f"{skill_file}: missing YAML frontmatter")
    fields = {name: value.strip().strip('"\'') for name, value in FIELD.findall(match.group(1))}
    if not fields.get("name") or not fields.get("description"):
        fail(f"{skill_file}: missing name or description")
    return fields["name"], fields["description"]


def validate_icon(icon: Path) -> None:
    raw = icon.read_bytes() if icon.is_file() else b""
    if len(raw) < 29 or raw[:8] != PNG_SIGNATURE or raw[12:16] != b"IHDR":
        fail(f"{icon}: must be a PNG")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", raw[16:26])
    if width != height or width == 0 or color_type not in (2, 6):
        fail(f"{icon}: must be a square true-color PNG")
    if bit_depth != 8 or icon.stat().st_size > MAX_ICON_BYTES:
        fail(f"{icon}: must use 8-bit color and stay below 10 KB")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def openai_yaml(display_name: str, skill_name: str, description: str, color: str) -> str:
    short = description.strip()
    if len(short) > 64:
        short = short[:61].rstrip() + "..."
    prompt = f"Use ${skill_name} to {description.rstrip('.')}"
    return "\n".join(
        (
            "interface:",
            f"  display_name: {yaml_string(display_name)}",
            f"  short_description: {yaml_string(short)}",
            '  icon_small: "./assets/chatgpt-icon.png"',
            '  icon_large: "./assets/chatgpt-icon.png"',
            f"  brand_color: {yaml_string(color)}",
            f"  default_prompt: {yaml_string(prompt)}",
            "",
        )
    )


def wrapper_skill(plugin_name: str, skill_names: list[str]) -> str:
    display_name = DISPLAY_NAMES[plugin_name]
    router = next((name for name in skill_names if name.endswith("-router")), skill_names[0])
    lines = [
        "---",
        f"name: open-software-studio-{plugin_name}",
        f"description: Use the {display_name} plugin bundle for focused software work without a tunnel or MCP connection.",
        "---",
        f"# {display_name}",
        "",
        "This is a skills-only Open Software Studio plugin bundle. No tunnel,",
        "localhost service, app connector, or API key is required.",
        "",
        f"Start with `skills/{router}/SKILL.md`, then read only the specialist",
        "Skill named by that router. The complete specialist set is included",
        "under `skills/` so the bundle works as a plugin in Codex and as an",
        "uploadable Agent Skill package in ChatGPT.",
        "",
        "Included specialists:",
    ]
    lines.extend(f"- `skills/{name}/SKILL.md`" for name in skill_names)
    lines.extend(
        (
            "",
            "Keep the plugin boundary intact: produce the artifact owned by",
            "this plugin, and hand off implementation or review work to the",
            "next Open Software Studio plugin when appropriate.",
            "",
        )
    )
    return "\n".join(lines)


def package_plugin(plugin_name: str, output_dir: Path) -> Path:
    plugin_root = ROOT / "plugins" / plugin_name
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    icon = plugin_root / "assets" / "chatgpt-icon.png"
    if not manifest_path.is_file():
        fail(f"{plugin_name}: missing plugin manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != plugin_name or manifest.get("skills") != "./skills/":
        fail(f"{plugin_name}: manifest must expose skills")
    if "mcpServers" in manifest or "apps" in manifest:
        fail(f"{plugin_name}: MCP and app surfaces are not allowed in ChatGPT bundles")
    validate_icon(icon)

    skill_dirs = sorted(path for path in (plugin_root / "skills").iterdir() if path.is_dir())
    if not skill_dirs:
        fail(f"{plugin_name}: no skills")
    skill_names: list[str] = []
    skill_metadata: dict[str, tuple[str, str]] = {}
    for skill_dir in skill_dirs:
        skill_name, description = parse_skill(skill_dir / "SKILL.md")
        skill_names.append(skill_dir.name)
        skill_metadata[skill_dir.name] = (skill_name, description)

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{plugin_name}.zip"
    root = Path(plugin_name)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(manifest_path, (root / ".codex-plugin" / "plugin.json").as_posix())
        for path in sorted(plugin_root.rglob("*")):
            if not path.is_file() or path == manifest_path:
                continue
            relative = path.relative_to(plugin_root)
            if relative.name in {".mcp.json", ".app.json"}:
                continue
            if relative.parts and relative.parts[0] == "assets" and (
                relative.name in {"icon.png", "plugin-icon.png"} or relative.suffix.lower() == ".jpg"
            ):
                continue
            if "__pycache__" in relative.parts or path.suffix == ".pyc":
                continue
            archive.write(path, (root / relative).as_posix())

        archive.writestr((root / "SKILL.md").as_posix(), wrapper_skill(plugin_name, skill_names))
        archive.writestr(
            (root / "agents" / "openai.yaml").as_posix(),
            openai_yaml(DISPLAY_NAMES[plugin_name], f"open-software-studio-{plugin_name}", f"route the {DISPLAY_NAMES[plugin_name]} workflow", COLORS[plugin_name]),
        )
        for skill_dir_name in skill_names:
            skill_name, description = skill_metadata[skill_dir_name]
            archive.writestr(
                (root / "skills" / skill_dir_name / "agents" / "openai.yaml").as_posix(),
                openai_yaml(f"{DISPLAY_NAMES[plugin_name]}: {skill_name.replace('-', ' ')}", skill_name, description, COLORS[plugin_name]),
            )
            archive.write(
                icon,
                (root / "skills" / skill_dir_name / "assets" / "chatgpt-icon.png").as_posix(),
            )
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "chatgpt-plugins")
    parser.add_argument("--plugin", choices=PLUGIN_NAMES, action="append", dest="plugins")
    args = parser.parse_args()
    selected = args.plugins or list(PLUGIN_NAMES)
    output_dir = args.output.resolve()
    archives = [package_plugin(name, output_dir) for name in selected]
    print(f"Packaged {len(archives)} ChatGPT plugin bundles in {output_dir}")
    for archive in archives:
        print(f"- {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
