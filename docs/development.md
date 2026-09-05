# Development

## Layout

```text
.codex-plugin/plugin.json       Plugin manifest and canonical version
.github/workflows/             CI and release automation
AGENTS.md                      Coding-agent operating guide
CHANGELOG.md                   Human-maintained version history
CONTRIBUTING.md                Contributor conventions
README.md                      Stable project overview
docs/                          User and maintainer documentation
evals/                         Synthetic behavioral cases and offline scorer
tools/                         Repository checks and release builder
tests/                         Automated unit, integration and packaging tests
skills/schierami/
  SKILL.md                     Skill entrypoint and workflow control plane
  agents/openai.yaml           Skill display metadata
  assets/                      Existing project icon
  examples/                    Synthetic executable inputs
  references/                  Rules, research, evidence and traceability guidance
  schemas/                     League profile and run-report representations
  scripts/                     Runtime validators, scorers, optimizers and dispatcher
```

Only files under the skill are installed with it. Keep the skill self-contained:
its relative links must not depend on repository docs, tests, evals or maintainer
tools.

## Local checks

Use Python 3.10 or newer. Project checks and deterministic runtime scripts use only
the standard library; no runtime package installation, API key or football data
service is required. Run from the repository root:

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py
```

Tests exercise deterministic contracts, integration invariants, behavioral scorer
fixtures, example inputs and release packaging. Repository checks validate local
file links, required files and version/changelog consistency. They do not validate
every external URL, forecast sporting performance, or replace the host's skill scan
and submission review.

Executable examples:

```sh
python skills/schierami/scripts/validate_lineup.py < skills/schierami/examples/lineup.json
python skills/schierami/scripts/score_scenario.py < skills/schierami/examples/scenario.json
```

The lineup example is a synthetic two-player format, not a real competition preset.
The scenario is a synthetic partial defensive unit, not a complete XI. Its expected
result is one substitution, 30 player points, a +1 modifier and 31 total points.
Read the [contract](../skills/schierami/references/scoring-model.md) before using
runtime scripts with real rules.

`skills/schierami/scripts/run_lineup.py` is the preferred deterministic entry point
for full-lineup calculations when a payload exactly matches a supported contract.
It dispatches to validation, additive optimization, scenario scoring or whole-lineup
scenario evaluation and returns an observable run report. It does not invent missing
forecasts, probabilities, scenarios or rules.

## Change discipline

Keep English prose consistent and use relative Markdown links for local documents.
Preserve the distinction between scientific evidence, rule deductions, qualitative
forecasts and deterministic calculations. Do not silently expand the deterministic
engine's claimed coverage when adding conversational guidance.

Behavioral process evaluations live in [evals](../evals/README.md) and are separate
from deterministic unit tests. Add a synthetic behavioral case when a change affects
whether the skill reads accessible inputs, asks a question, chooses a decision mode,
handles a blocker or makes an execution/freshness claim. Record real-environment
trials separately; a passing process eval is not evidence of superior football
prediction.

Coding agents should follow the compact [AGENTS.md](../AGENTS.md) guide in addition
to [CONTRIBUTING.md](../CONTRIBUTING.md). See [releases](releases.md) for versioning,
package contents and publication.
