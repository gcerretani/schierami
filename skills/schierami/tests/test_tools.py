import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def run(name, obj):
    p = subprocess.run([sys.executable, str(ROOT/'scripts'/name)], input=json.dumps(obj), text=True, capture_output=True)
    return p.returncode, json.loads(p.stdout)

def test_validator_valid():
    obj={"roster":[{"id":"g","roles":["P"]},{"id":"d","roles":["D"]}],"lineup":{"formation":"1-1","starters":[{"player_id":"g","slot":"P"},{"player_id":"d","slot":"D1"}],"bench":[]},"rules":{"starter_count":2,"formations":{"1-1":["P","D1"]},"slot_eligibility":{"P":["P"],"D1":["D"]}}}
    code,out=run('validate_lineup.py',obj); assert code==0 and out['ok']

def test_validator_rejects_duplicate():
    obj={"roster":[{"id":"x","roles":["P","D"]}],"lineup":{"formation":"1-1","starters":[{"player_id":"x","slot":"P"},{"player_id":"x","slot":"D1"}],"bench":[]},"rules":{"starter_count":2,"formations":{"1-1":["P","D1"]},"slot_eligibility":{"P":["P"],"D1":["D"]}}}
    code,out=run('validate_lineup.py',obj); assert code==2 and not out['ok']

def test_scorer_substitution_and_modifier():
    obj=json.load(open(ROOT/'examples'/'scenario.json'))
    code,out=run('score_scenario.py',obj); assert code==0 and out['ok']; assert len(out['substitutions'])==1; assert out['self_modifier_total']==1.0
