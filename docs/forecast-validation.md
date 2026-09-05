# Scientific validation protocol

Schierami 0.4 ships a runnable baseline and an evaluation system. It does not ship
licensed historical player data, fitted weights, certified calibration or evidence
that it beats human managers. All committed examples and test histories are synthetic.

## Implemented versus deferred

| Implemented and testable | Not claimed in this release |
| --- | --- |
| Empirical minutes/start/vote/points distributions and exact-role shrinkage | Learned expected-minutes, xG/xA or opponent models |
| Explicit joint-block import and seeded/exact scenario generation | Learned match-event correlation or football-physics simulation |
| Complete legal-candidate comparisons, including supplied bench alternatives | Global nonlinear XI/bench/captain optimizer or full Mantra |
| Walk-forward forecast metrics and optional realized decision replay | Real-data prospective accuracy gains or fitted calibration |
| Provenance/cutoff/expiry checks and JSON hashes | Independent attestation of source truth or timestamps |

Runtime contracts are in [forecasting](../skills/schierami/references/forecasting.md).
They preserve the scoring coverage limits established in 0.3.1.

## First reproducible experiment

1. Freeze one real competition, season, vote provider, scoring version and decision
   horizon. Acquire a permitted, complete historical export including eligible
   nonappearances, with player/match IDs and availability/capture timestamps.
2. Freeze roster snapshots and rule versions at the actual decision cutoffs. Do not
   backfill later transfer knowledge, corrected ratings or retrospective news.
3. Predeclare at least a recent-player baseline and the shrinkage comparator, their
   window/lookback/strength, fold boundaries, primary metric and research budget.
   Hyperparameter selection needs earlier inner folds, not the held-out evaluation.
4. Execute `backtest_forecasts.py`, retain inputs and output hashes locally, and
   inspect coverage, excluded data, cold starts, calibration bins and loss by fold.
   Empty or infinite metrics cannot be omitted from model comparisons.
5. Evaluate actual XI/bench choices under a fixed legal candidate set and real rules.
   Compare realized scores across identical cutoffs, not each model's best hindsight
   lineup. Report candidate-set restrictions and sampling noise.
6. Collect genuine pre-kickoff forecast snapshots on later rounds. Only those runs
   support a prospective claim. Publish a model card with sample sizes, uncertainty,
   failures, forecast coverage, source rights and the exact version evaluated.

Do not treat low errors on synthetic inputs as football accuracy. There is no
universal pass threshold or promised uplift; define a practically meaningful
improvement before examining the held-out results. A no-gain result is publishable.

## Ablations and statistical cautions

Compare alpha zero against nonzero shrinkage, and predeclared history windows.
Compare supplied joint scenarios against an explicitly independent ablation only
when the data supports both. Keep candidate generation and evidence budget fixed.

The implemented bootstrap resamples paired entire folds and reports a CRPS
comparison. It does not model serial dependence between rounds; use suitable larger
blocks and sensitivity analyses in a separate experiment when that dependence is
material. It does not correct for trying many variants or selecting the winner.
Reliability bins with small counts are descriptive, not proof of calibration.

Keep self-score, league standings utility, qualification and win probability
separate. The current probabilistic decision bridge ranks expected own score only;
unsupported opponent effects are errors, not an invitation to drop a league rule.

## Engineering release checks

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py
python tools/forecast_demo.py --output dist/forecast-demo
```

Unit tests cover independent numerical oracles, future-information invariance,
strict contracts, coupled outcomes, exact/Monte Carlo agreement on small examples,
case coverage, finite/infinite metric handling and execution from an extracted
skill package without repository modules or third-party site packages.

Keep real user data out of the repository, skill ZIP and public CI artifacts.
CI's review artifacts contain committed source, release packages and synthetic
validation material only. No ongoing monitoring or persistent service is introduced.
