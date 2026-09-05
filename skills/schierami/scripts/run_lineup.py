#!/usr/bin/env python3
"""Single deterministic entry point with an observable execution report.

This dispatcher never creates forecasts, probabilities, rules or scenarios. It chooses
only among deterministic operations already supported by the supplied payload.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from _core import ContractError, reject_unknown, require_array, require_object, require_string
from evaluate_lineups import evaluate
from optimize_lineup import optimize
from score_scenario import score
from validate_lineup import validate

TOP = {"payload", "checks", "blockers"}
CHECK = {"name", "status", "source", "note"}
BLOCKER = {"fact", "blocks", "flip_condition"}
STATUSES = {"done", "blocked", "not_applicable"}


def emit(obj: dict[str, Any], code: int) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def trace(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks = []
    for i, raw in enumerate(require_array(data.get("checks", []), "$.checks")):
        p = f"$.checks[{i}]"
        row = require_object(raw, p)
        reject_unknown(row, CHECK, p)
        if "name" not in row or "status" not in row:
            raise ContractError(f"{p} requires name and status")
        name = require_string(row["name"], p + ".name")
        status = require_string(row["status"], p + ".status")
        if status not in STATUSES:
            raise ContractError(f"{p}.status must be done, blocked or not_applicable")
        checks.append({"name": name, "status": status, "source": row.get("source"), "note": row.get("note")})
    blockers = []
    for i, raw in enumerate(require_array(data.get("blockers", []), "$.blockers")):
        p = f"$.blockers[{i}]"
        row = require_object(raw, p)
        reject_unknown(row, BLOCKER, p)
        if "fact" not in row or "blocks" not in row:
            raise ContractError(f"{p} requires fact and blocks")
        blocks = [require_string(x, p + ".blocks[]") for x in require_array(row["blocks"], p + ".blocks")]
        if not blocks:
            raise ContractError(f"{p}.blocks must not be empty")
        blockers.append({"fact": require_string(row["fact"], p + ".fact"), "blocks": blocks, "flip_condition": row.get("flip_condition")})
    return checks, blockers


def dispatch(payload: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    keys = set(payload)
    if {"roster", "candidates", "scenarios", "rules", "lineup_rules"}.issubset(keys):
        result = evaluate(payload)
        return "scenario_candidate_optimum", "evaluate_lineups.py", result
    if keys == {"roster", "projections", "rules"}:
        result = optimize(payload)
        return "exact_additive_optimum", "optimize_lineup.py", result
    if keys == {"roster", "lineup", "rules"}:
        result = validate(payload)
        return "deterministic_validation_scoring", "validate_lineup.py", result
    if keys == {"starters", "bench", "rules"}:
        result = score(payload)
        return "deterministic_validation_scoring", "score_scenario.py", result
    return "qualitative_conditional", "", {"ok": True, "contract": None, "message": "No deterministic contract exactly matches the supplied payload; continue with explicit conditional reasoning."}


def run(data: object) -> dict[str, Any]:
    top = require_object(data, "$")
    reject_unknown(top, TOP, "$")
    if "payload" not in top:
        raise ContractError("$.payload is required")
    payload = require_object(top["payload"], "$.payload")
    checks, blockers = trace(top)
    mode, script, result = dispatch(payload)
    optimality = result.get("optimality") if isinstance(result, dict) else None
    report = {
        "decision_mode": mode,
        "checks": checks,
        "blockers": blockers,
        "execution": {"script_ran": script or None, "contract": result.get("contract"), "optimality": optimality},
    }
    return {"ok": bool(result.get("ok", False)), "result": result, "run_report": report}


def main() -> None:
    try:
        out = run(json.load(sys.stdin))
    except (json.JSONDecodeError, ContractError, KeyError, TypeError) as exc:
        emit({"ok": False, "message": str(exc)}, 1)
    emit(out, 0 if out["ok"] else 2)


if __name__ == "__main__":
    main()
