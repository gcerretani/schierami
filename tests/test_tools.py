import copy, json
from pathlib import Path
import subprocess, sys, unittest
ROOT=Path(__file__).resolve().parents[1]; SKILL=ROOT/"skills/schierami"
def run_tool(name,obj):
    p=subprocess.run([sys.executable,str(SKILL/"scripts"/name)],input=json.dumps(obj),text=True,capture_output=True,check=False)
    return p.returncode,json.loads(p.stdout)
class ToolTests(unittest.TestCase):
    def lineup(self): return json.loads((SKILL/"examples/lineup.json").read_text())
    def scenario(self): return json.loads((SKILL/"examples/scenario.json").read_text())
    def test_validator_accepts_example(self):
        c,o=run_tool("validate_lineup.py",self.lineup()); self.assertEqual(c,0,o); self.assertEqual(o["contract"],"validate_lineup.v2")
    def test_validator_rejects_unknown_rule(self):
        x=self.lineup(); x["rules"]["minimum_defenders"]=4; c,o=run_tool("validate_lineup.py",x); self.assertEqual(c,1); self.assertIn("unsupported keys",o["message"])
    def test_validator_rejects_fractional_count(self):
        x=self.lineup(); x["rules"]["starter_count"]=2.5; c,o=run_tool("validate_lineup.py",x); self.assertEqual(c,1)
    def test_scorer_example(self):
        c,o=run_tool("score_scenario.py",self.scenario()); self.assertEqual(c,0,o); self.assertEqual(o["total"],31.0)
    def test_scorer_rejects_string_boolean(self):
        x=self.scenario(); x["starters"][0]["valid_vote"]="false"; c,o=run_tool("score_scenario.py",x); self.assertEqual(c,1)
    def test_scorer_rejects_nan(self):
        x=self.scenario(); x["starters"][0]["fantasy_points"]="NaN"; c,o=run_tool("score_scenario.py",x); self.assertEqual(c,1)
    def test_scorer_rejects_duplicate_identity(self):
        x=self.scenario(); x["bench"].append(copy.deepcopy(x["bench"][0])); c,o=run_tool("score_scenario.py",x); self.assertEqual(c,1)
    def test_decimal_threshold_exact(self):
        x={"starters":[{"player_id":p,"slot":s,"roles":["D"],"valid_vote":True,"fantasy_points":6,"base_vote":6.1} for p,s in [("a","S1"),("b","S2"),("c","S3")]],"bench":[],"rules":{"max_substitutions":0,"substitution_mode":"ordered_slots","slot_eligibility":{"S1":["D"],"S2":["D"],"S3":["D"]},"modifiers":[{"name":"m","type":"threshold_average","selectors":[{"slots":["S1","S2","S3"],"take_best":3}],"thresholds":[{"min":6.1,"points":3}],"target":"self"}]}}
        c,o=run_tool("score_scenario.py",x); self.assertEqual(c,0,o); self.assertEqual(o["total"],21.0)
    def test_optimizer_finds_nonobvious_best_xi(self):
        x={"roster":[{"id":"p","roles":["P"]},{"id":"d","roles":["D"]},{"id":"c","roles":["C"]},{"id":"x","roles":["D","C"]},{"id":"a","roles":["A"]}],"projections":[{"player_id":"p","expected_points":6},{"player_id":"d","expected_points":6.1},{"player_id":"c","expected_points":6.4},{"player_id":"x","expected_points":6.3},{"player_id":"a","expected_points":7}],"rules":{"starter_count":4,"formations":{"f":["P","D","C","A"]},"slot_eligibility":{"P":["P"],"D":["D"],"C":["C"],"A":["A"]},"captain_required":True,"captain_multiplier":2,"locked_starters":[],"excluded_players":[]}}
        c,o=run_tool("optimize_lineup.py",x); self.assertEqual(c,0,o); self.assertEqual(o["optimality"],"proven_within_supported_model"); self.assertEqual({r["player_id"] for r in o["starters"]},{"p","x","c","a"})
    def test_optimizer_fails_closed_on_nonlinear_rule(self):
        x={"roster":[{"id":"p","roles":["P"]}],"projections":[{"player_id":"p","expected_points":6}],"rules":{"starter_count":1,"formations":{"f":["P"]},"slot_eligibility":{"P":["P"]},"modifier":True}}
        c,o=run_tool("optimize_lineup.py",x); self.assertEqual(c,1); self.assertIn("unsupported keys",o["message"])
if __name__=="__main__": unittest.main()
