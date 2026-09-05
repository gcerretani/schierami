# AGENTS.md

This file is the short operating guide for coding agents working on Schierami.
Human contributor policy remains in [CONTRIBUTING.md](CONTRIBUTING.md); detailed
maintainer documentation remains under [docs](docs/README.md).

## Objective

Schierami exists to make the **best defensible fantasy-soccer lineup decision under
uncertainty** from the user's actual roster, league rules and available evidence.
The goal is better decisions, not maximal script usage, fake numerical precision or
optimizing a simplified model while silently dropping material real rules.

Keep the project **skill-only**. Do not introduce a hosted backend, account service,
persistent user profile or automatic lineup submission unless the project scope is
explicitly changed by the maintainer.

## Read first

For changes that affect behavior, read these before editing:

1. [skills/schierami/SKILL.md](skills/schierami/SKILL.md) — runtime control plane.
2. [skills/schierami/references/scoring-model.md](skills/schierami/references/scoring-model.md) — deterministic contracts and claim limits.
3. [skills/schierami/references/workflow-traceability.md](skills/schierami/references/workflow-traceability.md) — completion gates and observable traceability.
4. [evals/README.md](evals/README.md) — behavioral process evaluations.
5. [CONTRIBUTING.md](CONTRIBUTING.md) — repository conventions.

Load other rule or research references only when relevant to the change.

## Repository boundaries

- `skills/schierami/` is the installable runtime skill. It must remain self-contained.
- `skills/schierami/scripts/` contains deterministic runtime code; keep it standard-library-only and compatible with Python 3.10+.
- `skills/schierami/references/`, `schemas/`, `examples/` and `assets/` are runtime resources.
- `tests/`, `evals/`, `tools/`, `docs/` and root maintainer files are repository-only and are not packaged into the skill.
- `.codex-plugin/plugin.json` is the canonical version source.

Do not create runtime links from the installable skill to repository-only files.

## Non-negotiable invariants

- Never commit private rosters, conversations, credentials, session material or user exports. Tests and evals use synthetic data only.
- Repository prose, code, metadata and release notes are in English. User-facing advice follows the user's language.
- Do not invent probabilities, expected points, rules or source freshness merely to make an optimizer executable.
- Unsupported material rules must fail closed or narrow the claim; they must not be silently deleted.
- Every candidate scored as a lineup must first be legal under explicit lineup rules.
- A missing fact blocks only the decisions that depend on it. Continue independent checks.
- Use the strongest justified decision mode, but never upgrade a weaker result into a stronger optimality claim in prose.
- Keep forecasting separate from deterministic arithmetic and from realized-result evaluation.

## Change discipline

For a behavioral change, update the smallest appropriate combination of `SKILL.md`,
direct references and behavioral cases. For deterministic logic, add or update
unit/integration tests. For newly supported rules, update the executable contract,
its documentation and failure behavior together.

Prefer scripts for fragile deterministic operations and concise instructions for
judgment-heavy tasks. Avoid growing `SKILL.md` into a knowledge dump; directly link
one-level references instead.

Before opening or merging a change, run from the repository root:

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py
```

A passing unit test proves only the tested deterministic behavior. It does not prove
sporting prediction quality. Changes to lineup decision behavior should also be
represented in [evals](evals/README.md).

## Releases

Keep unreleased notes in [CHANGELOG.md](CHANGELOG.md). For a release, move them to a
dated version section and bump `.codex-plugin/plugin.json` in the same change. Pushes
to `main` run the release workflow, which tests, builds and publishes a missing
version without rewriting an existing published release.

Do not hand-edit generated archives or commit `dist/`. See
[docs/releases.md](docs/releases.md) for the full release process.

## Forecasting changes

Read the [forecasting contract](skills/schierami/references/forecasting.md) and
[validation guide](docs/forecast-validation.md) before changing forecast logic.
Keep observations, inference, joint-scenario sampling and realized evaluation
separate. Preserve timestamp exclusion, actual evidence-origin/support reporting,
seeded reproducibility and finite-model optimality limits. Add metamorphic tests
showing that future outcomes cannot change earlier predictions. Never turn
synthetic test gains or calibration diagnostics into a real-world accuracy claim.
