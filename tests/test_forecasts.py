"""Synthetic numerical/contract tests, not a football-accuracy benchmark."""
from copy import deepcopy
from itertools import product
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/schierami/scripts"
sys.path.insert(0, str(SCRIPTS))
from _core import ContractError
from backtest_forecasts import backtest
from build_forecasts import build
from forecast_core import OUTCOME, summaries, validate_bundle
from forecast_metrics import aggregate, crps, observations
from run_forecast import run, scenarios
from run_lineup import run as dispatch
from tools.build_release import build as package


def history_input():
    return json.loads((ROOT / 'skills/schierami/examples/forecast-history.json').read_text())


def decision(bundle):
    return {"forecast_bundle": bundle, "sampling": {"method": "exact", "max_scenarios": 10000},
        "candidates": [{"id": pid, "formation": "demo", "starters": [
            {"player_id": "keeper", "slot": "P"}, {"player_id": pid, "slot": "D"},
            {"player_id": "forward", "slot": "A"}], "bench": [other]}
            for pid, other in [("steady", "risky"), ("risky", "steady")]],
        "lineup_rules": {"starter_count": 3, "bench_max": 1, "captain_required": False,
                         "formations": {"demo": ["P", "D", "A"]},
                         "slot_eligibility": {"P": ["P"], "D": ["D"], "A": ["A"]}},
        "rules": {"substitution_mode": "ordered_slots", "max_substitutions": 1,
                  "slot_eligibility": {"P": ["P"], "D": ["D"], "A": ["A"]}, "modifiers": []}}


def benchmark_input():
    d = history_input()
    d.pop('as_of'); d.pop('deadline'); model = d.pop('model')
    d['models'] = [dict(model, name='recent', prior_strength=0), model]
    d['bootstrap'] = {'seed': 7, 'resamples': 100}
    d['folds'] = [{'id':f'f{i}', 'as_of':f'2026-08-{day:02d}T12:00:00+00:00',
                   'test_match_ids':[f'm{i}']} for i,day in [(4,12),(5,16),(6,20)]]
    return d


