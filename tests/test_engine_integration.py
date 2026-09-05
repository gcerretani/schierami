"""Regression and exhaustive-oracle tests; all players and rules are synthetic."""
import copy
from decimal import Decimal
import itertools
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/schierami/scripts"))
from _core import ContractError
from evaluate_lineups import evaluate
from optimize_lineup import optimize
from validate_lineup import validate


def ensemble():
    slots = ["S1", "S2"]
    return {
        "roster": [{"id": p, "roles": ["D"]} for p in "abc"],
        "candidates": [{"id": "legal", "formation": "f", "starters": [
            {"player_id": "a", "slot": "S1"}, {"player_id": "b", "slot": "S2"}
        ], "bench": ["c"]}],
        "lineup_rules": {"starter_count": 2, "bench_max": 1,
            "formations": {"f": slots}, "slot_eligibility": {s: ["D"] for s in slots},
            "captain_required": False},
        "rules": {"max_substitutions": 1, "substitution_mode": "ordered_slots",
            "slot_eligibility": {s: ["D"] for s in slots}, "modifiers": []},
        "scenarios": [{"id": "six", "weight": 1, "outcomes": [
            {"player_id": p, "valid_vote": True, "fantasy_points": 6} for p in "abc"]}],
    }


class EngineIntegrationTests(unittest.TestCase):
    def test_evaluator_validates_then_scores(self):
        result = evaluate(ensemble())
        self.assertTrue(result["legality_validated"])
        self.assertEqual(result["rankings"][0]["expected_total"], 12)

    def test_extra_starter_cannot_win(self):
        x = ensemble()
        x["candidates"][0]["bench"] = []
        x["candidates"][0]["starters"].append({"player_id": "c", "slot": "S3"})
        # A scoring map knowing S3 is not permission to submit an extra starter.
        x["rules"]["slot_eligibility"]["S3"] = ["D"]
        x["lineup_rules"]["slot_eligibility"]["S3"] = ["D"]
        with self.assertRaisesRegex(ContractError, "starter count"):
            evaluate(x)

    def test_illegal_formation_and_bench_limit(self):
        for field, value in [("formation", "invented"), ("bench", ["c", "c"])]:
            x = ensemble()
            x["candidates"][0][field] = value
            with self.assertRaises(ContractError):
                evaluate(x)
        x = ensemble()
        x["lineup_rules"]["bench_max"] = 0
        with self.assertRaisesRegex(ContractError, "bench size"):
            evaluate(x)

    def test_legality_and_scoring_cannot_disagree(self):
        x = ensemble()
        x["rules"]["slot_eligibility"]["S1"] = ["A"]
        with self.assertRaisesRegex(ContractError, "must agree"):
            evaluate(x)

    def test_missing_legality_does_not_default(self):
        for key in ("bench_max", "captain_required", "starter_count"):
            x = ensemble()
            del x["lineup_rules"][key]
            with self.assertRaises(ContractError):
                evaluate(x)

    def test_captain_scoring_fails_closed(self):
        x = ensemble()
        x["lineup_rules"]["captain_required"] = True
        x["candidates"][0]["captain_id"] = "a"
        with self.assertRaisesRegex(ContractError, "captain scoring"):
            evaluate(x)

    def test_locks_and_exclusions_share_validator(self):
        for key in ("locked_starters", "excluded_players"):
            x = ensemble()
            x["lineup_rules"][key] = ["c"]
            with self.assertRaises(ContractError):
                evaluate(x)

    def test_unused_outcomes_still_validated(self):
        x = ensemble()
        x["candidates"][0]["bench"] = []
        x["scenarios"][0]["outcomes"][2]["valid_vote"] = "false"
        with self.assertRaisesRegex(ContractError, "boolean"):
            evaluate(x)

    def test_captain_below_one(self):
        x = {"roster": [{"id": p, "roles": ["D"]} for p in "ab"],
             "projections": [{"player_id": "a", "expected_points": 10}, {"player_id": "b", "expected_points": 9}],
             "rules": {"starter_count": 2, "formations": {"f": ["S1", "S2"]},
                       "slot_eligibility": {"S1": ["D"], "S2": ["D"]},
                       "captain_required": True, "captain_multiplier": "0.5"}}
        result = optimize(x)
        self.assertEqual(result["captain_id"], "b")
        self.assertEqual(result["objective_value"], 14.5)

    def test_optimizer_matches_exhaustive_oracle(self):
        rng = random.Random(913)
        for case in range(30):
            values = {p: Decimal(rng.randrange(-30, 101)) / 10 for p in "abcde"}
            for multiplier in (Decimal("0.1"), Decimal("0.5"), Decimal(1), Decimal(2)):
                with self.subTest(case=case, multiplier=multiplier):
                    rules = {"starter_count": 3, "formations": {"f": ["S1", "S2", "S3"]},
                             "slot_eligibility": {s: ["D"] for s in ("S1", "S2", "S3")},
                             "captain_required": True, "captain_multiplier": str(multiplier),
                             "locked_starters": ["a"], "excluded_players": ["e"]}
                    data = {"roster": [{"id": p, "roles": ["D"]} for p in values],
                            "projections": [{"player_id": p, "expected_points": str(v)} for p, v in values.items()],
                            "rules": rules}
                    oracle = max(sum((values[p] for p in team), Decimal(0)) +
                                 max((multiplier - 1) * values[p] for p in team)
                                 for team in itertools.combinations("abcd", 3) if "a" in team)
                    self.assertEqual(Decimal(str(optimize(data)["objective_value"])), oracle)


if __name__ == "__main__":
    unittest.main()
