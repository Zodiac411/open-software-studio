#!/usr/bin/env python3
"""Create ChatGPT Skills upload ZIPs with the plugin icon embedded."""

from __future__ import annotations

import argparse
import re
import struct
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PLUGINS = (
    "project-architect",
    "interface-studio",
    "engineering-guard",
    "research-engineer",
    "project-docs",
    "web-app-builder",
    "execution-guard",
)


def validate_skill(skill_dir: Path, icon: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise SystemExit(f"{skill_dir}: missing SKILL.md")
    match = FRONTMATTER.match(skill_file.read_text(encoding="utf-8"))
    if not match or not re.search(r"(?m)^name:\s*\S+", match.group(1)) or not re.search(r"(?m)^description:\s*\S+", match.group(1)):
        raise SystemExit(f"{skill_file}: missing valid frontmatter")
    raw_icon = icon.read_bytes() if icon.is_file() else b""
    square = len(raw_icon) >= 24 and raw_icon[:8] == b"\x89PNG\r\n\x1a\n" and raw_icon[12:16] == b"IHDR" and struct.unpack(">II", raw_icon[16:24])[0] == struct.unpack(">II", raw_icon[16:24])[1]
    if not square or icon.stat().st_size > 10 * 1024:
        raise SystemExit(f"{icon}: must be a square PNG below 10 KB")


def package_skill(skill_dir: Path, icon: Path, output_dir: Path) -> Path:
    validate_skill(skill_dir, icon)
    archive_path = output_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = path.relative_to(skill_dir)
            if relative.as_posix() == "assets/plugin-icon.png":
                continue
            archive.write(path, Path(skill_dir.name, relative).as_posix())
        archive.write(icon, Path(skill_dir.name, "assets/plugin-icon.png").as_posix())
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "chatgpt-skills")
    parser.add_argument("--plugin", choices=PLUGINS, action="append", dest="plugins")
    parser.add_argument("--skill", action="append", dest="skills", help="Limit packaging to these skill directory names.")
    args = parser.parse_args()

    selected_plugins = args.plugins or list(PLUGINS)
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    wanted = set(args.skills or [])
    archives: list[Path] = []

    for plugin_name in selected_plugins:
        plugin_root = ROOT / "plugins" / plugin_name
        icon = plugin_root / "assets" / "plugin-icon.png"
        skill_dirs = sorted((plugin_root / "skills").iterdir())
        if wanted:
            skill_dirs = [path for path in skill_dirs if path.name in wanted]
        for skill_dir in skill_dirs:
            if not skill_dir.is_dir():
                continue
            archives.append(package_skill(skill_dir, icon, output_dir))

    if not archives:
        raise SystemExit("No skills selected.")
    print(f"Packaged {len(archives)} ChatGPT Skills in {output_dir}")
    for archive in archives:
        print(f"- {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
