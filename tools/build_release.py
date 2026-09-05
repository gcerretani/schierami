#!/usr/bin/env python3
"""Build deterministic standalone-skill and plugin release archives."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import zipfile

try:
    from .check_project import ROOT, check, release_notes
except ImportError:
    from check_project import ROOT, check, release_notes

MAX_BYTES = 25 * 1024 * 1024
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}


def source_skill_files(root: Path) -> dict[str, bytes]:
    skill = root / "skills/schierami"
    files: dict[str, bytes] = {}
    for path in sorted(skill.rglob("*")):
        relative = path.relative_to(skill)
        if any(part in IGNORED_PARTS for part in relative.parts) or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise ValueError(f"symlinks cannot be packaged: {relative}")
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    return files


def write_zip(path: Path, members: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, content in sorted(members.items()):
                info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, content)
        if temporary.stat().st_size > MAX_BYTES:
            raise ValueError(f"{path.name} exceeds the 25 MiB package limit")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def build(root: Path = ROOT, output: Path | None = None) -> dict[str, Path]:
    root = root.resolve()
    data = check(root)
    version = data["version"]
    output = (output or root / "dist").resolve()
    if output.is_relative_to(root / "skills"):
        raise ValueError("release output must be outside the installable skill")

    skill_files = source_skill_files(root)
    license_bytes = (root / "LICENSE").read_bytes()
    version_bytes = (version + "\n").encode("utf-8")

    skill_members = {f"schierami/{name}": content for name, content in skill_files.items()}
    skill_members["schierami/LICENSE"] = license_bytes
    skill_members["schierami/VERSION"] = version_bytes

    plugin_members = {
        ".codex-plugin/plugin.json": (root / ".codex-plugin/plugin.json").read_bytes(),
        "LICENSE": license_bytes,
        "VERSION": version_bytes,
    }
    plugin_members.update({f"skills/schierami/{name}": content for name, content in skill_files.items()})

    output.mkdir(parents=True, exist_ok=True)
    skill_zip = output / "skill.zip"
    plugin_zip = output / "schierami-plugin.zip"
    write_zip(skill_zip, skill_members)
    write_zip(plugin_zip, plugin_members)

    sums = []
    for path in (skill_zip, plugin_zip):
        sums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    checksums = output / "SHA256SUMS"
    checksums.write_text("\n".join(sums) + "\n", encoding="utf-8", newline="\n")

    notes = output / "RELEASE_NOTES.md"
    notes.write_text(
        f"# Schierami v{version}\n\n{release_notes(root, version)}\n",
        encoding="utf-8",
        newline="\n",
    )
    version_file = output / "VERSION"
    version_file.write_text(version + "\n", encoding="utf-8", newline="\n")
    return {
        "skill": skill_zip,
        "plugin": plugin_zip,
        "checksums": checksums,
        "notes": notes,
        "version": version_file,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = build(args.root, args.output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")
    print(f"Built {result['skill']}")
    print(f"Built {result['plugin']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
