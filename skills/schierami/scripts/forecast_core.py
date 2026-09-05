"""Versioned probabilistic contracts. No network, private state or fitted claims."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import sys
from typing import Any, Callable

from _core import ContractError, require_bool, require_int, require_string

ENGINE_VERSION = "0.4.0"
SCOPE = {"competition", "season", "scoring_id", "vote_provider"}
OUTCOME = {"player_id", "started", "minutes", "valid_vote", "base_vote", "fantasy_points"}


def obj(value: Any, keys: set[str], path: str, optional: set[str] = frozenset()) -> dict:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be an object")
    missing, extra = keys - value.keys(), value.keys() - keys - optional
    if missing or extra:
        raise ContractError(f"{path}: missing {sorted(missing)}; unsupported {sorted(extra)}")
    return value


def array(value: Any, path: str, *, empty: bool = False) -> list:
    if not isinstance(value, list) or (not value and not empty):
        raise ContractError(f"{path} must be {'an' if empty else 'a nonempty'} array")
    return value


def text(value: Any, path: str) -> str:
    value = require_string(value, path)
    if value != value.strip():
        raise ContractError(f"{path} must not have surrounding whitespace")
    return value


def number(value: Any, path: str, minimum: float = -1e12, maximum: float = 1e12) -> float:
    if type(value) not in (int, float):
        raise ContractError(f"{path} must be a JSON number")
    if not minimum <= value <= maximum or not math.isfinite(value):
        raise ContractError(f"{path} must be finite and in [{minimum}, {maximum}]")
    return float(value)


def time(value: Any, path: str) -> datetime:
    value = text(value, path)
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ContractError(f"{path} must be an ISO timestamp") from None
    if result.tzinfo is None:
        raise ContractError(f"{path} requires a timezone")
    return result.astimezone(timezone.utc)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def scope(value: Any) -> dict:
    value = obj(value, SCOPE, "scope")
    return {k: text(v, "scope." + k) for k, v in value.items()}


def roster(value: Any) -> dict[str, dict]:
    result = {}
    for row in array(value, "roster"):
        row = obj(row, {"id", "roles"}, "roster[]", {"name"})
        pid = text(row["id"], "roster.id")
        roles = [text(x, "role") for x in array(row["roles"], "roles")]
        if pid in result or len(roles) != len(set(roles)):
            raise ContractError("duplicate roster identity or role")
        if "name" in row:
            text(row["name"], "roster.name")
        result[pid] = dict(row)
    return result


def outcome(value: Any) -> dict:
    row = obj(value, OUTCOME, "outcome")
    text(row["player_id"], "outcome.player_id")
    started = require_bool(row["started"], "outcome.started")
    valid = require_bool(row["valid_vote"], "outcome.valid_vote")
    minutes = number(row["minutes"], "outcome.minutes", 0, 180)
    number(row["fantasy_points"], "outcome.fantasy_points")
    if started and minutes == 0:
        raise ContractError("started requires positive unrounded minutes")
    if not valid and (row["fantasy_points"] != 0 or row["base_vote"] is not None):
        raise ContractError("no valid vote requires zero fantasy_points and null base_vote")
    if row["base_vote"] is not None:
        number(row["base_vote"], "outcome.base_vote")
    # A valid office vote can exist with zero minutes. Never infer votes from minutes.
    return dict(row)


def evidence(value: Any) -> dict[str, dict]:
    result = {}
    fields = {"id", "origin_id", "locator", "published_at", "retrieved_at", "status", "valid_until"}
    for row in array(value, "evidence"):
        row = obj(row, fields, "evidence[]")
        for k in ("id", "origin_id", "locator"):
            text(row[k], "evidence." + k)
        if row["id"] in result:
            raise ContractError("duplicate evidence id")
        if row["status"] not in ("confirmed", "user_stated", "hypothesis", "conflicted"):
            raise ContractError("unsupported evidence status")
        published = time(row["published_at"], "published_at")
        if time(row["retrieved_at"], "retrieved_at") < published:
            raise ContractError("retrieved_at predates published_at")
        if row["valid_until"] is not None and time(row["valid_until"], "valid_until") < published:
            raise ContractError("valid_until predates published_at")
        result[row["id"]] = dict(row)
    return result


def usable(refs: Any, ledger: dict, as_of: datetime) -> list[str]:
    ids = [text(x, "evidence_id") for x in array(refs, "evidence_ids")]
    if len(ids) != len(set(ids)):
        raise ContractError("duplicate evidence reference")
    for eid in ids:
        if eid not in ledger:
            raise ContractError(f"unknown evidence: {eid}")
        row = ledger[eid]
        if row["status"] not in ("confirmed", "user_stated"):
            raise ContractError(f"unresolved evidence: {eid}")
        if time(row["retrieved_at"], "retrieved_at") > as_of:
            raise ContractError(f"evidence not captured by forecast cutoff: {eid}")
        if row["valid_until"] is not None and time(row["valid_until"], "valid_until") < as_of:
            raise ContractError(f"expired evidence: {eid}")
    return ids


def validate_bundle(value: Any) -> dict:
    keys = {"contract", "scope", "as_of", "deadline", "roster", "evidence", "model",
            "blocks", "independent_blocks", "input_sha256"}
    b = obj(value, keys, "forecast_bundle")
    if b["contract"] != "forecast_bundle.v1":
        raise ContractError("unsupported forecast bundle version")
    scope(b["scope"])
    cutoff = time(b["as_of"], "as_of")
    if cutoff > time(b["deadline"], "deadline"):
        raise ContractError("forecast cutoff is after deadline")
    players, ledger = roster(b["roster"]), evidence(b["evidence"])
    text(b["input_sha256"], "input_sha256")
    if len(b["input_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in b["input_sha256"]):
        raise ContractError("input_sha256 must be a lowercase SHA-256 hex digest")
    model = obj(b["model"], {"name", "version", "status", "assumptions"}, "model")
    for k in ("name", "version"):
        text(model[k], "model." + k)
    if model["status"] not in ("baseline_unvalidated", "supplied_unvalidated"):
        raise ContractError("v1 bundles cannot self-certify calibration or predictive superiority")
    for a in array(model["assumptions"], "assumptions"):
        text(a, "assumption")
    independent = require_bool(b["independent_blocks"], "independent_blocks")
    blocks = array(b["blocks"], "blocks")
    if len(blocks) > 1 and not independent:
        raise ContractError("dependent players must be represented inside one joint block")
    covered, block_ids = set(), set()
    for block in blocks:
        obj(block, {"id", "player_ids", "evidence_ids", "states"}, "block")
        bid = text(block["id"], "block.id")
        if bid in block_ids:
            raise ContractError("duplicate block id")
        block_ids.add(bid)
        ids = [text(x, "player_id") for x in array(block["player_ids"], "player_ids")]
        if len(ids) != len(set(ids)) or covered.intersection(ids) or not set(ids) <= players.keys():
            raise ContractError("unknown, repeated or overlapping block player")
        covered.update(ids)
        usable(block["evidence_ids"], ledger, cutoff)
        for state in array(block["states"], "states"):
            obj(state, {"weight", "outcomes"}, "state")
            if number(state["weight"], "state.weight", 0) <= 0:
                raise ContractError("state weight must be positive")
            rows = [outcome(x) for x in array(state["outcomes"], "state.outcomes")]
            if len(rows) != len(ids) or {r["player_id"] for r in rows} != set(ids):
                raise ContractError("state must contain each block player exactly once")
    if covered != players.keys():
        raise ContractError("blocks must partition the whole forecast roster")
    return b


def marginals(bundle: dict) -> dict[str, list[tuple[float, dict]]]:
    b = validate_bundle(bundle)
    result = {r["id"]: [] for r in b["roster"]}
    for block in b["blocks"]:
        total = math.fsum(s["weight"] for s in block["states"])
        for state in block["states"]:
            for row in state["outcomes"]:
                result[row["player_id"]].append((state["weight"] / total, row))
    return result


def summaries(bundle: dict) -> list[dict]:
    rows = []
    for pid, distribution in marginals(bundle).items():
        mean = lambda field: math.fsum(p * r[field] for p, r in distribution)
        vote_mass = math.fsum(p for p, r in distribution if r["valid_vote"] and r["base_vote"] is not None)
        rows.append({"player_id": pid, "p_start": mean("started"),
                     "p_appearance": math.fsum(p for p, r in distribution if r["minutes"] > 0),
                     "p_valid_vote": mean("valid_vote"), "expected_minutes": mean("minutes"),
                     "expected_points": mean("fantasy_points"), "base_vote_probability_mass": vote_mass,
                     "expected_base_vote_when_present": (math.fsum(p * r["base_vote"] for p, r in distribution
                         if r["base_vote"] is not None) / vote_mass if vote_mass else None)})
    return rows


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_request() -> Any:
    return json.load(sys.stdin, object_pairs_hook=_pairs)


def cli(function: Callable) -> None:
    try:
        data = read_request()
        result = function(data)
        output = json.dumps(result, ensure_ascii=True, allow_nan=False, indent=2)
    except (ContractError, ValueError, KeyError, TypeError, OverflowError) as exc:
        print(json.dumps({"ok": False, "message": str(exc)}))
        raise SystemExit(1) from None
    print(output)
