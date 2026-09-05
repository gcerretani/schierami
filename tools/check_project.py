#!/usr/bin/env python3
"""Validate Schierami repository structure and local documentation."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")
RELEASE_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", re.M)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)


def load_manifest(root: Path = ROOT) -> dict:
    data = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if data.get("name") != "schierami":
        raise ValueError("plugin name must be schierami")
    if not VERSION_RE.fullmatch(str(data.get("version", ""))):
        raise ValueError("plugin version must use MAJOR.MINOR.PATCH")
    if data.get("skills") != "./skills/":
        raise ValueError("plugin skills path must be ./skills/")
    if data.get("license") != "MIT":
        raise ValueError("plugin license metadata must be MIT")
    return data


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    fields: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or ":" not in raw:
            raise ValueError("skill frontmatter must use simple key: value lines")
        key, value = raw.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    if set(fields) != {"name", "description"}:
        raise ValueError("skill frontmatter must contain only name and description")
    if fields["name"] != "schierami" or not fields["description"]:
        raise ValueError("invalid skill name or description")
    if len(fields["description"]) > 1024:
        raise ValueError("skill description exceeds 1024 characters")
    return fields


def release_notes(root: Path, version: str) -> str:
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    matches = [m for m in RELEASE_RE.finditer(text) if m.group(1) == version]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one dated changelog section for {version}")
    start = matches[0].end()
    next_heading = re.search(r"^## ", text[start:], flags=re.M)
    end = start + next_heading.start() if next_heading else len(text)
    body = text[start:end].strip()
    if not body:
        raise ValueError(f"empty changelog section for {version}")
    return body


def local_link_errors(root: Path) -> list[str]:
    errors: list[str] = []
    markdown = list(root.glob("*.md"))
    for directory in ("docs", "evals", "skills"):
        base = root / directory
        if base.exists():
            markdown.extend(base.rglob("*.md"))
    for path in markdown:
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        targets = re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text)
        targets += re.findall(r"^\[[^\]\n]+\]:\s+(\S+)", text, flags=re.M)
        for target in targets:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            candidate = (path.parent / unquote(parsed.path)).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.exists():
                errors.append(f"{path.relative_to(root)}: missing local link {target}")
    return errors


def check(root: Path = ROOT) -> dict:
    root = root.resolve()
    data = load_manifest(root)
    required = [
        "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE",
        ".codex-plugin/plugin.json", ".github/workflows/test.yml",
        "docs/README.md", "docs/installation.md", "docs/development.md",
        "docs/releases.md", "docs/submission.md", "docs/privacy.md",
        "docs/terms.md", "docs/support.md", "evals/README.md",
        "skills/schierami/SKILL.md", "skills/schierami/agents/openai.yaml",
        "skills/schierami/assets/schierami-icon.svg", "tests", "tools",
    ]
    errors = [f"missing {item}" for item in required if not (root / item).exists()]

    skill = root / "skills/schierami"
    try:
        front = parse_skill_frontmatter(skill / "SKILL.md")
        if front["name"] != data["name"]:
            errors.append("skill and plugin names differ")
    except ValueError as exc:
        errors.append(str(exc))

    agent = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    display = re.search(r'^\s*display_name:\s*["\']?([^"\'\n]+)', agent, re.M)
    short = re.search(r'^\s*short_description:\s*["\']?([^"\'\n]+)', agent, re.M)
    if not display or display.group(1).strip() != data["interface"]["displayName"]:
        errors.append("plugin and skill display names differ")
    if not short or short.group(1).strip() != data["interface"]["shortDescription"]:
        errors.append("plugin and skill short descriptions differ")

    icon = data["interface"].get("composerIcon")
    if not isinstance(icon, str) or not icon.startswith("./") or not (root / icon[2:]).is_file():
        errors.append("composerIcon must point to an existing repository file")

    if len(list((root / "skills").rglob("SKILL.md"))) != 1:
        errors.append("this repository must contain exactly one skill")
    if (skill / "tests").exists():
        errors.append("maintainer tests must live outside the installable skill")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    releases = list(RELEASE_RE.finditer(changelog))
    versions = [m.group(1) for m in releases]
    if not versions or versions[0] != data["version"]:
        errors.append("newest dated changelog version must match the manifest")
    if len(versions) != len(set(versions)):
        errors.append("changelog versions must be unique")
    if changelog.count("## [Unreleased]") != 1:
        errors.append("changelog must contain exactly one Unreleased section")
    for item in releases:
        dt.date.fromisoformat(item.group(2))
    try:
        release_notes(root, data["version"])
    except ValueError as exc:
        errors.append(str(exc))

    errors.extend(local_link_errors(root))
    if errors:
        raise ValueError("\n".join(errors))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        data = check(args.root)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Project check failed:\n{exc}\n")
    print(f"Project checks passed: {data['name']} {data['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
