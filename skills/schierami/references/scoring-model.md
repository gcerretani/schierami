# Deterministic decision engine

The bundled scripts are local calculators and optimizers, not a hosted backend and not replicas of any fantasy platform. Unsupported rules must fail closed or remain outside the claimed optimum.

The method separates four layers: rules determine legality and scoring; forecasts/scenarios describe uncertainty; optimization chooses an action for an explicit objective; evaluation measures whether that process improves decisions over time. A correct optimizer fed invented projections is not a scientific forecast.

## Contract guarantees

The deterministic tools reject unknown supported-contract keys, malformed booleans/counts, duplicate identities where ambiguous, missing valid-vote scores and non-finite numeric values. Threshold arithmetic uses decimal comparison, so exact boundaries such as `6.1` are not lost to binary floating-point error.

## `validate_lineup.py`

Input is exactly `roster`, `lineup` and `rules`. It checks ownership, duplicate use, exact counts, formation slots, role eligibility, bench limit and captain placement. It does not infer platform settings, official role tables or conditional Mantra logic.

Exit code 0 means valid under the supplied contract; 2 means structurally invalid; 1 means malformed or unsupported input.

## `optimize_lineup.py`

Performs exact branch-and-bound search across all legal XIs representable by the supplied formations.

Input:

- `roster`: `{id, name?, roles:[...]}` rows;
- `projections`: exactly one `{player_id, expected_points}` row per roster player;
- `rules`: `starter_count`, `formations`, `slot_eligibility`, optional `captain_required`, `captain_multiplier`, `locked_starters`, `excluded_players`.

Supported objective: `additive_expected_fantasy_points`.

`optimality: proven_within_supported_model` means no other legal XI in the declared formations scores higher under those supplied additive projections and constraints. It does not include bench order, substitution outcomes, nonlinear modifiers, correlated scenarios, opponent score, win probability or standings points.

## `score_scenario.py`

Scores one explicit realized or hypothetical outcome. Each starter supplies `player_id`, `slot`, `roles`, exact boolean `valid_vote`, and `fantasy_points` when valid; `base_vote` is required when selected by a modifier. Bench rows omit `slot`.

Supported rules are deliberately narrow: non-negative `max_substitutions`, `substitution_mode: "ordered_slots"`, explicit `slot_eligibility`, and `threshold_average` modifiers with selectors, decimal thresholds and target `self` or `opponent`.

`ordered_slots` is a primitive, not Classic Dynamic/Hybrid or a complete Mantra Basic/Easy/Master engine.

## `evaluate_lineups.py`

Compares complete supplied candidate lineups over a supplied weighted scenario ensemble. Every candidate is scored inside every scenario after substitutions and nonlinear modifiers; weights are then normalized and used to compute expected score and dispersion.

`optimality: best_among_supplied_candidates_only` proves only the ranking of that candidate set under the supplied scenarios. Generate enough materially different candidates when nonlinear rules could make unusual formations or bench orders competitive.

## Nonlinear expectation

Apply threshold functions inside each scenario. In general `E[f(X)] != f(E[X])`. If probabilities are not defensible, compare named scenarios and report flip conditions instead of inventing a distribution.

## Decision modes

- **exact additive optimum**: `optimize_lineup.py` ran and all material effects fit the additive contract;
- **best among supplied scenarios/candidates**: `evaluate_lineups.py` ran over explicit lineups and scenarios;
- **deterministic score/validation**: calculators checked arithmetic or legality but did not optimize the forecast;
- **qualitative/conditional**: quantitative inputs or executable rule coverage were insufficient.

Never upgrade a weaker mode into a stronger claim in prose.
