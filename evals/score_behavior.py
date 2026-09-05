#!/usr/bin/env python3
"""Score observable Schierami behavioral runs against synthetic expectations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def contains_fragment(values: list[str], fragment: str) -> bool:
    needle = fragment.casefold()
    return any(needle in str(value).casefold() for value in values)


def score_case(case: dict[str, Any], run: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expect = case.get("expect", {})
    if "decision_modes" in expect and run.get("decision_mode") not in expect["decision_modes"]:
        errors.append(f"decision_mode={run.get('decision_mode')!r} not in {expect['decision_modes']!r}")

    checks = run.get("checks", {})
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
        checks = {}
    for name, allowed in expect.get("checks", {}).items():
        if checks.get(name) not in allowed:
            errors.append(f"check {name!r}={checks.get(name)!r} not in {allowed!r}")

    asked = run.get("asked_for", [])
    if not isinstance(asked, list):
        errors.append("asked_for must be an array")
        asked = []
    for item in expect.get("must_ask_for", []):
        if item not in asked:
            errors.append(f"required question missing: {item}")
    for item in expect.get("must_not_ask_for", []):
        if item in asked:
            errors.append(f"unnecessary/forbidden question: {item}")

    scripts = run.get("scripts_ran", [])
    if not isinstance(scripts, list):
        errors.append("scripts_ran must be an array")
        scripts = []
    for item in expect.get("must_run_scripts", []):
        if item not in scripts:
            errors.append(f"required deterministic execution missing: {item}")

    claims = run.get("claims", [])
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        claims = []
    for fragment in expect.get("required_claim_fragments", []):
        if not contains_fragment(claims, fragment):
            errors.append(f"required claim fragment missing: {fragment!r}")
    for fragment in expect.get("forbidden_claim_fragments", []):
        if contains_fragment(claims, fragment):
            errors.append(f"forbidden claim fragment present: {fragment!r}")
    return errors


def score(cases: list[dict[str, Any]], runs: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {row.get("case_id"): row for row in runs if isinstance(row, dict)}
    results = []
    passed = 0
    for case in cases:
        cid = case["id"]
        run = by_id.get(cid)
        errors = ["missing run result"] if run is None else score_case(case, run)
        ok = not errors
        passed += int(ok)
        results.append({"case_id": cid, "ok": ok, "errors": errors})
    total = len(cases)
    return {"ok": passed == total, "passed": passed, "total": total, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", type=Path, help="JSON array of observable run results")
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    args = parser.parse_args()
    try:
        cases = load(args.cases)
        runs = load(args.runs)
        if not isinstance(cases, list) or not isinstance(runs, list):
            raise ValueError("cases and runs must both be JSON arrays")
        result = score(cases, runs)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(json.dumps({"ok": False, "message": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