class ForecastContractTests(unittest.TestCase):
    def test_engine_version_matches_manifest(self):
        from forecast_core import ENGINE_VERSION
        manifest=json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(ENGINE_VERSION,manifest['version'])

    def test_build_reproducible_and_probabilities_coherent(self):
        a=build(history_input()); b=build(history_input())
        self.assertEqual(a,b)
        self.assertEqual(a['forecast_bundle']['model']['status'],'baseline_unvalidated')
        for row in a['player_forecasts']:
            self.assertLessEqual(row['p_start'],row['p_appearance'])
            self.assertGreaterEqual(row['p_valid_vote'],0)
            self.assertLessEqual(row['p_valid_vote'],1)
        self.assertTrue(validate_bundle(a['forecast_bundle']))

    def test_no_future_information_changes_forecasts(self):
        d=history_input(); d['as_of']='2026-08-12T12:00:00+00:00'
        a=build(d)
        for row in d['history']:
            if row['match_id'] in ['m4','m5','m6'] and row['valid_vote']:
                row['fantasy_points']=1000
        b=build(d)
        self.assertEqual(a['player_forecasts'],b['player_forecasts'])
        self.assertEqual(a['training_audit']['excluded_future_rows'],12)
        self.assertNotEqual(a['forecast_bundle']['input_sha256'],b['forecast_bundle']['input_sha256'])

    def test_weighted_mean_matches_independent_oracle(self):
        d=history_input(); d['model']['window']=1; d['model']['prior_strength']=2
        rows={r['player_id']:r for r in build(d)['player_forecasts']}
        # Most recent risky has no vote; peer steady has 6.5. (0 + 2*6.5)/3.
        self.assertAlmostEqual(rows['risky']['expected_points'],13/3)
        self.assertAlmostEqual(rows['risky']['p_valid_vote'],2/3)

    def test_cold_start_is_explicit(self):
        d=history_input(); d['history']=[r for r in d['history'] if r['player_id']!='risky']
        result=build(d)
        r=next(x for x in result['training_audit']['players'] if x['player_id']=='risky')
        self.assertTrue(r['cold_start'])

    def test_no_support_fails(self):
        d=history_input(); d['history']=[r for r in d['history'] if r['player_id']!='keeper']
        with self.assertRaisesRegex(ContractError,'no historical support'): build(d)

    def test_unknown_fields_rejected_at_each_level(self):
        for mutate in [lambda x:x.update(extra=True),lambda x:x['scope'].update(extra=True),
                       lambda x:x['model'].update(extra=True),lambda x:x['history'][0].update(extra=True),
                       lambda x:x['evidence'][0].update(extra=True)]:
            d=history_input(); mutate(d)
            with self.assertRaises(ContractError): build(d)

    def test_bad_types_and_nonfinite_values_rejected(self):
        for key,value in [('started','false'),('minutes',float('nan')),('fantasy_points',float('inf'))]:
            d=history_input(); d['history'][0][key]=value
            with self.assertRaises(ContractError): build(d)
        d=history_input(); d['model']['window']=3.5
        with self.assertRaises(ContractError): build(d)

    def test_duplicate_observation_is_not_extra_evidence(self):
        d=history_input(); d['history'].append(deepcopy(d['history'][0]))
        with self.assertRaises(ContractError): build(d)

    def test_same_origin_not_counted_as_multiple_origins(self):
        d=history_input()
        for e in d['evidence']: e['origin_id']='one-origin'
        self.assertEqual(build(d)['training_audit']['evidence_origins'],['one-origin'])

    def test_missing_timezone_and_cutoff_after_deadline_rejected(self):
        for stamp in ['2026-08-24T12:00:00','2026-08-26T12:00:00+00:00']:
            d=history_input(); d['as_of']=stamp
            with self.assertRaises(ContractError): build(d)

    def test_stale_or_conflicted_evidence_rejected(self):
        for key,value in [('status','conflicted'),('valid_until','2026-08-23T12:00:00+00:00')]:
            d=history_input(); d['evidence'][-1][key]=value
            with self.assertRaises(ContractError): build(d)

    def test_late_capture_excluded_even_if_publication_was_early(self):
        d=history_input(); d['evidence'][-1]['retrieved_at']='2026-08-26T12:00:00+00:00'
        self.assertEqual(build(d)['training_audit']['excluded_future_rows'],4)

    def test_no_vote_not_implicitly_inferred_from_minutes(self):
        d=history_input(); r=d['history'][0]; r.update(started=False,minutes=0,valid_vote=True)
        build(d)  # Explicit office vote remains a valid outcome.
        r.update(valid_vote=False)
        with self.assertRaises(ContractError): build(d)

    def test_bundle_rejects_overlap_missing_players_and_false_calibration(self):
        b=build(history_input())['forecast_bundle']
        for mutate in [lambda x:x['blocks'].append(deepcopy(x['blocks'][0])),
                       lambda x:x['blocks'].pop(),lambda x:x['model'].update(status='calibrated'),
                       lambda x:x.update(independent_blocks=False)]:
            x=deepcopy(b); mutate(x)
            with self.assertRaises(ContractError): validate_bundle(x)


