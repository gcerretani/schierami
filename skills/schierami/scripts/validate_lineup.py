#!/usr/bin/env python3
import json, sys

ALLOWED_TOP = {"roster", "lineup", "rules"}

def fail(message, code=1, errors=None):
    out = {"ok": False, "message": message}
    if errors is not None:
        out["errors"] = errors
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(code)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        fail(f"invalid JSON: {e}")
    if set(data) - ALLOWED_TOP:
        fail("unsupported top-level keys: " + ", ".join(sorted(set(data)-ALLOWED_TOP)))
    try:
        roster = data["roster"]
        lineup = data["lineup"]
        rules = data["rules"]
        formations = rules["formations"]
        eligibility = rules["slot_eligibility"]
        starter_count = int(rules["starter_count"])
    except Exception as e:
        fail(f"missing or malformed contract field: {e}")

    by_id = {}
    for p in roster:
        pid = str(p["id"])
        if pid in by_id:
            fail(f"duplicate roster id: {pid}")
        by_id[pid] = set(map(str, p.get("roles", [])))

    errors = []
    formation = str(lineup.get("formation", ""))
    required_slots = formations.get(formation)
    if required_slots is None:
        errors.append(f"formation not allowed: {formation}")
        required_slots = []
    required_slots = list(map(str, required_slots))

    starters = lineup.get("starters", [])
    bench = [str(x) for x in lineup.get("bench", [])]
    if len(starters) != starter_count:
        errors.append(f"starter count {len(starters)} != {starter_count}")

    seen_players, seen_slots = set(), set()
    for row in starters:
        pid, slot = str(row.get("player_id")), str(row.get("slot"))
        if pid not in by_id:
            errors.append(f"starter not in roster: {pid}")
        if pid in seen_players:
            errors.append(f"player used more than once: {pid}")
        seen_players.add(pid)
        if slot in seen_slots:
            errors.append(f"slot used more than once: {slot}")
        seen_slots.add(slot)
        allowed = set(map(str, eligibility.get(slot, [])))
        if slot not in required_slots:
            errors.append(f"slot not part of formation {formation}: {slot}")
        elif pid in by_id and not (by_id[pid] & allowed):
            errors.append(f"player {pid} roles {sorted(by_id[pid])} not eligible for slot {slot}")

    if set(required_slots) != seen_slots:
        missing = set(required_slots) - seen_slots
        extra = seen_slots - set(required_slots)
        if missing:
            errors.append("missing slots: " + ", ".join(sorted(missing)))
        if extra:
            errors.append("extra slots: " + ", ".join(sorted(extra)))

    for pid in bench:
        if pid not in by_id:
            errors.append(f"bench player not in roster: {pid}")
        if pid in seen_players:
            errors.append(f"player used more than once: {pid}")
        seen_players.add(pid)
    bench_max = rules.get("bench_max")
    if bench_max is not None and len(bench) > int(bench_max):
        errors.append(f"bench size {len(bench)} > {bench_max}")

    captain = lineup.get("captain_id")
    if rules.get("captain_required") and captain is None:
        errors.append("captain required")
    if captain is not None and str(captain) not in {str(r.get("player_id")) for r in starters}:
        errors.append("captain must be a starter")

    if errors:
        fail("lineup invalid", 2, errors)
    print(json.dumps({"ok": True, "formation": formation, "starters": len(starters), "bench": len(bench)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
