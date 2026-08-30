#!/usr/bin/env python3
"""High-confidence secret and packaged-path checks with no extra dependency."""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".svg", ".toml",
    ".ts", ".txt", ".yaml", ".yml",
}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{36,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
}
FORBIDDEN_NAMES = {".env", "credentials.json", "id_rsa", "id_ed25519"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def tracked_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return [ROOT / item.decode("utf-8") for item in output.split(b"\0") if item]


def check_tracked_sources(paths: list[Path]) -> None:
    for path in paths:
        relative = path.relative_to(ROOT)
        if path.name.lower() in FORBIDDEN_NAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            fail(f"tracked credential-like file: {relative.as_posix()}")
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"{label} pattern in {relative.as_posix()}")


def check_archives(paths: list[Path]) -> None:
    for archive in (path for path in paths if path.suffix.lower() == ".zip"):
        with zipfile.ZipFile(archive) as bundle:
            for entry in bundle.infolist():
                name = entry.filename
                parts = PurePosixPath(name.replace("\\", "/")).parts
                if not name or name.startswith(("/", "\\")) or ".." in parts or ":" in parts[0]:
                    fail(f"unsafe archive path in {archive.relative_to(ROOT)}: {name!r}")
                mode = (entry.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    fail(f"archive symlink in {archive.relative_to(ROOT)}: {name}")


def main() -> None:
    paths = tracked_files()
    check_tracked_sources(paths)
    check_archives(paths)
    print(f"PASS: {len(paths)} tracked paths scanned; packaged paths are traversal-safe")


if __name__ == "__main__":
    main()