class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.bundle=build(history_input())['forecast_bundle']

    def test_exact_means_match_marginals(self):
        ss,_=scenarios(self.bundle,{'method':'exact','max_scenarios':10000})
        total=sum(s['weight'] for s in ss)
        for row in summaries(self.bundle):
            mean=sum(s['weight']*next(r['fantasy_points'] for r in s['outcomes'] if r['player_id']==row['player_id']) for s in ss)/total
            self.assertAlmostEqual(mean,row['expected_points'])

    def test_nonlinear_expectation_is_not_modifier_of_mean_vote(self):
        b=deepcopy(self.bundle); b["roster"]=[r for r in b["roster"] if r["id"] in ["keeper","steady"]]
        b["blocks"]=[{"id":"joint","player_ids":["keeper","steady"],"evidence_ids":["s6"],"states":[
            {"weight":1,"outcomes":[{"player_id":pid,"started":True,"minutes":90,"valid_vote":True,
                "base_vote":v,"fantasy_points":v} for pid in ["keeper","steady"]]} for v in [4,8]]}]
        b["independent_blocks"]=False
        d=decision(b); d["candidates"]=[{"id":"only","formation":"two","starters":[
            {"player_id":"keeper","slot":"P"},{"player_id":"steady","slot":"D"}],"bench":[]}]
        eligibility={"P":["P"],"D":["D"]}
        d["lineup_rules"].update(starter_count=2,formations={"two":["P","D"]},slot_eligibility=eligibility)
        d["rules"].update(slot_eligibility=eligibility,modifiers=[{"type":"threshold_average",
             "selectors":[{"slots":["P","D"],"take_best":2}],"thresholds":[{"min":6,"points":3}]}])
        r=run(d)
        self.assertAlmostEqual(r["rankings"][0]["expected_total"],13.5)
        self.assertNotEqual(r["rankings"][0]["expected_total"],15)

    def test_mc_seed_reproducible_and_close_to_exact(self):
        config={'method':'monte_carlo','samples':3000,'seed':42}
        a,info=scenarios(self.bundle,config); b,_=scenarios(self.bundle,config)
        self.assertEqual(a,b); self.assertEqual(info['draws'],3000)
        self.assertEqual(sum(s['weight'] for s in a),3000)
        mean=sum(s['weight']*next(r['fantasy_points'] for r in s['outcomes'] if r['player_id']=='risky') for s in a)/3000
        expected=next(r['expected_points'] for r in summaries(self.bundle) if r['player_id']=='risky')
        self.assertAlmostEqual(mean,expected,delta=.3)

    def test_joint_states_are_never_broken(self):
        b=deepcopy(self.bundle); b['roster']=[p for p in b['roster'] if p['id'] in ['risky','steady']]
        empty={'started':False,'minutes':0,'valid_vote':False,'base_vote':None,'fantasy_points':0}
        active={'started':True,'minutes':90,'valid_vote':True,'base_vote':6,'fantasy_points':6}
        b['blocks']=[{'id':'joint','player_ids':['risky','steady'],'evidence_ids':['s6'],
             'states':[{'weight':1,'outcomes':[dict(active,player_id='risky'),dict(empty,player_id='steady')]},
                       {'weight':1,'outcomes':[dict(empty,player_id='risky'),dict(active,player_id='steady')]}]}]
        b['independent_blocks']=False; b['model']['status']='supplied_unvalidated'
        for config in [{'method':'exact','max_scenarios':10},{'method':'monte_carlo','samples':50,'seed':1}]:
            ss,_=scenarios(b,config)
            self.assertTrue(all(sum(r['valid_vote'] for r in s['outcomes'])==1 for s in ss))

    def test_exact_budget_does_not_silently_switch_method(self):
        with self.assertRaisesRegex(ContractError,'exceeds budget'):
            scenarios(self.bundle,{'method':'exact','max_scenarios':1})

    def test_dispatch_and_candidate_legality(self):
        d=decision(self.bundle); result=dispatch({'payload':d})
        self.assertEqual(result['run_report']['execution']['script_ran'],'run_forecast.py')
        self.assertTrue(result['result']['legality_validated'])
        d['candidates'][0]['starters'][1]['player_id']='keeper'
        with self.assertRaises(ContractError): run(d)

    def test_monte_carlo_narrows_claim_and_reports_paired_noise(self):
        d=decision(self.bundle); d['sampling']={'method':'monte_carlo','samples':100,'seed':7}
        r=run(d)
        self.assertEqual(r['optimality'],'best_among_supplied_candidates_on_sample_only')
        self.assertIsNotNone(r['comparisons_to_selected'][0]['paired_mc_standard_error'])

    def test_opponent_effect_not_ignored(self):
        d=decision(self.bundle); d['rules']['modifiers']=[{'type':'threshold_average','target':'opponent',
           'selectors':[{'slots':['P'],'take_best':1}],'thresholds':[{'min':6,'points':-1}]}]
        with self.assertRaisesRegex(ContractError,'opponent-target'): run(d)

    def test_modifiers_are_evaluated_per_scenario(self):
        d=decision(self.bundle); d['rules']['modifiers']=[{'name':'demo','type':'threshold_average',
           'selectors':[{'slots':['P'],'take_best':1}],'thresholds':[{'min':6,'points':3}],'target':'self'}]
        without=run(decision(self.bundle)); with_modifier=run(d)
        self.assertAlmostEqual(with_modifier['rankings'][0]['expected_total'],without['rankings'][0]['expected_total']+3)


