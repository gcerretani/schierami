#!/usr/bin/env python3
"""Compare complete candidate lineups over a supplied weighted scenario ensemble."""
from __future__ import annotations
from decimal import Decimal, localcontext
import json, sys
from typing import Any
from _core import ContractError, decimal_number, normalize_id, reject_unknown, require_array, require_decimal, require_object, require_string, require_string_list
from score_scenario import score, parse_rules, parse_player
from validate_lineup import validate

TOP={"roster","candidates","scenarios","rules","lineup_rules"}; PLAYER={"id","name","roles"}; CAND={"id","formation","starters","bench","captain_id"}; START={"player_id","slot"}; SCEN={"id","weight","outcomes"}; OUT={"player_id","valid_vote","fantasy_points","base_vote"}
def emit(x,c): print(json.dumps(x,ensure_ascii=False,indent=2)); raise SystemExit(c)

def evaluate(data: object)->dict[str,Any]:
    d=require_object(data,"$"); reject_unknown(d,TOP,"$")
    if set(d)!=TOP: raise ContractError("$ requires roster, candidates, scenarios, rules and lineup_rules")
    legality=require_object(d["lineup_rules"],"$.lineup_rules")
    required={"starter_count","bench_max","formations","slot_eligibility","captain_required"}
    if required-set(legality): raise ContractError("lineup_rules requires explicit " + ", ".join(sorted(required-set(legality))))
    scoring=parse_rules(d["rules"])
    declared={k:set(require_string_list(v,"lineup_rules.slot_eligibility[]",nonempty=True)) for k,v in require_object(legality["slot_eligibility"],"lineup_rules.slot_eligibility").items()}
    if declared!=scoring["slot_eligibility"]: raise ContractError("scoring and lineup slot eligibility must agree")
    roster={}
    for i,x in enumerate(require_array(d["roster"],"$.roster")):
        p=f"$.roster[{i}]"; x=require_object(x,p); reject_unknown(x,PLAYER,p)
        if "id" not in x or "roles" not in x: raise ContractError(f"{p} requires id and roles")
        pid=normalize_id(x["id"],p+".id")
        if pid in roster: raise ContractError(f"duplicate roster id: {pid}")
        roster[pid]={"roles":require_string_list(x["roles"],p+".roles",nonempty=True),"name":x.get("name")}
    candidates=[]; ids=set()
    for i,x in enumerate(require_array(d["candidates"],"$.candidates")):
        p=f"$.candidates[{i}]"; x=require_object(x,p); reject_unknown(x,CAND,p)
        if {"id","formation","starters","bench"}-set(x): raise ContractError(f"{p} requires id, formation, starters and bench")
        checked=validate({"roster":d["roster"],"lineup":{k:v for k,v in x.items() if k!="id"},"rules":legality})
        if not checked["ok"]: raise ContractError(f"candidate {x['id']} is illegal: " + "; ".join(checked["errors"]))
        if legality["captain_required"] or x.get("captain_id") is not None:
            raise ContractError("scenario evaluator does not support captain scoring; do not omit a real captain rule")
        cid=require_string(x["id"],p+".id")
        if cid in ids: raise ContractError(f"duplicate candidate id: {cid}")
        ids.add(cid); used=set(); slots=set(); starters=[]
        for j,s in enumerate(require_array(x["starters"],p+".starters")):
            q=f"{p}.starters[{j}]"; s=require_object(s,q); reject_unknown(s,START,q)
            if set(s)!=START: raise ContractError(f"{q} requires player_id and slot")
            pid=normalize_id(s["player_id"],q+".player_id"); slot=require_string(s["slot"],q+".slot")
            if pid not in roster: raise ContractError(f"candidate {cid} references player not in roster: {pid}")
            if pid in used or slot in slots: raise ContractError(f"candidate {cid} contains duplicate player or slot")
            used.add(pid); slots.add(slot); starters.append({"player_id":pid,"slot":slot})
        bench=[]
        for j,v in enumerate(require_array(x["bench"],p+".bench")):
            pid=normalize_id(v,f"{p}.bench[{j}]")
            if pid not in roster: raise ContractError(f"candidate {cid} references player not in roster: {pid}")
            if pid in used: raise ContractError(f"candidate {cid} uses player more than once: {pid}")
            used.add(pid); bench.append(pid)
        candidates.append({"id":cid,"starters":starters,"bench":bench})
    if not candidates: raise ContractError("$.candidates must not be empty")
    scenarios=[]; sids=set(); totalw=Decimal(0)
    for i,x in enumerate(require_array(d["scenarios"],"$.scenarios")):
        p=f"$.scenarios[{i}]"; x=require_object(x,p); reject_unknown(x,SCEN,p)
        if set(x)!=SCEN: raise ContractError(f"{p} requires id, weight and outcomes")
        sid=require_string(x["id"],p+".id"); w=require_decimal(x["weight"],p+".weight")
        if sid in sids or w<=0: raise ContractError(f"invalid or duplicate scenario: {sid}")
        sids.add(sid); totalw+=w; outcomes={}
        for j,o in enumerate(require_array(x["outcomes"],p+".outcomes")):
            q=f"{p}.outcomes[{j}]"; o=require_object(o,q); reject_unknown(o,OUT,q)
            if "player_id" not in o or "valid_vote" not in o: raise ContractError(f"{q} requires player_id and valid_vote")
            pid=normalize_id(o["player_id"],q+".player_id")
            if pid not in roster or pid in outcomes: raise ContractError(f"scenario {sid} has unknown or duplicate player outcome: {pid}")
            parse_player({**o,"roles":roster[pid]["roles"]},q,False)
            outcomes[pid]=dict(o)
        missing=sorted(set(roster)-set(outcomes))
        if missing: raise ContractError(f"scenario {sid} missing roster outcomes: {', '.join(missing)}")
        scenarios.append({"id":sid,"weight":w,"outcomes":outcomes})
    if not scenarios: raise ContractError("$.scenarios must not be empty")
    rankings=[]
    for c in candidates:
        exp=Decimal(0); rows=[]
        for s in scenarios:
            prob=s["weight"]/totalw
            starters=[{"player_id":a["player_id"],"slot":a["slot"],"roles":roster[a["player_id"]]["roles"],**{k:v for k,v in s["outcomes"][a["player_id"]].items() if k!="player_id"}} for a in c["starters"]]
            bench=[{"player_id":pid,"roles":roster[pid]["roles"],**{k:v for k,v in s["outcomes"][pid].items() if k!="player_id"}} for pid in c["bench"]]
            try: result=score({"starters":starters,"bench":bench,"rules":d["rules"]})
            except ContractError as e: raise ContractError(f"candidate {c['id']} / scenario {s['id']}: {e}") from None
            total=require_decimal(result["total"],"result.total"); exp+=prob*total; rows.append({"scenario_id":s["id"],"probability":decimal_number(prob),"total":decimal_number(total),"substitutions":result["substitutions"],"modifier_details":result["modifier_details"]})
        var=sum((require_decimal(r["probability"],"prob")*(require_decimal(r["total"],"total")-exp)**2 for r in rows),Decimal(0))
        with localcontext() as ctx: ctx.prec=28; sd=var.sqrt()
        totals=[require_decimal(r["total"],"total") for r in rows]
        rankings.append({"candidate_id":c["id"],"expected_total":decimal_number(exp),"standard_deviation":decimal_number(sd),"minimum_total":decimal_number(min(totals)),"maximum_total":decimal_number(max(totals)),"scenario_results":rows,"_e":exp})
    rankings.sort(key=lambda x:(-x["_e"],x["candidate_id"]))
    for i,x in enumerate(rankings,1): x.pop("_e"); x["rank"]=i
    return {"ok":True,"contract":"evaluate_lineups.v2","legality_validated":True,"objective_model":"expected_own_fantasy_score_over_supplied_scenarios","best_candidate_id":rankings[0]["candidate_id"],"optimality":"best_among_supplied_candidates_only","scenario_weights_normalized":True,"rankings":rankings}
def main():
    try: out=evaluate(json.load(sys.stdin))
    except (json.JSONDecodeError,ContractError,KeyError,TypeError) as e: emit({"ok":False,"message":str(e)},1)
    emit(out,0)
if __name__=="__main__": main()
