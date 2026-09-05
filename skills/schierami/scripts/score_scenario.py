#!/usr/bin/env python3
import json, sys

ALLOWED_RULES = {"max_substitutions", "substitution_mode", "slot_eligibility", "modifiers"}

def die(msg):
    print(json.dumps({"ok": False, "message": msg}, ensure_ascii=False, indent=2))
    raise SystemExit(1)

def choose_threshold(avg, thresholds):
    for t in sorted(thresholds, key=lambda x: float(x["min"]), reverse=True):
        if avg >= float(t["min"]):
            return float(t["points"])
    return 0.0

def main():
    try:
        d = json.load(sys.stdin)
        starters = d["starters"]
        bench = d.get("bench", [])
        rules = d["rules"]
    except Exception as e:
        die(f"missing or malformed contract field: {e}")
    unknown = set(rules) - ALLOWED_RULES
    if unknown:
        die("unsupported rule keys: " + ", ".join(sorted(unknown)))
    if rules.get("substitution_mode") != "ordered_slots":
        die("only substitution_mode=ordered_slots is supported")

    eligibility = {str(k): set(map(str,v)) for k,v in rules.get("slot_eligibility", {}).items()}
    effective = [dict(x) for x in starters]
    used_bench, subs = set(), []
    max_subs = int(rules.get("max_substitutions", 0))

    for i, s in enumerate(effective):
        if bool(s.get("valid_vote")):
            continue
        if len(subs) >= max_subs:
            break
        slot = str(s.get("slot"))
        allowed = eligibility.get(slot, set())
        pick = None
        for j, b in enumerate(bench):
            if j in used_bench or not bool(b.get("valid_vote")):
                continue
            roles = set(map(str, b.get("roles", [])))
            if roles & allowed:
                pick = (j, b)
                break
        if pick:
            j, b = pick
            used_bench.add(j)
            rep = dict(b)
            rep["slot"] = slot
            effective[i] = rep
            subs.append({"out": s.get("player_id"), "in": b.get("player_id"), "slot": slot})

    player_total = sum(float(x.get("fantasy_points", 0)) for x in effective if bool(x.get("valid_vote")))
    self_mod = 0.0
    opp_adj = 0.0

    for mod in rules.get("modifiers", []):
        if mod.get("type") != "threshold_average":
            die(f"unsupported modifier type: {mod.get('type')}")
        selected = []
        for sel in mod.get("selectors", []):
            slots = set(map(str, sel.get("slots", [])))
            take_best = int(sel.get("take_best", 0))
            candidates = [x for x in effective if str(x.get("slot")) in slots and bool(x.get("valid_vote"))]
            if len(candidates) < take_best:
                die(f"modifier {mod.get('name','unnamed')} lacks enough valid players")
            if any(x.get("base_vote") is None for x in candidates):
                die(f"modifier {mod.get('name','unnamed')} requires base_vote")
            candidates.sort(key=lambda x: float(x["base_vote"]), reverse=True)
            selected.extend(candidates[:take_best])
        if not selected:
            die(f"modifier {mod.get('name','unnamed')} selects no players")
        avg = sum(float(x["base_vote"]) for x in selected) / len(selected)
        pts = choose_threshold(avg, mod.get("thresholds", []))
        target = mod.get("target", "self")
        if target == "self":
            self_mod += pts
        elif target == "opponent":
            opp_adj += pts
        else:
            die(f"unsupported modifier target: {target}")

    out = {"ok": True, "effective_lineup": effective, "substitutions": subs, "player_total": player_total, "self_modifier_total": self_mod, "opponent_adjustment": opp_adj, "total": player_total + self_mod}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
