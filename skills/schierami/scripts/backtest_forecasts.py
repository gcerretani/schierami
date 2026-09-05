#!/usr/bin/env python3
"""Predeclared walk-forward forecast comparison; optional decision replay, no fitting on test outcomes."""
from __future__ import annotations

import math
import random
from typing import Any

from _core import ContractError, require_int
from build_forecasts import MODEL, build, parse_history
from evaluate_lineups import evaluate
from forecast_core import (ENGINE_VERSION, OUTCOME, array, cli, digest, evidence, obj, roster,
                           scope, text, time)
from forecast_metrics import aggregate, observations
from run_forecast import run as decide


def backtest(data: Any) -> dict:
    d = obj(data, {"scope", "roster", "evidence", "history", "models", "folds", "bootstrap"}, "backtest")
    scope(d["scope"])
    players, ledger = roster(d["roster"]), evidence(d["evidence"])
    history = parse_history(d["history"], players, ledger)
    models, names = array(d["models"], "models"), set()
    for model in models:
        obj(model, MODEL, "model")
        name = text(model["name"], "model.name")
        if name in names:
            raise ContractError("duplicate model name")
        names.add(name)
    if len(models) < 2:
        raise ContractError("benchmark requires at least two predeclared models")
    bootstrap = obj(d["bootstrap"], {"seed", "resamples"}, "bootstrap")
    seed = require_int(bootstrap["seed"], "seed", 0)
    resamples = require_int(bootstrap["resamples"], "resamples", 0)
    if resamples > 10000:
        raise ContractError("bootstrap budget exceeds 10000")
    folds, fold_ids, tested, previous = [], set(), set(), None
    # Validate all fold boundaries before making any forecast.
    for fold in array(d["folds"], "folds"):
        obj(fold, {"id", "as_of", "test_match_ids"}, "fold", {"decision"})
        fid = text(fold["id"], "fold.id")
        cutoff = time(fold["as_of"], "fold.as_of")
        if fid in fold_ids or (previous is not None and cutoff <= previous):
            raise ContractError("folds must have unique IDs and strictly increasing cutoffs")
        fold_ids.add(fid)
        previous = cutoff
        matches = [text(x, "test_match_id") for x in array(fold["test_match_ids"], "test_match_ids")]
        if len(matches) != len(set(matches)):
            raise ContractError("duplicate test match id")
        targets = [r for r in history if r["match_id"] in matches]
        if {r["match_id"] for r in targets} != set(matches):
            raise ContractError("test match has no target outcomes")
        for row in targets:
            key = (row["player_id"], row["match_id"])
            if key in tested or time(row["kickoff"], "kickoff") <= cutoff:
                raise ContractError("test target repeated or kickoff is not after cutoff")
            if time(row["available_at"], "available_at") <= cutoff:
                raise ContractError("test outcome is already available at cutoff")
            if ledger[row["source_id"]]["status"] not in ("confirmed", "user_stated"):
                raise ContractError("unresolved test outcome evidence")
            tested.add(key)
        folds.append((fold, targets))
    all_records = {n: [] for n in names}
    fold_results = []
    for fold, targets in folds:
        per_model = []
        for model in models:
            forecast = build({k: d[k] for k in ("scope", "roster", "evidence", "history")} |
                             {"as_of": fold["as_of"], "deadline": fold["as_of"], "model": model})
            bundle = forecast["forecast_bundle"]
            # Each player-match is a scoring unit; never collapse double fixtures into one outcome.
            records = [observations(bundle, [{k: row[k] for k in OUTCOME}])[0] for row in targets]
            all_records[model["name"]].extend(records)
            entry = {"model": model["name"], "metrics": aggregate(records),
                     "forecast_sha256": digest(bundle), "training_audit": forecast["training_audit"]}
            if "decision" in fold:
                decision = obj(fold["decision"], {"candidates", "rules", "lineup_rules", "sampling"}, "decision")
                if len(targets) != len(players) or {r["player_id"] for r in targets} != set(players):
                    raise ContractError("decision replay needs exactly one observed outcome per roster player")
                prediction = decide({"forecast_bundle": bundle, **decision})
                # Realized results enter only after the candidate has been selected.
                realized = evaluate({"roster": d["roster"], **{k: decision[k] for k in ("candidates", "rules", "lineup_rules")},
                    "scenarios": [{"id": "observed", "weight": 1, "outcomes": [
                        {k: r[k] for k in ("player_id", "valid_vote", "fantasy_points", "base_vote")} for r in targets]}]})
                values = {r["candidate_id"]: r["expected_total"] for r in realized["rankings"]}
                selected = prediction["best_candidate_id"]
                entry["decision"] = {"selected_candidate_id": selected, "realized_total": values[selected],
                    "hindsight_regret_among_candidates": max(values.values()) - values[selected],
                    "selection_optimality": prediction["optimality"]}
            per_model.append(entry)
        fold_results.append({"id": fold["id"], "as_of": fold["as_of"], "models": per_model,
                             "test_player_matches": [[r["player_id"], r["match_id"]] for r in targets]})
    comparisons = []
    for j in range(1, len(models)):
        deltas = [f["models"][j]["metrics"]["fantasy_points"]["crps"] -
                  f["models"][0]["metrics"]["fantasy_points"]["crps"] for f in fold_results]
        interval = None
        if len(deltas) >= 2 and resamples:
            rng = random.Random(seed)
            draws = sorted(math.fsum(rng.choice(deltas) for _ in deltas) / len(deltas) for _ in range(resamples))
            interval = [draws[int(.025 * (len(draws) - 1))], draws[int(.975 * (len(draws) - 1))]]
        comparisons.append({"model": models[j]["name"], "reference": models[0]["name"],
                            "metric": "equal_fold_mean_fantasy_points_crps_difference",
                            "difference": math.fsum(deltas) / len(deltas), "negative_favors_model": True,
                            "paired_fold_bootstrap_percentile_95": interval})
    return {"ok": True, "contract": "backtest_forecasts.v1", "engine_version": ENGINE_VERSION,
            "input_sha256": digest(d), "evaluation_kind": "declared_timestamp_walk_forward_replay",
            "predictive_superiority_established": False,
            "models": [{"name": m["name"], "parameters": m, "metrics": aggregate(all_records[m["name"]])} for m in models],
            "folds": fold_results, "comparisons": comparisons, "bootstrap": bootstrap,
            "limitations": ["Availability is checked from supplied timestamps, not independently attested.",
                "No automatic tuning, calibration fit, model selection or promotion occurs on test folds.",
                "Bootstrap resamples whole folds; serial dependence across folds is not modeled.",
                "Intervals on few folds are unstable and comparisons are not multiplicity-adjusted.",
                "Hindsight regret is diagnostic, not evidence that the pre-deadline decision was irrational."]}


if __name__ == "__main__":
    cli(backtest)
