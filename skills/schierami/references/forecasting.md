# Forecasts, joint scenarios and scientific evaluation

## Contents

- [Scope and decision gate](#scope-and-decision-gate)
- [Historical baseline](#historical-baseline)
- [Forecast bundle contract](#forecast-bundle-contract)
- [Scenario decision contract](#scenario-decision-contract)
- [Walk-forward benchmark](#walk-forward-benchmark)
- [Evidence and operational limits](#evidence-and-operational-limits)
- [Methodological sources](#methodological-sources)

## Scope and decision gate

Version 0.4 adds a **baseline and measurement system**, not a proven winning model.
It runs locally in the host's Python 3.10+ environment using only the standard
library. No API key, package installation, network access or Schierami backend is
needed by these scripts. The host must actually execute them before claiming a run.

Use numerical forecasts only when the data, population and assumptions fit the
current decision. Historic minutes are not a substitute for current injury news.
A recent transfer, changed role or confirmed absence can invalidate this baseline;
keep that blocker explicit and compare supported conditional scenarios instead.
Never turn article adjectives or model intuition into percentages to satisfy a schema.

The code separates prediction, scoring, candidate selection and outcome evaluation.
An imported forecast is not automatically calibrated. A schema/hash validates
structure/identity, not whether evidence or probabilities are true.

## Historical baseline

Run `scripts/build_forecasts.py` with JSON on standard input. The executable
[history example](../examples/forecast-history.json) is wholly synthetic.

Required top-level fields: `scope`, `as_of`, `deadline`, `roster`, `evidence`,
`history`, `model`. Unknown keys at every supported level fail closed.

`scope` requires `competition`, `season`, `scoring_id`, `vote_provider`. These bind
one homogeneous dataset: do not mix leagues, seasons, editorial providers or
scoring revisions under one label. Multi-fixture fantasy rounds require a separate
aggregation model; a row here is one player in one sporting match.

`roster` rows contain string `id`, nonempty unique `roles`, optional `name`.
The roster also defines the limited peer population in this baseline; it is not
assumed to represent the whole league. Obtain a pre-deadline roster snapshot for
historical decision replay, rather than using today's surviving players.

Each `history` row requires `player_id`, `match_id`, `kickoff`, `available_at`,
`source_id`, `started`, `minutes`, `valid_vote`, `base_vote`, `fantasy_points`.
Use timezone-aware ISO timestamps, real JSON booleans and finite JSON numbers.
Minutes must be unrounded, between 0 and 180 for this per-match contract; a starter
has positive minutes. An explicit office vote may have zero minutes. A no-vote
outcome has null `base_vote` and zero player points; resolving a league's no-vote
exceptions is upstream. When valid, `base_vote` may still be null for event-only
scoring. Player points must already include that scoring system's bonus/malus:
do not add goals, assists or cards a second time.

Record **all eligible player-match observations, including nonappearances**.
An appearances-only export cannot estimate appearance/vote probability. Never
invent zero rows to fill a sparse dataset without establishing match eligibility.
Duplicate player-match observations fail, even when copied by a second provider.

`model` requires an identifier `name`, positive integer `window`, nonnegative
`prior_strength` and positive integer `lookback_days`. No fit or automatic tuning
occurs. The baseline selects at most `window` recent usable observations per player
inside the lookback. It pools only other roster players with the **exact same role
set**, within the declared scope.

For n own observations and k available peer observations, each own outcome has
weight 1 and each peer outcome has weight alpha/k, where alpha is the supplied
prior strength. Thus, for n > 0 and peers available:

`F_player = (n * F_recent + alpha * F_peers) / (n + alpha)`.

Alpha is an engineering hyperparameter, **not a universal literature-derived
constant**. Predeclare it or tune only on earlier inner training folds. Alpha zero
is the recent-player baseline. With no own history, the peer empirical distribution
is an explicitly marked cold-start fallback; with no peers, use own history and
report unavailable shrinkage. With neither, fail rather than invent a prior.
Peer outcomes preserve their internal minutes/vote/point relationship but this is
an exchangeability assumption, not a player-specific structural football model.

Only outcomes available and evidence captured by `as_of` enter the estimate.
Late rows are counted in `excluded_future_rows`; old rows are counted separately.
Return the actual used player-match IDs, model parameters, evidence origins, player
support counts, an input SHA-256, a `forecast_bundle`, marginal `player_forecasts`
and additive `projections`. The projections do not include bench insurance or
nonlinear modifiers; do not route them to the additive optimizer when those matter.

## Forecast bundle contract

`forecast_bundle.v1` is checked by `forecast_core.validate_bundle`; the companion
[JSON Schema](../schemas/forecast-bundle.schema.json) documents its shape. Runtime
validation additionally enforces temporal, identity and cross-field invariants.

Required fields: `contract`, `scope`, `as_of`, `deadline`, `roster`, `evidence`,
`model`, `blocks`, `independent_blocks`, `input_sha256`.

`model` contains `name`, `version`, `status`, nonempty `assumptions`. V1 accepts
`baseline_unvalidated` or `supplied_unvalidated`, never a self-certified calibration
claim. Keep external validation reports separately; a label cannot establish them.

Each block has `id`, `player_ids`, `evidence_ids`, `states`. Blocks partition the
whole roster, without overlapping players. Every positive-weight state contains
one full outcome for each player in that block, using the six outcome fields above.
Weights are relative, not necessarily normalized probabilities.

Keep materially dependent players in the **same joint block**. A whole state is
selected together: competing starters or correlated player scores supplied jointly
cannot be broken by independent draws. Multiple blocks require an explicit
`independent_blocks: true` assumption. The historical baseline creates one block
per player: it does **not** learn match-level correlations or enforce shared goals,
assists, clean sheets or lineup constraints between real clubs. An imported joint
block preserves only the coherence actually encoded by its author; the validator
cannot infer physical football consistency from aggregate points.

## Scenario decision contract

Run `scripts/run_forecast.py` or supply its payload to `scripts/run_lineup.py`.
The payload requires `forecast_bundle`, `sampling`, `candidates`, `rules` and
`lineup_rules`. Legality and scoring reuse the existing evaluator contracts.

Two explicit sampling modes:

- `{"method":"exact","max_scenarios":10000}` enumerates the finite Cartesian
  state space, failing if it exceeds the declared budget (maximum 10,000).
- `{"method":"monte_carlo","samples":2000,"seed":42}` draws whole joint-block
  states, compresses identical draws by frequency, and uses the **same scenarios
  for every candidate**. Samples must be 2 to 10,000. Record Python/runtime version
  alongside the seed for cross-environment reproducibility.

No silent truncation or switch from exact to approximate search occurs. At most
100,000 candidate-scenario evaluations are accepted. The returned finite-model
ranking is exact only for the supplied candidate set; Monte Carlo explicitly
returns `best_among_supplied_candidates_on_sample_only`.

Preserve returned forecast hashes, cutoff, assumptions, sampling method and
optimality. Compare XI **and bench alternatives** by supplying different complete
legal candidates. This version does not globally generate/optimize all benches,
implement full Mantra, score captaincy in scenarios, or optimize opponent-aware
utility. Opponent-target modifiers fail rather than being ignored in own-score
ranking. Other unsupported scoring rules still fail in the existing engine.

Differences from the selected candidate include minimum/maximum scenario difference
and, for Monte Carlo, paired standard error. That error measures **simulation noise
under the supplied model**, not forecast accuracy. Selected-best comparisons are
exploratory, not post-selection confidence intervals. Check seed/sample sensitivity
when numerical differences are small; more draws do not fix a wrong forecast.

## Walk-forward benchmark

Run `scripts/backtest_forecasts.py`. Inputs are `scope`, `roster`, `evidence`,
`history`, at least two predeclared `models`, ordered `folds`, and
`bootstrap: {seed, resamples}` (0 disables; maximum 10,000).

A fold requires `id`, timezone-aware `as_of`, and `test_match_ids`. The forecast is
rebuilt at each cutoff; training uses only outcomes and captured evidence available
then. Every requested test match must have targets, kickoffs must follow the cutoff,
and a player-match target cannot be evaluated twice. All supplied targets are scored;
missing or unsupported training data fails explicitly rather than silently dropping
hard-to-predict players. This cannot detect targets omitted from the source export:
check export completeness independently.

Optional `decision` contains `candidates`, `rules`, `lineup_rules`, `sampling` and
requires exactly one actual outcome per forecast-roster player. Select the candidate
using forecasts first, then separately score actual results. Record realized score
and regret against the **hindsight best supplied candidate**, not an unknowable
pre-deadline oracle. Do not use that regret alone to judge decision quality.

Metrics: Brier and logarithmic loss for starts, appearances and valid votes; MAE,
RMSE and finite-distribution CRPS for minutes and fantasy points; conditional
base-vote errors with target/scored/missing counts; ten reliability bins with counts.
Impossible events produce `log_loss: null` plus `infinite_log_losses > 0`, not a
finite disguised score. A separately labelled clipped log loss uses epsilon 1e-15.
Null never means a perfect or zero loss. Empty conditional vote samples stay null.

Return per-fold results, training provenance and aggregate metrics. The first model
is the predeclared reference. Paired fold bootstrap compares equal-fold mean
fantasy-point CRPS; negative difference favors the candidate model. It resamples
whole folds, not correlated players independently. It does not handle serial
correlation across folds or multiple-comparison selection; few-fold intervals are
unstable. It is a diagnostic, not automatic evidence of superiority.

Keep training, calibration, model selection and final test periods separate. Add
ablation runs (alpha zero, shorter/longer windows) as **predeclared** comparisons;
never tune from the final benchmark. Do not call this a prospective test unless
forecasts were genuinely saved before kickoff. Supplied historical timestamps are
checked for consistency, not independently attested. Real datasets and published
numeric skill claims need a separate evidence-backed experiment report.

## Evidence and operational limits

Each evidence item requires `id`, `origin_id`, `locator`, `published_at`,
`retrieved_at`, `status`, `valid_until` (explicit null for immutable historical
facts). `confirmed` and `user_stated` can enter the baseline, but their truth is not
certified by software. `hypothesis` and `conflicted` cannot support numerical input.
Set a real expiry for volatile information; no universal freshness lifetime is
assumed. Referenced evidence must have been retrieved by the forecast cutoff and
remain valid. A copied story retains its original `origin_id`.

Follow [sources](sources.md) and [research protocol](research-protocol.md) to prefer
primary announcements for factual availability, the actual league provider for
votes/rules, and source-specific data definitions for statistics. A source ranking
is not a numeric model weight. Resolve conflicts rather than majority-voting copied
reports. The host acquires authorized files/web evidence; Python processes supplied
JSON only. Neither script bypasses logins, scrapes providers or grants data rights.
Confirm export/API permissions before use; keep raw private datasets and real run
logs outside the repository and distributable skill. No persistence is promised.

## Methodological sources

These sources support evaluation principles, not the predictive performance of
this implementation. Shrinkage strength, caps, bins and finite-block representation
are documented engineering choices, not validated universal football constants.

- Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and
  Estimation*, DOI: https://doi.org/10.1198/016214506000001437 . Proper scoring rules
  motivate honest probabilistic forecasts; CRPS evaluates the whole distribution.
- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, rolling-origin
  evaluation: https://otexts.com/fpp3/tscv.html . Train on information preceding
  each test origin rather than random future-contaminated splits.
- Groos (2025), *OpenFPL* [preprint]: https://arxiv.org/abs/2508.09992 . A forecasting
  research reference, not bundled model weights. Its FPL findings are not direct
  evidence for Italian editorial votes or this baseline.

Consult [scientific evidence](scientific-evidence.md) for the broader evidence map.
