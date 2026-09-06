# Method provenance

This reference explains where Schierami's executable formulas, algorithms and decision rules come from. It prevents a common category error: a method can be consistent with scientific literature without being a formula copied from a cited fantasy-football paper.

## Provenance labels

Use exactly these labels when explaining an implemented method:

- **literature-derived** — the implemented evaluation principle or mathematical tool is directly tied to cited methodological literature. This does not mean Schierami copied source code, that the paper validates this implementation, or that the method guarantees predictive superiority.
- **standard-method** — a general mathematical, statistical, optimization or numerical technique. Relevant papers may motivate its use, but the technique is not specific to the cited fantasy-football literature.
- **league-derived** — a formula, constraint or objective follows from the user's actual fantasy rules once those rules are known. Scientific papers are not needed to justify the arithmetic.
- **engineering-choice** — a project-specific representation, hyperparameter, cap, fallback or guardrail. It must never be presented as a literature-established football constant.

A method may have a primary label plus a supporting note. When in doubt, prefer the weaker attribution and state what is project-specific.

## Executable-method map

| Method or formula | Primary provenance | What may be claimed | What must not be claimed |
| --- | --- | --- | --- |
| Legal lineup constraints: formation, role eligibility, starter count, bench limit, locks, exclusions | **league-derived** | They encode the supplied competition rules and candidate contract. | That a paper determines the user's league rules. |
| Additive XI objective `max sum(E[FP_i])` when the contest objective is own expected fantasy score | **standard-method** with **league-derived** objective | It is a standard constrained optimization of the declared additive objective and is consistent with fantasy-team-selection literature. | That the exact Schierami equation or branch-and-bound implementation was copied from Bonomo, Maniezzo or Venter. |
| Branch-and-bound search in `optimize_lineup.py` | **standard-method** | It proves the optimum within the explicitly supported additive model and supplied constraints. | That branch-and-bound makes the sporting forecast scientifically correct. |
| Captain multiplier, defensive modifier, home bonus, goal bands and other scoring tables | **league-derived** | Their deterministic effect follows from the exact supplied rules. | That a generic paper supplies the correct league-specific values. |
| Decimal comparison at exact thresholds | **standard-method** | It is a numerical-correctness choice that avoids binary floating-point boundary errors. | That decimal arithmetic is a football forecasting result. |
| Scenario scoring after substitutions, then nonlinear modifiers | **league-derived** plus **standard-method** | It applies the real scoring order inside explicit scenarios. | That evaluating one scenario establishes a calibrated probability model. |
| `E[f(X)] != f(E[X])` for nonlinear goal/modifier functions | **standard-method** | Nonlinear scoring must generally be applied inside scenarios before averaging. | That this identity is a special empirical finding from a fantasy paper. |
| Weighted expected score across supplied scenarios | **standard-method** | It computes expectation under the supplied scenario weights. | That the supplied weights are automatically true probabilities. |
| Exact finite-state enumeration | **standard-method** | It is exact for the finite supplied state space when enumeration completes. | That it is exact for unmodelled real-world uncertainty. |
| Seeded Monte Carlo sampling | **standard-method** | It approximates the supplied model and exposes sampling noise. | That more samples repair a misspecified forecast or turn sample frequency into real-world certainty. |
| Joint state blocks and explicit independence between separate blocks | **engineering-choice** using a **standard-method** probabilistic representation | They preserve dependencies that are explicitly supplied and make independence assumptions observable. | That the current baseline learns real football correlations. |
| Historical empirical distribution from recent player observations | **engineering-choice** | It is a transparent baseline built from observed outcomes. | That the cited literature proves this exact baseline is optimal for Italian fantacalcio. |
| Shrinkage `F_player = (n * F_recent + alpha * F_peers) / (n + alpha)` | **engineering-choice** | It is a documented empirical shrinkage baseline whose parameters must be predeclared or validated out of sample. | That `alpha`, the exact peer pool or this formula is a universal coefficient established by the cited fantasy papers. |
| Exact-role-set peer pooling | **engineering-choice** | It is the current baseline's explicit exchangeability assumption. | That players with the same fantasy role are scientifically interchangeable. |
| Historical window, lookback days and prior strength | **engineering-choice** | They are model parameters that may be predeclared or tuned only on earlier training data. | That any default or chosen value is a literature constant. |
| Brier score and logarithmic loss for probabilistic events | **literature-derived** | They are proper scoring-rule tools for evaluating probabilistic forecasts; see Gneiting & Raftery (2007). | That a good score on synthetic or retrospective data proves sporting superiority. |
| CRPS for finite fantasy-point distributions | **literature-derived** | It evaluates the quality of a full predictive distribution; see Gneiting & Raftery (2007). | That CRPS validates the upstream data-generating assumptions. |
| MAE and RMSE | **standard-method** | They are standard point-forecast error summaries. | That either is uniquely preferred by the fantasy-football literature. |
| Chronological rolling-origin / walk-forward evaluation | **literature-derived** | Training must precede each test origin; see Hyndman & Athanasopoulos. | That replaying old data is automatically a prospective experiment. |
| Paired fold bootstrap | **standard-method** | It is a diagnostic uncertainty summary over the declared folds. | That it handles every serial dependence or multiple-comparison issue. |
| Ten reliability bins | **engineering-choice** | They are a transparent visualization/diagnostic convention. | That ten bins are theoretically optimal. |
| Clipped log-loss epsilon `1e-15` | **engineering-choice** | It is a separately labelled numerical diagnostic. | That clipping changes an impossible event into a valid probabilistic forecast. |
| Scenario/sample/evaluation caps | **engineering-choice** | They are runtime and safety guardrails that prevent silent method changes or unbounded work. | That the caps have scientific meaning for football. |
| Evidence statuses, cutoffs, source IDs and hashes | **engineering-choice** informed by reproducibility principles | They make provenance, temporal leakage and conflicts observable. | That a valid schema or hash certifies the truth of a source. |
| Head-to-head objective `E[standings points]` when win/draw/loss rules and opponent scenarios are available | **league-derived** plus **standard-method** expected utility | It matches the competition objective better than own-score maximization when the required opponent model is defensible. | That opponent-aware utility is justified when opponent scenarios are invented or unsupported. |

## Scientific evidence versus implementation provenance

Use [scientific evidence](scientific-evidence.md) to answer **which decision principles are supported by fantasy-football or football research**. Use this file to answer **where an executable formula or algorithm comes from**.

Examples:

- Research supports treating expected minutes and availability as first-order inputs. It does **not** provide Schierami with a universal coefficient for expected minutes.
- Research supports constrained whole-team optimization. Schierami's exact additive contract and branch-and-bound implementation are still project implementations built with standard optimization methods.
- Proper scoring-rule literature directly supports Brier/log-loss/CRPS as evaluation tools. It does not validate Schierami's football forecast model.
- The user's modifier and goal-band formulas are league-derived. No paper can substitute for the actual league configuration.

## Attribution rule for assistants

When asked whether a formula "comes from the papers", answer at the narrowest correct level:

1. Name the implemented method.
2. Give its provenance label.
3. Cite the relevant repository scientific source only when the label is `literature-derived` or when a paper merely motivates the broader decision principle.
4. State any project-specific parameter or assumption separately.
5. Never promote `standard-method`, `league-derived` or `engineering-choice` into `literature-derived` for rhetorical convenience.

The scientific standard is traceable attribution, not maximal attribution to papers.
