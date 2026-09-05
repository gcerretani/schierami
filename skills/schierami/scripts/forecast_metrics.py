"""Proper-score diagnostics for finite forecast distributions; lower loss is better."""
from __future__ import annotations

import math

from _core import ContractError
from forecast_core import marginals, outcome


def crps(values: list[tuple[float, float]], observed: float) -> float:
    """E|X-y| - E|X-X'|/2 using a sorted O(n log n) weighted scan."""
    first = math.fsum(p * abs(x - observed) for p, x in values)
    mass, moment, half_pairwise = 0.0, 0.0, 0.0
    for p, x in sorted(values, key=lambda a: a[1]):
        half_pairwise += p * (x * mass - moment)
        mass += p
        moment += p * x
    return max(0.0, first - half_pairwise)


def observations(bundle: dict, actual: list[dict]) -> list[dict]:
    distributions = marginals(bundle)
    records, seen = [], set()
    for raw in actual:
        row = outcome(raw)
        pid = row["player_id"]
        if pid in seen or pid not in distributions:
            raise ContractError("unknown or duplicate observed player")
        seen.add(pid)
        distribution = distributions[pid]
        record = {"player_id": pid}
        for target, field in (("start", "started"), ("vote", "valid_vote"), ("appearance", "minutes")):
            p = math.fsum(w * (x[field] > 0 if target == "appearance" else x[field]) for w, x in distribution)
            p = min(1.0, max(0.0, p))  # Only roundoff: positive normalized weights were validated.
            y = int(row[field] > 0 if target == "appearance" else row[field])
            likelihood = p if y else 1 - p
            record[target] = {"probability": p, "actual": y, "brier": (p - y)**2,
                              "log_loss": -math.log(likelihood) if likelihood > 0 else None,
                              "clipped_log_loss": -math.log(max(likelihood, 1e-15))}
        for field in ("minutes", "fantasy_points"):
            values = [(p, x[field]) for p, x in distribution]
            mean = math.fsum(p * x for p, x in values)
            record[field] = {"mean": mean, "actual": row[field], "error": mean - row[field],
                             "crps": crps(values, row[field])}
        base = [(p, r["base_vote"]) for p, r in distribution if r["base_vote"] is not None]
        mass = math.fsum(p for p, _ in base)
        record["base_vote_target_available"] = row["base_vote"] is not None
        record["base_vote"] = None
        if row["base_vote"] is not None and mass:
            values = [(p / mass, v) for p, v in base]
            mean = math.fsum(p * v for p, v in values)
            record["base_vote"] = {"mean": mean, "actual": row["base_vote"],
                                   "error": mean - row["base_vote"], "crps": crps(values, row["base_vote"])}
        records.append(record)
    return records


def aggregate(records: list[dict]) -> dict:
    if not records:
        raise ContractError("no forecast observations to evaluate")
    n = len(records)
    mean = lambda values: math.fsum(values) / n
    result = {"n": n}
    for target in ("start", "vote", "appearance"):
        rows = [r[target] for r in records]
        impossible = sum(r["log_loss"] is None for r in rows)
        bins = []
        for i in range(10):
            group = [r for r in rows if min(9, int(r["probability"] * 10)) == i]
            bins.append({"lower": i / 10, "upper": (i + 1) / 10, "n": len(group),
                         "mean_probability": math.fsum(r["probability"] for r in group) / len(group) if group else None,
                         "observed_frequency": math.fsum(r["actual"] for r in group) / len(group) if group else None})
        result[target] = {"brier": mean(r["brier"] for r in rows),
                          "log_loss": None if impossible else mean(r["log_loss"] for r in rows),
                          "infinite_log_losses": impossible,
                          "clipped_log_loss_epsilon_1e_15": mean(r["clipped_log_loss"] for r in rows),
                          "reliability_bins": bins}
    for field in ("minutes", "fantasy_points"):
        rows = [r[field] for r in records]
        result[field] = {"mae": mean(abs(r["error"]) for r in rows),
                         "rmse": math.sqrt(mean(r["error"]**2 for r in rows)),
                         "crps": mean(r["crps"] for r in rows)}
    targets = sum(r["base_vote_target_available"] for r in records)
    base = [r["base_vote"] for r in records if r["base_vote"] is not None]
    result["base_vote_conditional"] = {"n_targets": targets, "n_scored": len(base),
        "missing_forecast_count": targets - len(base),
        "mae": math.fsum(abs(r["error"]) for r in base) / len(base) if base else None,
        "rmse": math.sqrt(math.fsum(r["error"]**2 for r in base) / len(base)) if base else None,
        "crps": math.fsum(r["crps"] for r in base) / len(base) if base else None}
    return result
