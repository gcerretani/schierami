# Behavioral evaluations

These evaluations target **process reliability**, not lucky match outcomes or claimed predictive superiority. They use synthetic data only and keep Schierami skill-only: no production backend is introduced.

The core question is whether a full-lineup request follows the scientific decision process consistently: use accessible inputs, resolve only material unknowns, keep blockers local, choose the strongest justified decision mode, and never claim computations or freshness that did not occur.

## Evaluation layers

1. **Unit/integration tests** in `tests/` verify deterministic contracts and calculators.
2. **Behavioral cases** in `evals/cases.json` describe synthetic conversations and machine-checkable process expectations.
3. **Run scorer** in `evals/score_behavior.py` scores a model/agent run exported as observable JSON. It evaluates actions and claims, never hidden chain-of-thought.
4. **Real-environment trials** should run the same cases in the intended ChatGPT/Codex environment with the same tools and research budget. Keep those records private when they include user data.

## Required run-result shape

A runner should emit a JSON array whose objects contain:

```json
{
  "case_id": "accessible_roster_missing_modifier",
  "decision_mode": "qualitative_conditional",
  "checks": {
    "roster_read": "done",
    "modifier_rule": "blocked",
    "candidate_screening": "done"
  },
  "asked_for": ["modifier_formula"],
  "claims": ["module comparison remains conditional"],
  "scripts_ran": []
}
```

`score_behavior.py` compares those observable fields with the expectations in `cases.json` and exits non-zero on any failed case.

## Principles

- A missing modifier formula may block module ranking, but must not block reading an accessible roster or screening candidates.
- If all material rules and defensible projections/scenarios are supplied, an unjustified qualitative fallback is a failure.
- Unsupported material rules must narrow the claim; silently deleting them to make an optimizer run is a failure.
- Do not ask the user for a roster or rule already available in an accessible source.
- Do not claim a file read, web check, script run, validation or optimum unless the corresponding operation occurred.
- Judge evidence only as available before the lineup deadline. Separate process quality from realized fantasy points.

For version comparisons, hold model, inputs, available tools and research budget constant. Repeat important cases because one successful sample does not establish consistency. Track rule errors, extraction errors, unnecessary questions, unsupported claims, mode selection, tool usage and latency separately.

## Forecast evaluation is a separate layer

`backtest_forecasts.py` evaluates predeclared probabilistic baselines with chronological
cutoffs and optional realized candidate scores. Follow the
[validation protocol](../docs/forecast-validation.md). Behavioral cases now also
check future-data exclusion, source conflicts and sample-only optimality claims.
The unit tests exercise the contracts with synthetic data; real host-agent trials
and real-data prospective accuracy experiments remain separate, unreported work.
