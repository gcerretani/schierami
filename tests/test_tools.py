import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/schierami"


def run_tool(name, obj):
    completed = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / name)],
        input=json.dumps(obj),
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


class RuntimeToolTests(unittest.TestCase):
    def test_validator_accepts_example(self):
        obj = json.loads((SKILL / "examples/lineup.json").read_text(encoding="utf-8"))
        code, out = run_tool("validate_lineup.py", obj)
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(out["starters"], 2)

    def test_validator_rejects_duplicate_player(self):
        obj = {
            "roster": [{"id": "x", "roles": ["P", "D"]}],
            "lineup": {
                "formation": "1-1",
                "starters": [
                    {"player_id": "x", "slot": "P"},
                    {"player_id": "x", "slot": "D1"},
                ],
                "bench": [],
            },
            "rules": {
                "starter_count": 2,
                "formations": {"1-1": ["P", "D1"]},
                "slot_eligibility": {"P": ["P"], "D1": ["D"]},
            },
        }
        code, out = run_tool("validate_lineup.py", obj)
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertTrue(any("more than once" in error for error in out["errors"]))

    def test_scorer_example_has_expected_result(self):
        obj = json.loads((SKILL / "examples/scenario.json").read_text(encoding="utf-8"))
        code, out = run_tool("score_scenario.py", obj)
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(len(out["substitutions"]), 1)
        self.assertEqual(out["player_total"], 30.0)
        self.assertEqual(out["self_modifier_total"], 1.0)
        self.assertEqual(out["total"], 31.0)

    def test_scorer_fails_closed_on_unknown_rule(self):
        obj = json.loads((SKILL / "examples/scenario.json").read_text(encoding="utf-8"))
        obj["rules"]["unsupported_custom_rule"] = True
        code, out = run_tool("score_scenario.py", obj)
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertIn("unsupported rule keys", out["message"])


if __name__ == "__main__":
    unittest.main()
