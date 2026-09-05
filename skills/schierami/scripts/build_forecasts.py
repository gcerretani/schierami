#!/usr/bin/env python3
"""Empirical player/role shrinkage baseline; no invented news-derived probabilities."""
from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from typing import Any

from _core import ContractError, require_int
from forecast_core import (ENGINE_VERSION, OUTCOME, array, cli, digest, evidence,
                           number, obj, outcome, roster, scope, summaries, text, time, usable,
                           validate_bundle)

INPUT = {"scope", "as_of", "deadline", "roster", "evidence", "history", "model"}
HISTORY = OUTCOME | {"match_id", "kickoff", "available_at", "source_id"}
MODEL = {"name", "window", "prior_strength", "lookback_days"}


def parse_history(value: Any, players: dict, ledger: dict) -> list[dict]:
    result, seen = [], set()
    for row in array(value, "history"):
        obj(row, HISTORY, "history[]")
        outcome({k: row[k] for k in OUTCOME})
        key = (row["player_id"], text(row["match_id"], "match_id"))
        if key in seen or key[0] not in players:
            raise ContractError("duplicate player-match observation or unknown player")
        seen.add(key)
        source = text(row["source_id"], "source_id")
        if source not in ledger:
            raise ContractError("unknown history source")
        if time(row["available_at"], "available_at") < time(row["kickoff"], "kickoff"):
            raise ContractError("outcome available_at predates kickoff")
        if time(ledger[source]["retrieved_at"], "retrieved_at") < time(row["available_at"], "available_at"):
            raise ContractError("history source captured before its outcome was available")
        result.append(dict(row))
    return result


def build(data: Any) -> dict:
    d = obj(data, INPUT, "forecast request")
    context = scope(d["scope"])
    cutoff = time(d["as_of"], "as_of")
    if cutoff > time(d["deadline"], "deadline"):
        raise ContractError("forecast cutoff is after deadline")
    players, ledger = roster(d["roster"]), evidence(d["evidence"])
    model = obj(d["model"], MODEL, "model")
    text(model["name"], "model.name")
    window = require_int(model["window"], "window", 1)
    days = require_int(model["lookback_days"], "lookback_days", 1)
    if window > 10000 or days > 36500:
        raise ContractError("baseline window/lookback exceeds supported limit")
    strength = number(model["prior_strength"], "prior_strength", 0, 10000)
    history = parse_history(d["history"], players, ledger)
    by_player = defaultdict(list)
    used_ids = set()
    excluded_future, excluded_old = 0, 0
    for row in history:
        if (time(row["available_at"], "available_at") > cutoff or
                time(ledger[row["source_id"]]["retrieved_at"], "retrieved_at") > cutoff):
            excluded_future += 1
            continue
        if time(row["kickoff"], "kickoff") < cutoff - timedelta(days=days):
            excluded_old += 1
            continue
        # Unresolved/expired evidence fails closed instead of silently selecting a cleaner sample.
        usable([row["source_id"]], ledger, cutoff)
        by_player[row["player_id"]].append(row)
    for pid in by_player:
        by_player[pid] = sorted(by_player[pid], key=lambda r: (time(r["kickoff"], "kickoff"), r["match_id"]))[-window:]
    blocks, diagnostics = [], []
    for pid in sorted(players):
        own = by_player[pid]
        peers = [r for other in sorted(players) if other != pid and
                 set(players[other]["roles"]) == set(players[pid]["roles"]) for r in by_player[other]]
        if not own and not peers:
            raise ContractError(f"no historical support for {pid} or its exact role group; supply data or use conditional advice")
        weighted = [(1.0, r) for r in own]
        # Empirical-Bayes-style shrinkage with explicit, not fitted, prior strength.
        if peers and (strength > 0 or not own):
            weighted += [((strength if own else 1.0) / len(peers), r) for r in peers]
        states, refs = [], set()
        for weight, row in weighted:
            refs.add(row["source_id"])
            used_ids.add((row["player_id"], row["match_id"]))
            state = {k: row[k] for k in OUTCOME}
            state["player_id"] = pid
            states.append({"weight": weight, "outcomes": [state]})
        blocks.append({"id": pid, "player_ids": [pid], "evidence_ids": sorted(refs), "states": states})
        diagnostics.append({"player_id": pid, "player_matches": len(own), "peer_matches": len(peers),
                            "cold_start": not bool(own), "shrinkage_applied": bool(peers and strength > 0),
                            "prior_unavailable": strength > 0 and not peers})
    refs = {eid for b in blocks for eid in b["evidence_ids"]}
    bundle = {"contract": "forecast_bundle.v1", "scope": context, "as_of": d["as_of"],
              "deadline": d["deadline"], "roster": [players[p] for p in sorted(players)],
              "evidence": [ledger[k] for k in sorted(refs)], "input_sha256": digest(d),
              "model": {"name": model["name"], "version": ENGINE_VERSION,
                        "status": "baseline_unvalidated", "assumptions": [
                            "Empirical recent outcomes with explicit exact-role peer shrinkage; no trained calibration.",
                            "Minutes, vote and points remain coupled within each player outcome.",
                            "Player blocks are independent: no inter-player or match-event coherence is claimed.",
                            "No opponent adjustment, injury/news update, goal model or editorial-vote transfer is inferred."]},
              "independent_blocks": True, "blocks": blocks}
    validate_bundle(bundle)
    return {"ok": True, "contract": "build_forecasts.v1", "engine_version": ENGINE_VERSION,
            "forecast_bundle": bundle, "player_forecasts": summaries(bundle),
            "projections": [{"player_id": r["player_id"], "expected_points": r["expected_points"]}
                            for r in summaries(bundle)],
            "training_audit": {"parameters": dict(model), "excluded_future_rows": excluded_future,
                "excluded_old_rows": excluded_old, "used_player_matches": [list(x) for x in sorted(used_ids)],
                "evidence_origins": sorted({ledger[r]["origin_id"] for r in refs}),
                "players": diagnostics, "availability_check": "declared_capture_times_only"}}


if __name__ == "__main__":
    cli(build)
