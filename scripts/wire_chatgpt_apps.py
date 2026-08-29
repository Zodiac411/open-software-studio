#!/usr/bin/env python3
"""Wire registered ChatGPT MCP app IDs into the seven plugin packages.

ChatGPT creates the ``plugin_asdk_app_...`` identifier after a developer-mode
MCP connection is created. IDs are deliberately not committed until that
connection exists. This script accepts either one shared ID or a JSON mapping
from plugin slug to ID, then updates only the app maps.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = (
    "project-architect",
    "interface-studio",
    "engineering-guard",
    "research-engineer",
    "project-docs",
    "web-app-builder",
    "execution-guard",
)
APP_ID = re.compile(r"^plugin_asdk_app_[A-Za-z0-9]+$")


def validate_id(value: str) -> str:
    value = value.strip()
    if not APP_ID.fullmatch(value):
        raise SystemExit("App IDs must match plugin_asdk_app_<identifier>.")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="Use one registered app ID for every plugin.")
    group.add_argument("--map", type=Path, help="JSON file mapping plugin slugs to app IDs.")
    args = parser.parse_args()

    if args.id:
        mapping = {slug: validate_id(args.id) for slug in PLUGINS}
    else:
        payload = json.loads(args.map.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise SystemExit("The mapping file must contain a JSON object.")
        missing = [slug for slug in PLUGINS if slug not in payload]
        if missing:
            raise SystemExit(f"Missing app IDs for: {', '.join(missing)}")
        mapping = {slug: validate_id(str(payload[slug])) for slug in PLUGINS}

    for slug in PLUGINS:
        app_path = ROOT / "plugins" / slug / ".app.json"
        app_key = f"open-software-studio-{slug}"
        app_path.write_text(json.dumps({"apps": {app_key: {"id": mapping[slug]}}}, indent=2) + "\n", encoding="utf-8")

    print(f"Wired ChatGPT app mappings for {len(PLUGINS)} plugins.")


if __name__ == "__main__":
    main()