class MetricsAndBenchmarkTests(unittest.TestCase):
    def test_crps_matches_quadratic_oracle(self):
        rng=random.Random(17)
        for _ in range(25):
            w=[rng.random() for _ in range(10)]; total=sum(w)
            v=[(a/total,rng.uniform(-3,10)) for a in w]; y=rng.uniform(-3,10)
            oracle=sum(p*abs(x-y) for p,x in v)-sum(p*q*abs(x-z) for p,x in v for q,z in v)/2
            self.assertAlmostEqual(crps(v,y),oracle)

    def test_metrics_never_hide_impossible_events_with_clipping(self):
        b=build(history_input())['forecast_bundle']
        actual={'player_id':'keeper','started':False,'minutes':0,'valid_vote':False,'base_vote':None,'fantasy_points':0}
        m=aggregate(observations(b,[actual]))
        self.assertEqual(m['start']['brier'],1)
        self.assertIsNone(m['start']['log_loss'])
        self.assertEqual(m['start']['infinite_log_losses'],1)
        self.assertAlmostEqual(m['fantasy_points']['mae'],6)
        self.assertAlmostEqual(m['fantasy_points']['crps'],6)

    def test_conditional_vote_metric_reports_missing_forecasts(self):
        b=build(history_input())["forecast_bundle"]
        for block in b["blocks"]:
            for state in block["states"]:
                for row in state["outcomes"]: row["base_vote"]=None
        actual={"player_id":"keeper","started":True,"minutes":90,"valid_vote":True,"base_vote":6,"fantasy_points":6}
        metric=aggregate(observations(b,[actual]))["base_vote_conditional"]
        self.assertEqual(metric["missing_forecast_count"],1)
        self.assertIsNone(metric["mae"])

    def test_walk_forward_reproducible_and_all_targets_evaluated(self):
        d=benchmark_input(); a=backtest(d); b=backtest(d)
        self.assertEqual(a,b)
        self.assertEqual(a['models'][0]['metrics']['n'],12)
        self.assertFalse(a['predictive_superiority_established'])
        self.assertEqual(len(a['folds']),3)
        self.assertIsNotNone(a['comparisons'][0]['paired_fold_bootstrap_percentile_95'])

    def test_invalid_fold_order_and_reused_test_target_rejected(self):
        for mutate in [lambda d:d['folds'].reverse(),lambda d:d['folds'][1].update(test_match_ids=['m4'])]:
            d=benchmark_input(); mutate(d)
            with self.assertRaises(ContractError): backtest(d)

    def test_test_outcome_cannot_change_earlier_decision(self):
        d=benchmark_input(); d['folds']=d['folds'][:1]
        plan=decision(build(history_input())['forecast_bundle']); plan.pop('forecast_bundle')
        plan['sampling']={'method':'monte_carlo','samples':30,'seed':4}
        d['folds'][0]['decision']=plan
        before=backtest(d)
        for row in d['history']:
            if row['match_id']=='m4' and row['player_id']=='steady': row['fantasy_points']=100
        after=backtest(d)
        for a,b in zip(before['folds'][0]['models'],after['folds'][0]['models']):
            self.assertEqual(a['decision']['selected_candidate_id'],b['decision']['selected_candidate_id'])
        self.assertIsNone(before['comparisons'][0]['paired_fold_bootstrap_percentile_95'])

    def test_incomplete_decision_targets_fail_closed(self):
        d=benchmark_input(); d['folds']=d['folds'][:1]
        d['history']=[r for r in d['history'] if not(r['match_id']=='m4' and r['player_id']=='keeper')]
        plan=decision(build(history_input())['forecast_bundle']); plan.pop('forecast_bundle')
        d['folds'][0]['decision']=plan
        with self.assertRaisesRegex(ContractError,'exactly one'): backtest(d)

    def test_no_test_targets_silently_dropped(self):
        d=benchmark_input(); d['folds'][0]['test_match_ids']=['does-not-exist']
        with self.assertRaises(ContractError): backtest(d)

    def test_duplicate_model_names_rejected(self):
        d=benchmark_input(); d['models'][1]['name']=d['models'][0]['name']
        with self.assertRaises(ContractError): backtest(d)

    def test_cli_errors_are_json_without_traceback(self):
        for script in ['build_forecasts.py','run_forecast.py','backtest_forecasts.py','run_lineup.py']:
            for invalid in ['[]','{"scope":1,"scope":2}','{"bad":NaN}']:
                p=subprocess.run([sys.executable,str(SCRIPTS/script)],input=invalid,text=True,capture_output=True)
                self.assertEqual(p.returncode,1,(script,p.stdout,p.stderr))
                self.assertFalse(json.loads(p.stdout)['ok'])
                self.assertNotIn('Traceback',p.stderr)

    def test_packaged_skill_runs_without_repository_or_installed_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            files=package(ROOT,Path(tmp)/'dist')
            with zipfile.ZipFile(files['skill']) as z: z.extractall(Path(tmp)/'isolated')
            script=Path(tmp)/'isolated/schierami/scripts/build_forecasts.py'
            p=subprocess.run([sys.executable,'-S',str(script)],input=json.dumps(history_input()),
                             text=True,capture_output=True,cwd=tmp)
            self.assertEqual(p.returncode,0,p.stderr+p.stdout)
            self.assertTrue(json.loads(p.stdout)['ok'])


if __name__ == '__main__':
    unittest.main()
