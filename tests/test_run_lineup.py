from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/schierami/scripts"))
from run_lineup import run


FULL_CHECKS = [
    {"name": "roster_read", "status": "done"},
    {"name": "matchday_mapping", "status": "done"},
    {"name": "formation_rules", "status": "done"},
    {"name": "substitution_rules", "status": "not_applicable"},
    {"name": "modifier_rules", "status": "not_applicable"},
    {"name": "captain_rules", "status": "not_applicable"},
    {"name": "data_quality", "status": "done"},
    {"name": "availability_evidence", "status": "done"},
    {"name": "candidate_screening", "status": "done"},
]


class RunLineupTests(unittest.TestCase):
    def test_unknown_payload_stays_conditional_for_legacy_callers(self):
        out = run({"payload": {"roster": []}, "checks": [{"name": "modifier", "status": "blocked"}], "blockers": [{"fact": "modifier formula unknown", "blocks": ["module ranking"]}]})
        self.assertTrue(out["ok"])
        self.assertEqual(out["run_report"]["decision_mode"], "qualitative_conditional")
        self.assertIsNone(out["run_report"]["execution"]["script_ran"])
        self.assertEqual(out["run_report"]["completion"]["status"], "not_enforced")

    def test_full_lineup_cannot_silently_fall_back_without_quantitative_blocker(self):
        checks = FULL_CHECKS + [{"name": "deterministic_calculation", "status": "blocked"}]
        out = run({"request": {"kind": "full_lineup"}, "payload": {"roster": []}, "checks": checks, "blockers": [{"fact": "modifier formula unknown", "blocks": ["module ranking"]}]})
        self.assertTrue(out["ok"])
        gate = out["run_report"]["completion"]
        self.assertEqual(gate["status"], "blocked")
        self.assertEqual(gate["claim_scope"], "incomplete")
        self.assertFalse(gate["quantitative_blocked"])
        self.assertTrue(any("explicit blocker" in item for item in gate["issues"]))

    def test_full_lineup_conditional_only_requires_explicit_quantitative_blocker(self):
        checks = FULL_CHECKS + [{"name": "deterministic_calculation", "status": "blocked"}]
        out = run({"request": {"kind": "full_lineup"}, "payload": {"roster": []}, "checks": checks, "blockers": [{"fact": "no defensible quantitative observations", "blocks": ["quantitative_comparison"], "flip_condition": "verified historical observations become available"}]})
        self.assertTrue(out["ok"])
        gate = out["run_report"]["completion"]
        self.assertEqual(gate["status"], "complete")
        self.assertEqual(gate["claim_scope"], "conditional_only")
        self.assertTrue(gate["quantitative_blocked"])

    def test_validation_dispatch_is_observable(self):
        payload = {
            "roster": [{"id": "a", "roles": ["D"]}],
            "lineup": {"formation": "f", "starters": [{"player_id": "a", "slot": "S"}], "bench": []},
            "rules": {"starter_count": 1, "bench_max": 0, "formations": {"f": ["S"]}, "slot_eligibility": {"S": ["D"]}, "captain_required": False},
        }
        out = run({"payload": payload, "checks": [{"name": "legality", "status": "done", "source": "synthetic test"}], "blockers": []})
        self.assertTrue(out["ok"])
        self.assertEqual(out["run_report"]["decision_mode"], "deterministic_validation_scoring")
        self.assertEqual(out["run_report"]["execution"]["script_ran"], "validate_lineup.py")

    def test_full_lineup_additive_execution_passes_completion_gate(self):
        payload = {
            "roster": [{"id": "a", "roles": ["D"]}],
            "projections": [{"player_id": "a", "expected_points": 6.0}],
            "rules": {"starter_count": 1, "formations": {"f": ["S"]}, "slot_eligibility": {"S": ["D"]}, "captain_required": False},
        }
        checks = FULL_CHECKS + [{"name": "deterministic_calculation", "status": "done"}]
        out = run({"request": {"kind": "full_lineup"}, "payload": payload, "checks": checks, "blockers": []})
        self.assertTrue(out["ok"])
        self.assertEqual(out["run_report"]["decision_mode"], "exact_additive_optimum")
        self.assertEqual(out["run_report"]["execution"]["script_ran"], "optimize_lineup.py")
        self.assertEqual(out["run_report"]["completion"]["status"], "complete")
        self.assertEqual(out["run_report"]["completion"]["claim_scope"], "full_rule_quantitative")

    def test_full_lineup_additive_execution_with_material_blocker_is_partial(self):
        payload = {
            "roster": [{"id": "a", "roles": ["D"]}],
            "projections": [{"player_id": "a", "expected_points": 6.0}],
            "rules": {"starter_count": 1, "formations": {"f": ["S"]}, "slot_eligibility": {"S": ["D"]}, "captain_required": False},
        }
        checks = [dict(row) for row in FULL_CHECKS]
        for row in checks:
            if row["name"] == "modifier_rules":
                row["status"] = "blocked"
        checks.append({"name": "deterministic_calculation", "status": "done"})
        out = run({"request": {"kind": "full_lineup"}, "payload": payload, "checks": checks, "blockers": [{"fact": "defense modifier formula unknown", "blocks": ["full_rule_optimum"], "flip_condition": "modifier table is supplied"}]})
        self.assertTrue(out["ok"])
        self.assertEqual(out["run_report"]["completion"]["status"], "complete")
        self.assertEqual(out["run_report"]["completion"]["claim_scope"], "partial_quantitative")


if __name__ == "__main__":
    unittest.main()
