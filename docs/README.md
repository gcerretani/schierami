# Documentation

## Using Schierami

- [Installation and first use](installation.md): choose the correct archive and host.
- [Support](support.md): report issues without exposing private league data.
- [Privacy](privacy.md) and [terms](terms.md): data handling and limitations.

## Developing and distributing

- [Contributing](../CONTRIBUTING.md): language, change and testing conventions.
- [Agent guide](../AGENTS.md): concise objectives and invariants for coding agents.
- [Development](development.md): repository layout and local commands.
- [Releases](releases.md): versions, changelog, packages and GitHub publication.
- [Directory submission](submission.md): third-party distribution checklist.
- [Behavioral evaluations](../evals/README.md): synthetic machine-scoreable process checks, not prediction claims.
- [Changelog](../CHANGELOG.md): historical changes and release notes.

## How the skill works

The [entrypoint](../skills/schierami/SKILL.md) links the operational references.
Start with the [league profile](../skills/schierami/references/league-profile.md),
[clarification policy](../skills/schierami/references/clarification-policy.md),
[research protocol](../skills/schierami/references/research-protocol.md) and
[scientific evidence](../skills/schierami/references/scientific-evidence.md).
The [deterministic engine contract](../skills/schierami/references/scoring-model.md)
describes what the optional runtime Python scripts actually support, while
[workflow traceability](../skills/schierami/references/workflow-traceability.md)
describes completion gates and observable execution records.
