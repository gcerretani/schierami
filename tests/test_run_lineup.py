from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/schierami/scripts"))
from run_lineup import run


class RunLineupTests(unittest.TestCase):
    def test_unknown_payload_stays_conditional(self):
        out = run({"payload": {"roster": []}, "checks": [{"name": "modifier", "status": "blocked"}], "blockers": [{"fact": "modifier formula unknown", "blocks": ["module ranking"]}]})
        self.assertTrue(out["ok"])
        self.assertEqual(out["run_report"]["decision_mode"], "qualitative_conditional")
        self.assertIsNone(out["run_report"]["execution"]["script_ran"])

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


if __name__ == "__main__":
    unittest.main()
