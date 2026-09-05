# Development

## Layout

```text
.codex-plugin/plugin.json       Plugin manifest and canonical version
.github/workflows/             CI and release automation
CHANGELOG.md                   Human-maintained version history
CONTRIBUTING.md                 Contributor conventions
README.md                      Stable project overview
docs/                          User and maintainer documentation
evals/                         Manual behavioral evaluation scenarios
tools/                         Repository checks and release builder
tests/                         Automated regression and packaging tests
skills/schierami/
  SKILL.md                     Skill entrypoint
  agents/openai.yaml           Skill display metadata
  assets/                      Existing project icon
  examples/                    Synthetic executable inputs
  references/                  Rules, research and evidence guidance
  schemas/                     League profile representation
  scripts/                     Optional runtime calculators
```

Only scripts under the skill are installed with it. Keep the skill self-contained:
its relative links must not depend on repository docs, tests or maintainer tools.

## Local checks

Use Python 3.10 or newer. The project checks and calculators use only the standard
library; no runtime package installation, API key or football data service is
required. Run from the repository root:

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py
```

Tests exercise calculators, example inputs and release packaging. Repository
checks validate local file links, required files and version/changelog consistency.
They do not validate every external URL, predict performance, or replace the
host's skill scan and submission review.

Executable examples:

```sh
python skills/schierami/scripts/validate_lineup.py < skills/schierami/examples/lineup.json
python skills/schierami/scripts/score_scenario.py < skills/schierami/examples/scenario.json
```

The lineup example is a synthetic two-player format, not a real competition
preset. The scenario is a synthetic partial defensive unit, not a complete XI.
Its expected result is one substitution, 30 player points, a +1 modifier and 31
total points. Read the [contract](../skills/schierami/references/scoring-model.md)
before using these scripts with real rules.

## Change discipline

Keep English prose consistent and use relative Markdown links for local documents.
Preserve the distinction between scientific evidence, rule deductions, qualitative
forecasts and deterministic calculations. Do not silently expand the calculators'
claimed coverage when adding conversational guidance.

The [evaluation checklist](../evals/README.md) is separate from automated tests.
Record actual runs and limitations before claiming a behavioral improvement.
See [releases](releases.md) for versioning, package contents and publication.
