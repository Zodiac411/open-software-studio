#!/usr/bin/env python3
"""Verify that a clean checkout rebuild leaves every repository byte unchanged."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", "runtime"}


def digest_tree(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        files[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def run_build(root: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(root / "scripts" / "build_studio.py")],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(f"FAIL: clean build exited {completed.returncode}: {completed.stdout}{completed.stderr}")


def changed(before: dict[str, str], after: dict[str, str]) -> list[str]:
    names = sorted(set(before) | set(after))
    return [name for name in names if before.get(name) != after.get(name)]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="studio-repro-") as temporary:
        checkout = Path(temporary) / "checkout"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(*IGNORED_PARTS))
        before = digest_tree(checkout)
        run_build(checkout)
        first = digest_tree(checkout)
        run_build(checkout)
        second = digest_tree(checkout)
    drift = changed(before, first) + changed(first, second)
    if drift:
        unique = list(dict.fromkeys(drift))
        raise SystemExit(f"FAIL: clean rebuild changed {len(unique)} files: {', '.join(unique[:12])}")
    print("PASS: two clean-checkout builds reproduced every repository byte")


if __name__ == "__main__":
    main()
