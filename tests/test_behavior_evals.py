import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
from score_behavior import score


class BehavioralEvalScorerTests(unittest.TestCase):
    def test_example_run_passes_all_cases(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        runs = json.loads((ROOT / "evals/example-passing-runs.json").read_text(encoding="utf-8"))
        result = score(cases, runs)
        self.assertTrue(result["ok"])
        self.assertEqual(result["passed"], result["total"])

    def test_unjustified_qualitative_fallback_fails(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        runs = json.loads((ROOT / "evals/example-passing-runs.json").read_text(encoding="utf-8"))
        target = next(row for row in runs if row["case_id"] == "complete_additive_contract")
        target["decision_mode"] = "qualitative_conditional"
        target["scripts_ran"] = []
        result = score(cases, runs)
        failed = next(row for row in result["results"] if row["case_id"] == "complete_additive_contract")
        self.assertFalse(failed["ok"])
        self.assertTrue(any("decision_mode" in error for error in failed["errors"]))
        self.assertTrue(any("optimize_lineup.py" in error for error in failed["errors"]))


if __name__ == "__main__":
    unittest.main()
