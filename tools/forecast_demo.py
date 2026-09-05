#!/usr/bin/env python3
"""Run the shipped synthetic forecast example, decision bridge and benchmark."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/schierami/scripts'))
from build_forecasts import build
from backtest_forecasts import backtest
from run_forecast import run


def demo(output: Path) -> None:
    source = json.loads((ROOT / 'skills/schierami/examples/forecast-history.json').read_text())
    forecast = build(source)
    eligibility = {'P':['P'], 'D':['D'], 'A':['A']}
    plan = {'forecast_bundle':forecast['forecast_bundle'],
        'sampling':{'method':'monte_carlo', 'samples':2000, 'seed':42},
        'candidates':[{'id':pid, 'formation':'demo', 'starters':[
            {'player_id':'keeper','slot':'P'}, {'player_id':pid,'slot':'D'},
            {'player_id':'forward','slot':'A'}], 'bench':[other]}
            for pid,other in [('steady','risky'),('risky','steady')]],
        'rules':{'max_substitutions':1,'substitution_mode':'ordered_slots','slot_eligibility':eligibility,'modifiers':[]},
        'lineup_rules':{'starter_count':3,'bench_max':1,'captain_required':False,
                        'formations':{'demo':['P','D','A']},'slot_eligibility':eligibility}}
    benchmark = {k:source[k] for k in ['scope','roster','evidence','history']}
    benchmark.update({'models':[dict(source['model'],name='recent',prior_strength=0),source['model']],
        'bootstrap':{'seed':42,'resamples':1000},
        'folds':[{'id':f'f{i}', 'as_of':f'2026-08-{day:02d}T12:00:00+00:00', 'test_match_ids':[f'm{i}'],
                  'decision':{k:v for k,v in plan.items() if k!='forecast_bundle'}} for i,day in [(4,12),(5,16),(6,20)]]})
    output.mkdir(parents=True, exist_ok=True)
    for name,value in [('forecast',forecast),('decision-input',plan),('decision',run(plan)),
                       ('benchmark-input',benchmark),('benchmark',backtest(benchmark))]:
        (output/(name+'.json')).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('Synthetic pipeline completed; no real-world predictive performance is established.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist/forecast-demo')
    demo(parser.parse_args().output)
