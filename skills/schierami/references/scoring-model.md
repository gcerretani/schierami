# Deterministic decision engine

The bundled scripts are local calculators and optimizers, not a hosted backend and not replicas of any fantasy platform. Unsupported rules must fail closed or remain outside the claimed optimum.

The method separates four layers: rules determine legality and scoring; forecasts/scenarios describe uncertainty; optimization chooses an action for an explicit objective; evaluation measures whether that process improves decisions over time. A correct optimizer fed invented projections is not a scientific forecast.

For the provenance of each executable formula, algorithm and numerical convention, read [method provenance](method-provenance.md). In particular, do not describe a standard optimization method, league-derived scoring rule or project engineering choice as a formula taken directly from the cited fantasy-football papers.

## Contract guarantees

The deterministic tools reject unknown supported-contract keys, malformed booleans/counts, duplicate identities where ambiguous, missing valid-vote scores and non-finite numeric values. Threshold arithmetic uses decimal comparison, so exact boundaries such as `6.1` are not lost to binary floating-point error.

Observed numeric inputs and deterministic arithmetic should be as exact as their sources. Forecasts are different: decimal outputs do not imply decimal predictive certainty. Keep measurement precision, rule precision and forecast uncertainty separate in both traces and prose.

## `run_lineup.py`

`run_lineup.py` is the preferred dispatcher. It selects the strongest supported deterministic mode from explicit supplied inputs and emits a run report. It never manufactures missing rules, observations, expected points or probabilities.

Version 0.5 adds an optional request envelope:

```json
{"request": {"kind": "full_lineup"}}
```

For `full_lineup`, the dispatcher enforces an observable completion preflight. The trace must contain the canonical checks documented in [workflow traceability](workflow-traceability.md). A full lineup without deterministic execution is complete only when an explicit blocker states that `deterministic_calculation` or `quantitative_comparison` itself is blocked. Missing a richer rule does not justify skipping an independent lower-scope calculation.

The completion report distinguishes `full_rule_quantitative`, `partial_quantitative`, `conditional_only` and `incomplete`. This scope is separate from the optimizer's own mathematical optimality field.

## `validate_lineup.py`

Input is exactly `roster`, `lineup` and `rules`. It checks ownership, duplicate use, exact counts, formation slots, role eligibility, bench limit, captain placement, locked starters and excluded players. It does not infer platform settings, official role tables or conditional Mantra logic.

Exit code 0 means valid under the supplied contract; 2 means structurally invalid; 1 means malformed or unsupported input.

## `optimize_lineup.py`

Performs exact branch-and-bound search across all legal XIs representable by the supplied formations.

Input:

- `roster`: `{id, name?, roles:[...]}` rows;
- `projections`: exactly one `{player_id, expected_points}` row per roster player;
- `rules`: `starter_count`, `formations`, `slot_eligibility`, optional `captain_required`, `captain_multiplier`, `locked_starters`, `excluded_players`.

Supported objective: `additive_expected_fantasy_points`.

`optimality: proven_within_supported_model` means no other legal XI in the declared formations scores higher under those supplied additive projections and constraints. It does not include bench order, substitution outcomes, nonlinear modifiers, correlated scenarios, opponent score, win probability or standings points.

The additive objective and branch-and-bound search are standard optimization methods applied to the supplied fantasy constraints. The fantasy-team-selection literature motivates whole-lineup constrained optimization, but Schierami's exact contract and implementation are project-specific and must not be described as copied equations from those papers.

## `score_scenario.py`

Scores one explicit realized or hypothetical outcome. Each starter supplies `player_id`, `slot`, `roles`, exact boolean `valid_vote`, and `fantasy_points` when valid; `base_vote` is required when selected by a modifier. Bench rows omit `slot`.

Supported rules are deliberately narrow: non-negative `max_substitutions`, `substitution_mode: "ordered_slots"`, explicit `slot_eligibility`, and `threshold_average` modifiers with selectors, decimal thresholds and target `self` or `opponent`.

`ordered_slots` is a primitive, not Classic Dynamic/Hybrid or a complete Mantra Basic/Easy/Master engine.

## `evaluate_lineups.py`

Compares complete supplied candidate lineups over a supplied weighted scenario ensemble.

Version 2 requires `roster`, `candidates`, `scenarios`, scoring `rules` and separate
`lineup_rules`. Every candidate supplies `id`, `formation`, `starters` and `bench`.
`lineup_rules` is the shared validator contract with explicit `starter_count`,
`bench_max`, `formations`, `slot_eligibility` and `captain_required`; optional
`locked_starters` and `excluded_players` are enforced. The evaluator rejects every
illegal candidate before scoring. Scoring and legality eligibility maps must agree.
Captain scoring is not supported here: a required or supplied captain fails closed.
Existing v1 inputs must add the actual formation and legality settings, not defaults. Every candidate is scored inside every scenario after substitutions and nonlinear modifiers; weights are then normalized and used to compute expected score and dispersion.

`optimality: best_among_supplied_candidates_only` proves only the ranking of that candidate set under the supplied scenarios. Generate enough materially different candidates when nonlinear rules could make unusual formations or bench orders competitive.

## Nonlinear expectation

Apply threshold functions inside each scenario. In general `E[f(X)] != f(E[X])`. If probabilities are not defensible, compare named scenarios and report flip conditions instead of inventing a distribution.

For head-to-head leagues, the preferred decision objective is expected standings utility when defensible opponent scenarios and the goal-conversion rules are available. If they are not, optimize own expected fantasy score only as an explicit lower-scope fallback.

These nonlinear and expected-utility calculations are standard mathematical consequences of the scoring/objective once the league rules and scenario distribution are supplied; they are not empirical formulas learned from the cited fantasy papers.

## Decision modes

- **exact additive optimum**: `optimize_lineup.py` ran and all effects represented by the additive contract were optimized exactly;
- **best among supplied scenarios/candidates**: `evaluate_lineups.py` or `run_forecast.py` ran over explicit lineups/scenarios;
- **deterministic score/validation**: calculators checked arithmetic or legality but did not optimize the forecast;
- **qualitative/conditional**: quantitative inputs or executable rule coverage were insufficient for a ranking contract.

Never upgrade a weaker mode into a stronger claim in prose. In particular, an exact additive optimum can still be only `partial_quantitative` under the real league rules when a material modifier, substitution rule or opponent-aware objective remains unresolved.

## Forecast bridge (0.4+)

`build_forecasts.py`, `run_forecast.py` and `backtest_forecasts.py` add a separately
versioned probabilistic layer; read [forecasting](forecasting.md) before use.
They do not expand the existing league-scoring contract. `run_lineup.py` dispatches
forecast-bundle payloads through this layer and preserves sample-only optimality
when Monte Carlo is used. Existing v2 evaluator inputs remain supported.
