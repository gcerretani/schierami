#!/usr/bin/env python3
"""Validate one lineup against a deliberately explicit supported rule contract."""
from __future__ import annotations

import json
import sys

from _core import (
    ContractError, normalize_id, reject_unknown, require_array, require_bool,
    require_int, require_object, require_string, require_string_list,
)

ALLOWED_TOP = {"roster", "lineup", "rules"}
ALLOWED_PLAYER = {"id", "name", "roles"}
ALLOWED_LINEUP = {"formation", "starters", "bench", "captain_id"}
ALLOWED_STARTER = {"player_id", "slot"}
ALLOWED_RULES = {"starter_count", "bench_max", "formations", "slot_eligibility", "captain_required", "locked_starters", "excluded_players"}


def emit(obj: dict, code: int) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def contract(data: object):
    top = require_object(data, "$")
    reject_unknown(top, ALLOWED_TOP, "$")
    if set(top) != ALLOWED_TOP:
        raise ContractError("missing top-level keys: " + ", ".join(sorted(ALLOWED_TOP - set(top))))
    roster_raw = require_array(top["roster"], "$.roster")
    lineup = require_object(top["lineup"], "$.lineup")
    rules = require_object(top["rules"], "$.rules")
    reject_unknown(lineup, ALLOWED_LINEUP, "$.lineup")
    reject_unknown(rules, ALLOWED_RULES, "$.rules")

    by_id = {}
    for i, raw in enumerate(roster_raw):
        row = require_object(raw, f"$.roster[{i}]")
        reject_unknown(row, ALLOWED_PLAYER, f"$.roster[{i}]")
        if "id" not in row or "roles" not in row:
            raise ContractError(f"$.roster[{i}] requires id and roles")
        pid = normalize_id(row["id"], f"$.roster[{i}].id")
        if pid in by_id:
            raise ContractError(f"duplicate roster id: {pid}")
        by_id[pid] = set(require_string_list(row["roles"], f"$.roster[{i}].roles", nonempty=True))
        if row.get("name") is not None:
            require_string(row["name"], f"$.roster[{i}].name")

    if "formation" not in lineup or "starters" not in lineup:
        raise ContractError("$.lineup requires formation and starters")
    formation = require_string(lineup["formation"], "$.lineup.formation")
    starters = require_array(lineup["starters"], "$.lineup.starters")
    bench = require_array(lineup.get("bench", []), "$.lineup.bench")

    missing = sorted({"starter_count", "formations", "slot_eligibility"} - set(rules))
    if missing:
        raise ContractError("missing rule keys: " + ", ".join(missing))
    starter_count = require_int(rules["starter_count"], "$.rules.starter_count", 0)
    bench_max = None if "bench_max" not in rules else require_int(rules["bench_max"], "$.rules.bench_max", 0)
    captain_required = require_bool(rules.get("captain_required", False), "$.rules.captain_required")

    formations = {}
    for key, value in require_object(rules["formations"], "$.rules.formations").items():
        name = require_string(key, "$.rules.formations key")
        slots = require_string_list(value, f"$.rules.formations.{name}")
        if len(slots) != starter_count:
            raise ContractError(f"formation {name} has {len(slots)} slots but starter_count is {starter_count}")
        formations[name] = slots
    if not formations:
        raise ContractError("$.rules.formations must not be empty")

    eligibility = {}
    for key, value in require_object(rules["slot_eligibility"], "$.rules.slot_eligibility").items():
        slot = require_string(key, "$.rules.slot_eligibility key")
        eligibility[slot] = set(require_string_list(value, f"$.rules.slot_eligibility.{slot}", nonempty=True))
    for name, slots in formations.items():
        unknown = [slot for slot in slots if slot not in eligibility]
        if unknown:
            raise ContractError(f"formation {name} references slots without eligibility: {', '.join(unknown)}")

    restrictions = {}
    for key in ("locked_starters", "excluded_players"):
        values = [normalize_id(x, f"$.rules.{key}[]") for x in require_array(rules.get(key, []), f"$.rules.{key}")]
        if len(values) != len(set(values)) or set(values) - set(by_id):
            raise ContractError(f"{key} contains duplicate or unknown players")
        restrictions[key] = set(values)
    if restrictions["locked_starters"] & restrictions["excluded_players"]:
        raise ContractError("players cannot be both locked and excluded")

    return by_id, {"formation": formation, "starters": starters, "bench": bench, "captain_id": lineup.get("captain_id")}, {"starter_count": starter_count, "bench_max": bench_max, "captain_required": captain_required, "formations": formations, "slot_eligibility": eligibility, **restrictions}


