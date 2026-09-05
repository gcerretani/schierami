# Changelog

Notable changes are recorded here in reverse chronological order. GitHub release
notes are extracted from the matching version section, not maintained in the README.
The plugin manifest is the canonical version source.

Versions 0.1.0 and 0.2.0 below document historical source snapshots. They did not
have GitHub releases or tags when this changelog was introduced; their dates are
source-history dates, not retrospective publication claims.

## [Unreleased]

## [0.3.0] - 2026-09-05

### Added

- Exact branch-and-bound XI optimization for supplied additive expected-point projections, legal formations, captain multiplier, locked starters and exclusions.
- Whole-lineup weighted scenario evaluation that applies substitutions and nonlinear threshold modifiers inside each scenario.
- Explicit decision-mode and optimality-scope fields so a proven model optimum is never confused with certainty about real matches.
- Regression tests for unknown nested rules, malformed booleans/counts, non-finite values, duplicate identities and exact decimal thresholds.

### Changed

- Deterministic contracts now fail closed instead of silently ignoring unsupported decision-changing fields.
- Threshold arithmetic uses exact decimal comparison.
- Substitute use is tracked by player identity rather than only bench position.
- Forecasts are explicitly separated from rule arithmetic: Schierami must not invent expected points or probabilities merely to run an optimizer.
- The lineup workflow checks the broader realistic candidate pool before narrowing to human-selected toss-ups.

## [0.2.1] - 2026-09-05

### Changed

- Establish English as the repository's documentation and metadata language while preserving responses in the user's language, including Italian.
- Replace the README's embedded version notes with a stable project overview and a navigable documentation index.
- Separate installation, contributor workflow, releases and directory submission; distinguish GitHub publication from third-party approval.
- Move maintainer tests out of the installable skill and place the existing icon inside the skill's assets without changing the artwork.
- Refresh outdated Serie-A-only descriptions and remove stale submission drafts.

### Added

- Reproducible `skill.zip` and `schierami-plugin.zip` builds with license notices, version metadata and SHA-256 checksums.
- CI checks for local documentation links, package contents, executable examples and version/changelog consistency.
- A release workflow that tests and builds the exact versioned commit, uploads assets to a draft, and publishes only after the upload succeeds.
- An executable lineup example and a separate manual evaluation checklist.

### Fixed

- Prevent independently assembled chat archives from drifting from repository source: release artifacts are built by the same checked-in script.
- Correct relative documentation links and clarify the calculators' actual scope.

## [0.2.0] - 2026-09-05

### Added

- Separate Classic, Mantra and custom-rule guidance.
- Scoped league profiles, provenance states and decision-sensitive clarification.
- Optional lineup validator and limited scenario scorer with synthetic examples.
- Initial calculator regression tests and a CI workflow.

### Changed

- Generalize beyond Serie A and a single fantasy platform.
- Route research by the question, freshness and independent evidence.
- Distinguish research priority from player preference, and model nonlinear thresholds, substitutes and contest objectives explicitly.

Source snapshot: `daf42244c89f89b10891921eca55f1593f543ed0`.

## [0.1.0] - 2026-09-04

### Added

- Initial skills-only plugin for Italian fantasy soccer lineup decisions.
- Decision-first research, player comparison and league-profile guidance.
- Scientific evidence map, project icon, privacy, terms and support documentation.
- MIT license and plugin metadata.

Source snapshot: `fdbdcd26370cc50dde367c04baf0b8ffe4597a04`.

[Unreleased]: https://github.com/gcerretani/schierami/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/gcerretani/schierami/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/gcerretani/schierami/releases/tag/v0.2.1
[0.2.0]: https://github.com/gcerretani/schierami/compare/fdbdcd26370cc50dde367c04baf0b8ffe4597a04...daf42244c89f89b10891921eca55f1593f543ed0
[0.1.0]: https://github.com/gcerretani/schierami/tree/fdbdcd26370cc50dde367c04baf0b8ffe4597a04
