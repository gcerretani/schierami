# Workflow traceability

A full-lineup recommendation is complete only when every decision-relevant check was either completed or has a specific recorded blocker, and the strongest defensible quantitative layer was attempted. A blocker is local: it prevents only dependent steps.

## Observable run trace

Keep a compact trace of facts and operations, not private reasoning. Record:

- scope: real competition/season, fantasy competition, team, matchday and deadline;
- inputs: roster/rule/history files or conversation facts actually used, with sheet/section/locator when available;
- data quality: source/provenance for decisive numeric observations, exactness, conflicts and whether no-votes/non-appearances are represented;
- rules: status and provenance for every material formation, substitution, modifier, captain, scoring and goal-conversion rule;
- sporting evidence: source, as-of time, matchday relevance and whether the item is observed fact or inference;
- checks: roster extraction, matchday mapping, broad candidate screening, legality, bench/captain coverage, data quality and freshness;
- deterministic execution: script/contract, decision mode, returned optimality scope and completion status;
- blockers: unresolved facts, which decisions they block, and the condition that would flip or unlock the choice.

Do not claim a file was inspected, a source was researched or a script was executed unless the corresponding tool operation occurred.

## Full-lineup completion gate

Call `run_lineup.py` with `request.kind: "full_lineup"`. The following check names must be present in the trace; use `not_applicable` only when the rule/effect genuinely does not exist:

1. `roster_read`;
2. `matchday_mapping`;
3. `formation_rules`;
4. `substitution_rules`;
5. `modifier_rules`;
6. `captain_rules`;
7. `data_quality`;
8. `availability_evidence`;
9. `candidate_screening`;
10. `deterministic_calculation`.

The answer is complete only when `run_report.completion.status == "complete"`.

`deterministic_calculation` has special semantics for a full lineup:

- mark `done` only when a deterministic script actually ran;
- mark `blocked` only when no defensible quantitative comparison can be executed, and add a blocker whose `blocks` includes `deterministic_calculation` or `quantitative_comparison`;
- never mark it `not_applicable` for a full-lineup request.

A perfect model is not required. If a material rule blocks the full optimum but a lower-scope calculation remains valid, run that calculation and keep the blocker. For example, an unknown defense-modifier table may block the final module ranking while still allowing legality checks or an additive baseline. The completion gate then reports a partial quantitative claim rather than pretending the real-rule optimum was solved.

## Data-quality gate

For decisive numeric inputs, prefer source-backed observations over reconstructed approximations. Record enough provenance to audit the value. Preserve conflicts instead of averaging incompatible sources. Keep deterministic arithmetic exact across thresholds, but keep forecast uncertainty distinct from decimal output precision.

When historical fantasy observations are used, identify whether the sample includes no-vote/non-appearance outcomes. An appearances-only average cannot be treated as a per-team-match expectation without an explicit availability model.

## Decision modes and claim scopes

Decision modes describe which engine ran:

- `exact_additive_optimum`: additive projections and all effects represented by that contract fit the optimizer;
- `scenario_candidate_optimum`: candidates and defensible weighted scenarios fit the scenario evaluator/forecast runner;
- `deterministic_validation_scoring`: only legality or explicit scenario arithmetic was computed;
- `qualitative_conditional`: no deterministic ranking contract matched.

Completion claim scopes describe what the full-lineup trace supports:

- `full_rule_quantitative`: a deterministic script ran and no recorded blocker narrows the claim;
- `partial_quantitative`: a deterministic script ran, but one or more recorded blockers limit the real-rule conclusion;
- `conditional_only`: no deterministic script could defensibly run and an explicit quantitative blocker explains why;
- `incomplete`: required checks are missing or the trace claims/fails to claim execution inconsistently.

Always preserve the weakest material limitation in the user-facing claim. A `partial_quantitative` result must never be described as the real-rule global optimum.

## Forecast trace

For forecast-bundle decisions, retain forecast cutoff, input/bundle SHA-256,
model name/version/status, evidence origins, history support and exclusions,
independence assumptions, sampling method/budget/seed, candidate-set scope and
returned optimality. Record actual execution separately from user-supplied checks.
Sampling error does not measure model uncertainty. Save prospective forecasts
before kickoff through an authorized file tool; do not claim persistence or
prospective validation from a reconstructed replay. See [forecasting](forecasting.md).
