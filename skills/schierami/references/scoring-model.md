# Scenario scoring and deterministic tools

The bundled scripts are calculators, not forecast models and not replicas of any host platform. Use them only when the user's confirmed rules fit the declared contract. Never coerce an unsupported rule into a similar-looking field.

## `validate_lineup.py`

Input is JSON with `roster`, `lineup` and `rules`.

- `roster`: array of `{id, name?, roles:[...]}`.
- `lineup`: `{formation, starters:[{player_id, slot}], bench:[player_id...], captain_id?}`.
- `rules`: `{starter_count, bench_max?, formations, slot_eligibility, captain_required?}`.
- `formations` maps a formation name to the exact required slot names.
- `slot_eligibility` maps each slot to the fantasy roles that can occupy it.

The validator checks ownership, duplicate use, count, formation slots, eligibility, bench limit and captain placement. It does not know whether a supplied role/slot table is the official one, resolve conditional Mantra constraints, apply substitutions or infer a platform setting.

Exit code 0 means structurally valid under the supplied contract; 2 means invalid; 1 means malformed/unsupported input. Output is JSON.

## `score_scenario.py`

Score one explicit outcome after receiving player values; it does not estimate those values. Each starter/bench entry supplies `player_id`, `slot`, `roles`, `valid_vote`, `fantasy_points` and optional `base_vote`. `fantasy_points` must already include the user's player-level vote/event bonuses and maluses. Do not add them a second time.

Supported rules are intentionally narrow:

- `max_substitutions`.
- `substitution_mode: "ordered_slots"`: process absent starter slots in submitted order and use the first unused bench player with a valid vote whose role is eligible for that slot.
- `slot_eligibility` as above.
- `modifiers` of `type: "threshold_average"`, applied after replacements. A modifier contains `selectors`, each with explicit `slots` and `take_best`, plus descending or unsorted `{min, points}` thresholds and optional `target: "self"|"opponent"`.

For example, goalkeeper plus the best three of four defenders can be represented as two selectors: `{slots:["P"], take_best:1}` and `{slots:["D1","D2","D3","D4"], take_best:3}`. Selection and average use `base_vote`, not `fantasy_points`. If a selected effective player lacks `base_vote`, scoring fails rather than inventing it.

The scorer returns the effective lineup, substitutions, player total, self modifier total, opponent adjustment and total. `target:"opponent"` is reported separately and is not subtracted from one's own total because the caller may be scoring both sides.

Unknown rule keys and unsupported modifier types are errors, not silently ignored features. `ordered_slots` is a primitive, not Classic Dynamic/Hybrid and not Mantra Basic/Easy/Master. Captaincy, office reserves, Switch, module-changing substitutions, relative/opponent-input modifiers and arbitrary custom formulas must be resolved manually or by another verified engine.

## Nonlinear rules and expectation

A threshold function must be applied inside each scenario. In general `E[f(X)]` is not `f(E[X])`. When probabilities are defensible, score the relevant scenarios then probability-weight their outputs. When they are not, compare a few plausible scenarios qualitatively instead of inventing a distribution.

Keep player forecasting separate from rule calculation. A deterministic script proving that one supplied scenario scores 72.5 does not prove that scenario is likely.
