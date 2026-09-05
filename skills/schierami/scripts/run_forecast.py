#!/usr/bin/env python3
"""Evaluate legal candidates using an explicit forecast bundle and shared scenarios."""
from __future__ import annotations

import itertools
import math
import random
from typing import Any

from _core import ContractError, require_int
from evaluate_lineups import evaluate
from score_scenario import parse_rules
from forecast_core import ENGINE_VERSION, array, cli, digest, obj, validate_bundle


def scenarios(bundle: Any, sampling: Any) -> tuple[list[dict], dict]:
    b = validate_bundle(bundle)
    config = obj(sampling, {"method"}, "sampling", {"max_scenarios", "samples", "seed"})
    blocks = sorted(b["blocks"], key=lambda x: x["id"])
    states = [block["states"] for block in blocks]
    size = math.prod(len(s) for s in states)
    method = config["method"]
    if method == "exact":
        obj(config, {"method", "max_scenarios"}, "sampling")
        limit = require_int(config["max_scenarios"], "max_scenarios", 1)
        if limit > 10000 or size > limit:
            raise ContractError(f"exact state space {size} exceeds budget; choose explicit Monte Carlo or smaller supported model")
        combinations = [(indices, math.prod(states[j][i]["weight"] / math.fsum(x["weight"] for x in states[j])
                          for j, i in enumerate(indices)))
                        for indices in itertools.product(*(range(len(s)) for s in states))]
        n = None
        seed = None
    elif method == "monte_carlo":
        obj(config, {"method", "samples", "seed"}, "sampling")
        n = require_int(config["samples"], "samples", 2)
        seed = require_int(config["seed"], "seed", 0)
        if n > 10000:
            raise ContractError("maximum 10000 Monte Carlo draws per run")
        rng = random.Random(seed)
        counts = {}
        # Draw one whole state per block, never independently sample players inside it.
        for _ in range(n):
            indices = tuple(rng.choices(range(len(s)), weights=[x["weight"] for x in s], k=1)[0] for s in states)
            counts[indices] = counts.get(indices, 0) + 1
        combinations = sorted(counts.items())
    else:
        raise ContractError("sampling.method must be exact or monte_carlo")
    result = []
    for k, (indices, weight) in enumerate(combinations):
        if weight <= 0 or not math.isfinite(weight):
            raise ContractError("scenario probability underflow/overflow; rescale or reduce the model")
        rows = [r for j, i in enumerate(indices) for r in states[j][i]["outcomes"]]
        result.append({"id": str(k), "weight": weight, "outcomes": [
            {key: row[key] for key in ("player_id", "valid_vote", "base_vote", "fantasy_points")}
            for row in sorted(rows, key=lambda r: r["player_id"])]})
    return result, {"method": method, "state_space": size, "scenarios_scored": len(result),
                    "draws": n, "seed": seed, "shared_scenarios_across_candidates": True,
                    "joint_blocks_preserved": True, "independence_between_blocks": b["independent_blocks"]}


def run(data: Any) -> dict:
    d = obj(data, {"forecast_bundle", "sampling", "candidates", "rules", "lineup_rules"}, "forecast decision")
    bundle = validate_bundle(d["forecast_bundle"])
    generated, sampling = scenarios(bundle, d["sampling"])
    if len(array(d["candidates"], "candidates")) * len(generated) > 100000:
        raise ContractError("candidate-scenario evaluations exceed 100000; reduce explicit budget")
    # Reject opponent effects: maximizing own score alone would ignore a material rule.
    for modifier in parse_rules(d["rules"])["modifiers"]:
        if modifier.get("target", "self") != "self":
            raise ContractError("forecast decision does not support opponent-target modifiers")
    result = evaluate({"roster": bundle["roster"], "candidates": d["candidates"], "scenarios": generated,
                       "rules": d["rules"], "lineup_rules": d["lineup_rules"]})
    comparisons = []
    best = result["rankings"][0]
    for other in result["rankings"][1:]:
        rows = [(a["probability"], a["total"] - b["total"]) for a, b in
                zip(best["scenario_results"], other["scenario_results"])]
        mean = math.fsum(p * v for p, v in rows)
        variance = max(0.0, math.fsum(p * (v - mean)**2 for p, v in rows))
        n = sampling["draws"]
        comparisons.append({"versus": other["candidate_id"], "expected_score_difference": mean,
                            "minimum_scenario_difference": min(v for _, v in rows),
                            "maximum_scenario_difference": max(v for _, v in rows),
                            "paired_mc_standard_error": math.sqrt(variance / (n - 1)) if n else None})
    if sampling["method"] == "monte_carlo":
        result["optimality"] = "best_among_supplied_candidates_on_sample_only"
    result.update({"contract": "forecast_decision.v1", "engine_version": ENGINE_VERSION,
                   "sampling": sampling, "comparisons_to_selected": comparisons,
                   "forecast_status": bundle["model"]["status"], "forecast_as_of": bundle["as_of"],
                   "forecast_sha256": digest(bundle), "input_sha256": digest(d),
                   "scientific_limits": [
                       "Candidate set, supplied distribution and supported rules only; not a global fantasy optimum.",
                       "Monte Carlo standard error measures sampling noise, not forecast/model uncertainty.",
                       "Selected-best comparisons are exploratory, not post-selection confidence tests.",
                       "No empirical accuracy, calibration or real-world winning probability is certified."]})
    return result


if __name__ == "__main__":
    cli(run)
