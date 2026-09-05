#!/usr/bin/env python3
from __future__ import annotations

from decimal import Decimal
import json
import sys
from typing import Any

from _core import ContractError, decimal_number, normalize_id, reject_unknown, require_array, require_bool, require_decimal, require_int, require_object, require_string, require_string_list

ALLOWED_TOP = {"starters", "bench", "rules"}
ALLOWED_STARTER = {"player_id", "slot", "roles", "valid_vote", "fantasy_points", "base_vote"}
ALLOWED_BENCH = {"player_id", "roles", "valid_vote", "fantasy_points", "base_vote"}
ALLOWED_RULES = {"max_substitutions", "substitution_mode", "slot_eligibility", "modifiers"}
ALLOWED_MODIFIER = {"name", "type", "selectors", "thresholds", "target"}
ALLOWED_SELECTOR = {"slots", "take_best"}
ALLOWED_THRESHOLD = {"min", "points"}


def emit(obj: dict, code: int) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2)); raise SystemExit(code)


def parse_player(raw: Any, path: str, starter: bool) -> dict[str, Any]:
    row = require_object(raw, path); reject_unknown(row, ALLOWED_STARTER if starter else ALLOWED_BENCH, path)
    required = {"player_id", "roles", "valid_vote"} | ({"slot"} if starter else set())
    missing = sorted(required - set(row))
    if missing: raise ContractError(f"{path} missing required keys: {', '.join(missing)}")
    out = {"player_id": normalize_id(row["player_id"], f"{path}.player_id"), "roles": require_string_list(row["roles"], f"{path}.roles", nonempty=True), "valid_vote": require_bool(row["valid_vote"], f"{path}.valid_vote")}
    if starter: out["slot"] = require_string(row["slot"], f"{path}.slot")
    if out["valid_vote"]:
        if "fantasy_points" not in row: raise ContractError(f"{path}.fantasy_points is required when valid_vote is true")
        out["fantasy_points"] = require_decimal(row["fantasy_points"], f"{path}.fantasy_points")
    else:
        out["fantasy_points"] = require_decimal(row["fantasy_points"], f"{path}.fantasy_points") if row.get("fantasy_points") is not None else None
    out["base_vote"] = require_decimal(row["base_vote"], f"{path}.base_vote") if row.get("base_vote") is not None else None
    return out


def parse_rules(raw: Any) -> dict[str, Any]:
    rules = require_object(raw, "$.rules"); reject_unknown(rules, ALLOWED_RULES, "$.rules")
    missing = sorted({"max_substitutions", "substitution_mode", "slot_eligibility"} - set(rules))
    if missing: raise ContractError("missing rule keys: " + ", ".join(missing))
    max_subs = require_int(rules["max_substitutions"], "$.rules.max_substitutions", 0)
    mode = require_string(rules["substitution_mode"], "$.rules.substitution_mode")
    if mode != "ordered_slots": raise ContractError("only substitution_mode=ordered_slots is supported")
    eligibility = {require_string(k, "slot key"): set(require_string_list(v, f"$.rules.slot_eligibility.{k}", nonempty=True)) for k, v in require_object(rules["slot_eligibility"], "$.rules.slot_eligibility").items()}
    modifiers = []
    for i, raw_mod in enumerate(require_array(rules.get("modifiers", []), "$.rules.modifiers")):
        path = f"$.rules.modifiers[{i}]"; mod = require_object(raw_mod, path); reject_unknown(mod, ALLOWED_MODIFIER, path)
        if mod.get("type") != "threshold_average": raise ContractError(f"unsupported modifier type: {mod.get('type')}")
        name = str(mod.get("name", "unnamed")); target = mod.get("target", "self")
        if target not in {"self", "opponent"}: raise ContractError(f"unsupported modifier target: {target}")
        selectors, used_slots = [], set()
        for j, raw_sel in enumerate(require_array(mod.get("selectors", []), f"{path}.selectors")):
            sp = f"{path}.selectors[{j}]"; sel = require_object(raw_sel, sp); reject_unknown(sel, ALLOWED_SELECTOR, sp)
            if set(sel) != ALLOWED_SELECTOR: raise ContractError(f"{sp} requires slots and take_best")
            slots = require_string_list(sel["slots"], f"{sp}.slots", nonempty=True)
            overlap = used_slots.intersection(slots)
            if overlap: raise ContractError(f"modifier {name} has overlapping selector slots: {', '.join(sorted(overlap))}")
            used_slots.update(slots)
            unknown = [s for s in slots if s not in eligibility]
            if unknown: raise ContractError(f"modifier {name} references unknown slots: {', '.join(unknown)}")
            take = require_int(sel["take_best"], f"{sp}.take_best", 1)
            if take > len(slots): raise ContractError(f"{sp}.take_best exceeds number of slots")
            selectors.append({"slots": slots, "take_best": take})
        if not selectors: raise ContractError(f"modifier {name} selects no players")
        thresholds, minima = [], set()
        for j, raw_t in enumerate(require_array(mod.get("thresholds", []), f"{path}.thresholds")):
            tp = f"{path}.thresholds[{j}]"; t = require_object(raw_t, tp); reject_unknown(t, ALLOWED_THRESHOLD, tp)
            if set(t) != ALLOWED_THRESHOLD: raise ContractError(f"{tp} requires min and points")
            minimum = require_decimal(t["min"], f"{tp}.min"); points = require_decimal(t["points"], f"{tp}.points")
            if minimum in minima: raise ContractError(f"modifier {name} has duplicate threshold minimum {minimum}")
            minima.add(minimum); thresholds.append({"min": minimum, "points": points})
        if not thresholds: raise ContractError(f"modifier {name} requires thresholds")
        modifiers.append({"name": name, "selectors": selectors, "thresholds": thresholds, "target": target})
    return {"max_substitutions": max_subs, "slot_eligibility": eligibility, "modifiers": modifiers}


