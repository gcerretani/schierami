# Workflow traceability

A full-lineup recommendation is complete only when every decision-relevant check was either completed or has a specific recorded blocker. A blocker is local: it prevents only dependent steps.

## Observable run trace

Keep a compact trace of facts and operations, not private reasoning. Record:

- scope: real competition/season, fantasy competition, team, matchday and deadline;
- inputs: roster/rule files or conversation facts actually used, with sheet/section/locator when available;
- rules: status and provenance for every material formation, substitution, modifier, captain and scoring rule;
- sporting evidence: source, as-of time, matchday relevance and whether the item is observed fact or inference;
- checks: roster extraction, matchday mapping, broad candidate screening, legality, bench/captain coverage and freshness;
- deterministic execution: script/contract, decision mode and returned optimality scope;
- blockers: unresolved facts, which decisions they block, and the condition that would flip or unlock the choice.

Do not claim a file was inspected, a source was researched or a script was executed unless the corresponding tool operation occurred.

## Completion gate

For a full lineup, do not finalize until all applicable items below are `done` or `blocked` with a reason:

1. roster ownership and identity;
2. fantasy-to-real matchday mapping;
3. formation and slot legality;
4. substitutions and bench constraints;
5. modifiers and captain rules;
6. current availability/minutes evidence for realistic candidates;
7. broad candidate/module screening;
8. deterministic calculation when its required inputs are defensible and its contract covers every material effect;
9. final freshness check for volatile facts near the deadline.

If an item is irrelevant, mark it `not_applicable`, not `done`.

## Decision modes

- `exact_additive_optimum`: additive projections and all material rules fit the optimizer.
- `scenario_candidate_optimum`: candidates and defensible weighted scenarios fit the scenario evaluator.
- `deterministic_validation_scoring`: only legality or explicit scenario arithmetic was computed.
- `qualitative_conditional`: the recommendation depends on evidence or rules that cannot be represented or quantified defensibly.

Always preserve the weakest material limitation in the user-facing claim.
