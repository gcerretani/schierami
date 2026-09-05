#!/usr/bin/env python3
"""Prove the best legal XI for supplied additive expected-point projections."""
from __future__ import annotations
from decimal import Decimal
import json, sys
from typing import Any
from _core import ContractError, decimal_number, normalize_id, reject_unknown, require_array, require_bool, require_decimal, require_int, require_object, require_string, require_string_list

TOP={"roster","projections","rules"}; PLAYER={"id","name","roles"}; PROJ={"player_id","expected_points"}; RULES={"starter_count","formations","slot_eligibility","captain_required","captain_multiplier","locked_starters","excluded_players"}
def emit(x,c): print(json.dumps(x,ensure_ascii=False,indent=2)); raise SystemExit(c)

def parse(data):
    d=require_object(data,"$"); reject_unknown(d,TOP,"$")
    if set(d)!=TOP: raise ContractError("$ requires roster, projections and rules")
    roster={}
    for i,x in enumerate(require_array(d["roster"],"$.roster")):
        p=f"$.roster[{i}]"; x=require_object(x,p); reject_unknown(x,PLAYER,p)
        if "id" not in x or "roles" not in x: raise ContractError(f"{p} requires id and roles")
        pid=normalize_id(x["id"],p+".id")
        if pid in roster: raise ContractError(f"duplicate roster id: {pid}")
        if x.get("name") is not None: require_string(x["name"],p+".name")
        roster[pid]={"name":x.get("name"),"roles":set(require_string_list(x["roles"],p+".roles",nonempty=True))}
    projections={}
    for i,x in enumerate(require_array(d["projections"],"$.projections")):
        p=f"$.projections[{i}]"; x=require_object(x,p); reject_unknown(x,PROJ,p)
        if set(x)!=PROJ: raise ContractError(f"{p} requires player_id and expected_points")
        pid=normalize_id(x["player_id"],p+".player_id")
        if pid not in roster: raise ContractError(f"projection player not in roster: {pid}")
        if pid in projections: raise ContractError(f"duplicate projection for player_id: {pid}")
        projections[pid]=require_decimal(x["expected_points"],p+".expected_points")
    missing=sorted(set(roster)-set(projections))
    if missing: raise ContractError("missing projections for roster players: "+", ".join(missing))
    r=require_object(d["rules"],"$.rules"); reject_unknown(r,RULES,"$.rules")
    miss=sorted({"starter_count","formations","slot_eligibility"}-set(r))
    if miss: raise ContractError("missing rule keys: "+", ".join(miss))
    n=require_int(r["starter_count"],"$.rules.starter_count",1); cap=require_bool(r.get("captain_required",False),"$.rules.captain_required"); mult=require_decimal(r.get("captain_multiplier",1),"$.rules.captain_multiplier")
    if mult<=0: raise ContractError("$.rules.captain_multiplier must be > 0")
    if not cap and mult!=Decimal(1): raise ContractError("captain_multiplier != 1 requires captain_required=true")
    forms={}
    for k,v in require_object(r["formations"],"$.rules.formations").items():
        name=require_string(k,"formation key"); slots=require_string_list(v,f"$.rules.formations.{name}",nonempty=True)
        if len(slots)!=n: raise ContractError(f"formation {name} has {len(slots)} slots but starter_count is {n}")
        forms[name]=slots
    elig={require_string(k,"slot key"):set(require_string_list(v,f"$.rules.slot_eligibility.{k}",nonempty=True)) for k,v in require_object(r["slot_eligibility"],"$.rules.slot_eligibility").items()}
    for f,slots in forms.items():
        u=[s for s in slots if s not in elig]
        if u: raise ContractError(f"formation {f} references slots without eligibility: {', '.join(u)}")
    locked=[normalize_id(x,"locked_starters[]") for x in require_array(r.get("locked_starters",[]),"$.rules.locked_starters")]; excluded=[normalize_id(x,"excluded_players[]") for x in require_array(r.get("excluded_players",[]),"$.rules.excluded_players")]
    if len(locked)!=len(set(locked)) or len(excluded)!=len(set(excluded)): raise ContractError("locked/excluded player lists must not contain duplicates")
    for pid in locked+excluded:
        if pid not in roster: raise ContractError(f"rule references player not in roster: {pid}")
    if set(locked)&set(excluded): raise ContractError("players cannot be both locked and excluded")
    return roster,projections,{"forms":forms,"elig":elig,"cap":cap,"mult":mult,"locked":set(locked),"excluded":set(excluded)}

def optimize(data):
    roster,proj,r=parse(data); available=set(roster)-r["excluded"]; best=None; complete=pruned=0
    for fname in sorted(r["forms"]):
        slots=r["forms"][fname]; cand={s:sorted([p for p in available if roster[p]["roles"]&r["elig"][s]],key=lambda p:(-proj[p],p)) for s in slots}
        if any(not cand[s] for s in slots): continue
        order=sorted(slots,key=lambda s:(len(cand[s]),s)); assign={}
        def bound(i,used,total):
            b=total
            for s in order[i:]:
                v=next((proj[p] for p in cand[s] if p not in used),None)
                if v is None:return None
                b+=v
            if r["cap"]: b+=(r["mult"]-1)*max(proj[p] for p in available)
            return b
        def visit(i,used,total):
            nonlocal best,complete,pruned
            b=bound(i,used,total)
            if b is None or (best and b<best[0]): pruned+=1; return
            if i==len(order):
                if not r["locked"].issubset(used): return
                complete+=1; captain=min(used,key=lambda p:(-proj[p],p)) if r["cap"] else None; extra=(r["mult"]-1)*proj[captain] if captain else Decimal(0); obj=total+extra; ordered=tuple((s,assign[s]) for s in slots); tie=(fname,ordered,captain or "")
                if best is None or obj>best[0] or (obj==best[0] and tie<best[1]): best=(obj,tie,total,extra,captain,ordered)
                return
            s=order[i]; remain=len(order)-i-1
            for p in cand[s]:
                if p in used: continue
                nu=used|{p}
                if len(r["locked"]-nu)>remain: continue
                assign[s]=p; visit(i+1,nu,total+proj[p]); assign.pop(s,None)
        visit(0,set(),Decimal(0))
    if best is None: raise ContractError("no legal lineup satisfies the supplied constraints")
    obj,tie,base,extra,captain,ordered=best
    return {"ok":True,"contract":"optimize_lineup.v1","objective_model":"additive_expected_fantasy_points","optimality":"proven_within_supported_model","formation":tie[0],"starters":[{"slot":s,"player_id":p,"name":roster[p]["name"],"expected_points":decimal_number(proj[p])} for s,p in ordered],"captain_id":captain,"expected_points_base":decimal_number(base),"captain_extra":decimal_number(extra),"objective_value":decimal_number(obj),"complete_lineups_evaluated":complete,"branches_pruned":pruned,"unsupported_in_this_optimizer":["bench-order optimization","substitution outcomes","nonlinear modifiers","opponent-aware objectives","correlated scenario utility"]}
def main():
    try: out=optimize(json.load(sys.stdin))
    except (json.JSONDecodeError,ContractError,KeyError,TypeError) as e: emit({"ok":False,"message":str(e)},1)
    emit(out,0)
if __name__=="__main__": main()
