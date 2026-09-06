#!/usr/bin/env python3
"""Single deterministic entry point with an observable execution report.

The dispatcher never invents forecasts, probabilities or league rules. For a
full-lineup request it also enforces a completion preflight so an agent cannot
silently substitute qualitative prose for an available quantitative attempt.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from _core import ContractError, reject_unknown, require_array, require_object, require_string
from evaluate_lineups import evaluate
from run_forecast import run as run_forecast
from forecast_core import read_request
from optimize_lineup import optimize
from score_scenario import score
from validate_lineup import validate

TOP = {"payload", "checks", "blockers", "request"}
REQUEST = {"kind"}
REQUEST_KINDS = {"full_lineup", "narrow"}
CHECK = {"name", "status", "source", "note"}
BLOCKER = {"fact", "blocks", "flip_condition"}
STATUSES = {"done", "blocked", "not_applicable"}
FULL_LINEUP_CHECKS = (
    "roster_read",
    "matchday_mapping",
    "formation_rules",
    "substitution_rules",
    "modifier_rules",
    "captain_rules",
    "data_quality",
    "availability_evidence",
    "candidate_screening",
    "deterministic_calculation",
)
CALCULATION_BLOCKS = {"deterministic_calculation", "quantitative_comparison"}


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


def request_kind(data: dict[str, Any]) -> str | None:
    raw = data.get("request")
    if raw is None:
        return None
    row = require_object(raw, "$.request")
    reject_unknown(row, REQUEST, "$.request")
    if "kind" not in row:
        raise ContractError("$.request.kind is required")
    kind = require_string(row["kind"], "$.request.kind")
    if kind not in REQUEST_KINDS:
        raise ContractError("$.request.kind must be full_lineup or narrow")
    return kind


def dispatch(payload: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    keys = set(payload)
    if "forecast_bundle" in keys:
        result = run_forecast(payload)
        return "scenario_candidate_optimum", "run_forecast.py", result
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
    return "qualitative_conditional", "", {
        "ok": True,
        "contract": None,
        "message": "No deterministic contract exactly matches the supplied payload; preserve explicit blockers and conditional reasoning.",
    }


def completion(
    kind: str | None,
    checks: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    script: str,
) -> dict[str, Any]:
    if kind != "full_lineup":
        return {
            "status": "not_enforced",
            "claim_scope": None,
            "missing_checks": [],
            "issues": [],
            "quantitative_attempted": bool(script),
        }

    by_name = {row["name"]: row for row in checks}
    missing = [name for name in FULL_LINEUP_CHECKS if name not in by_name]
    issues: list[str] = []
    calc = by_name.get("deterministic_calculation")
    blocked_targets = {target for row in blockers for target in row["blocks"]}
    quantitative_blocked = bool(blocked_targets & CALCULATION_BLOCKS)

    if script:
        if calc is not None and calc["status"] != "done":
            issues.append("deterministic_calculation must be done when a deterministic script ran")
    else:
        if calc is not None and calc["status"] == "done":
            issues.append("deterministic_calculation cannot be done when no deterministic script ran")
        if calc is not None and calc["status"] == "not_applicable":
            issues.append("deterministic_calculation cannot be not_applicable for a full lineup")
        if not quantitative_blocked:
            issues.append(
                "a full lineup without deterministic execution requires an explicit blocker for deterministic_calculation or quantitative_comparison"
            )

    if missing or issues:
        status = "blocked"
        scope = "incomplete"
    elif script and blockers:
        status = "complete"
        scope = "partial_quantitative"
    elif script:
        status = "complete"
        scope = "full_rule_quantitative"
    else:
        status = "complete"
        scope = "conditional_only"

    return {
        "status": status,
        "claim_scope": scope,
        "missing_checks": missing,
        "issues": issues,
        "quantitative_attempted": bool(script),
        "quantitative_blocked": quantitative_blocked,
    }


def run(data: object) -> dict[str, Any]:
    top = require_object(data, "$")
    reject_unknown(top, TOP, "$")
    if "payload" not in top:
        raise ContractError("$.payload is required")
    payload = require_object(top["payload"], "$.payload")
    kind = request_kind(top)
    checks, blockers = trace(top)
    mode, script, result = dispatch(payload)
    optimality = result.get("optimality") if isinstance(result, dict) else None
    gate = completion(kind, checks, blockers, script)
    report = {
        "request_kind": kind,
        "decision_mode": mode,
        "checks": checks,
        "blockers": blockers,
        "execution": {"script_ran": script or None, "contract": result.get("contract"), "optimality": optimality},
        "completion": gate,
    }
    return {"ok": bool(result.get("ok", False)), "result": result, "run_report": report}


def main() -> None:
    try:
        out = run(read_request())
    except (json.JSONDecodeError, ContractError, KeyError, TypeError) as exc:
        emit({"ok": False, "message": str(exc)}, 1)
    emit(out, 0 if out["ok"] else 2)


if __name__ == "__main__":
    main()