def validate(data: object) -> dict:
    by_id, lineup, rules = contract(data)
    errors = []
    formation = lineup["formation"]
    required_slots = rules["formations"].get(formation)
    if required_slots is None:
        errors.append(f"formation not allowed: {formation}")
        required_slots = []
    starters = lineup["starters"]
    if len(starters) != rules["starter_count"]:
        errors.append(f"starter count {len(starters)} != {rules['starter_count']}")

    seen_players, seen_slots = set(), set()
    for i, raw in enumerate(starters):
        try:
            row = require_object(raw, f"$.lineup.starters[{i}]")
            reject_unknown(row, ALLOWED_STARTER, f"$.lineup.starters[{i}]")
            if set(row) != ALLOWED_STARTER:
                raise ContractError(f"$.lineup.starters[{i}] requires player_id and slot")
            pid = normalize_id(row["player_id"], f"$.lineup.starters[{i}].player_id")
            slot = require_string(row["slot"], f"$.lineup.starters[{i}].slot")
        except ContractError as exc:
            errors.append(str(exc)); continue
        if pid not in by_id: errors.append(f"starter not in roster: {pid}")
        if pid in seen_players: errors.append(f"player used more than once: {pid}")
        seen_players.add(pid)
        if slot in seen_slots: errors.append(f"slot used more than once: {slot}")
        seen_slots.add(slot)
        if slot not in required_slots:
            errors.append(f"slot not part of formation {formation}: {slot}")
        elif pid in by_id and not (by_id[pid] & rules["slot_eligibility"][slot]):
            errors.append(f"player {pid} roles {sorted(by_id[pid])} not eligible for slot {slot}")

    required_slot_set = set(required_slots)
    if required_slot_set != seen_slots:
        missing, extra = required_slot_set - seen_slots, seen_slots - required_slot_set
        if missing: errors.append("missing slots: " + ", ".join(sorted(missing)))
        if extra: errors.append("extra slots: " + ", ".join(sorted(extra)))

    if rules["locked_starters"] - seen_players:
        errors.append("missing locked starters: " + ", ".join(sorted(rules["locked_starters"] - seen_players)))

    bench_ids = []
    for i, raw in enumerate(lineup["bench"]):
        try: pid = normalize_id(raw, f"$.lineup.bench[{i}]")
        except ContractError as exc: errors.append(str(exc)); continue
        bench_ids.append(pid)
        if pid not in by_id: errors.append(f"bench player not in roster: {pid}")
        if pid in seen_players: errors.append(f"player used more than once: {pid}")
        seen_players.add(pid)
    if rules["bench_max"] is not None and len(bench_ids) > rules["bench_max"]:
        errors.append(f"bench size {len(bench_ids)} > {rules['bench_max']}")

    if rules["excluded_players"] & seen_players:
        errors.append("excluded players selected: " + ", ".join(sorted(rules["excluded_players"] & seen_players)))

    captain = lineup["captain_id"]
    if rules["captain_required"] and captain is None: errors.append("captain required")
    if captain is not None:
        try:
            captain_id = normalize_id(captain, "$.lineup.captain_id")
            starter_ids = {normalize_id(r.get("player_id"), "starter.player_id") for r in starters if isinstance(r, dict) and "player_id" in r}
            if captain_id not in starter_ids: errors.append("captain must be a starter")
        except ContractError as exc: errors.append(str(exc))

    if errors:
        return {"ok": False, "message": "lineup invalid", "errors": errors, "exit_code": 2}
    return {"ok": True, "contract": "validate_lineup.v2", "formation": formation, "starters": len(starters), "bench": len(bench_ids), "exit_code": 0}


def main() -> None:
    try:
        out = validate(json.load(sys.stdin))
    except (json.JSONDecodeError, ContractError, KeyError, TypeError) as exc:
        emit({"ok": False, "message": str(exc)}, 1)
    code = out.pop("exit_code")
    emit(out, code)


if __name__ == "__main__":
    main()