def choose_threshold(avg: Decimal, thresholds: list[dict[str, Decimal]]) -> Decimal:
    for t in sorted(thresholds, key=lambda x: x["min"], reverse=True):
        if avg >= t["min"]: return t["points"]
    return Decimal(0)


def score(data: object) -> dict[str, Any]:
    top = require_object(data, "$"); reject_unknown(top, ALLOWED_TOP, "$")
    if "starters" not in top or "rules" not in top: raise ContractError("$ requires starters and rules")
    starters = [parse_player(x, f"$.starters[{i}]", True) for i, x in enumerate(require_array(top["starters"], "$.starters"))]
    bench = [parse_player(x, f"$.bench[{i}]", False) for i, x in enumerate(require_array(top.get("bench", []), "$.bench"))]
    rules = parse_rules(top["rules"])
    seen = set()
    for row in starters + bench:
        if row["player_id"] in seen: raise ContractError(f"player_id appears more than once in scenario: {row['player_id']}")
        seen.add(row["player_id"])
    slots = set()
    for row in starters:
        slot = row["slot"]
        if slot in slots: raise ContractError(f"starter slot appears more than once: {slot}")
        slots.add(slot)
        if slot not in rules["slot_eligibility"]: raise ContractError(f"starter references unknown slot: {slot}")
        if not set(row["roles"]) & rules["slot_eligibility"][slot]: raise ContractError(f"starter {row['player_id']} is not eligible for slot {slot}")
    effective = [dict(x) for x in starters]; used_bench, substitutions = set(), []
    for i, starter in enumerate(effective):
        if starter["valid_vote"]: continue
        if len(substitutions) >= rules["max_substitutions"]: break
        allowed = rules["slot_eligibility"][starter["slot"]]
        pick = next((r for r in bench if r["player_id"] not in used_bench and r["valid_vote"] and set(r["roles"]) & allowed), None)
        if pick:
            used_bench.add(pick["player_id"]); rep = dict(pick); rep["slot"] = starter["slot"]; effective[i] = rep
            substitutions.append({"out": starter["player_id"], "in": pick["player_id"], "slot": starter["slot"]})
    player_total = sum((r["fantasy_points"] for r in effective if r["valid_vote"]), Decimal(0)); self_mod = Decimal(0); opp = Decimal(0); details = []
    for mod in rules["modifiers"]:
        selected = []
        for sel in mod["selectors"]:
            candidates = [r for r in effective if r["slot"] in set(sel["slots"]) and r["valid_vote"]]
            if len(candidates) < sel["take_best"]: raise ContractError(f"modifier {mod['name']} lacks enough valid players")
            if any(r["base_vote"] is None for r in candidates): raise ContractError(f"modifier {mod['name']} requires base_vote")
            candidates.sort(key=lambda r: r["base_vote"], reverse=True); selected.extend(candidates[:sel["take_best"]])
        if len({r["player_id"] for r in selected}) != len(selected): raise ContractError(f"modifier {mod['name']} selects the same player more than once")
        avg = sum((r["base_vote"] for r in selected), Decimal(0)) / Decimal(len(selected)); pts = choose_threshold(avg, mod["thresholds"])
        if mod["target"] == "self": self_mod += pts
        else: opp += pts
        details.append({"name": mod["name"], "target": mod["target"], "average": decimal_number(avg), "points": decimal_number(pts), "selected_player_ids": [r["player_id"] for r in selected]})
    def public(r): return {"player_id": r["player_id"], "roles": r["roles"], "valid_vote": r["valid_vote"], "slot": r.get("slot"), "fantasy_points": decimal_number(r["fantasy_points"]) if r["fantasy_points"] is not None else None, "base_vote": decimal_number(r["base_vote"]) if r["base_vote"] is not None else None}
    return {"ok": True, "contract": "score_scenario.v2", "effective_lineup": [public(r) for r in effective], "substitutions": substitutions, "player_total": decimal_number(player_total), "self_modifier_total": decimal_number(self_mod), "opponent_adjustment": decimal_number(opp), "total": decimal_number(player_total + self_mod), "modifier_details": details}


def main() -> None:
    try: out = score(json.load(sys.stdin))
    except (json.JSONDecodeError, ContractError, KeyError, TypeError) as exc: emit({"ok": False, "message": str(exc)}, 1)
    emit(out, 0)


if __name__ == "__main__": main()
