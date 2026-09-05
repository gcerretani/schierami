# Contributing

Use English for repository documentation, code, metadata and release notes.
Keep official product names and rule labels such as Classic, Mantra and Switch.
User-facing advice follows the user's language; an English reference is not an
instruction to translate an Italian conversation into English.

Start with the [development guide](docs/development.md). Coding agents should also
read [AGENTS.md](AGENTS.md), which summarizes the project objective, invariants and
change workflow without replacing this contributor guide.

Add unreleased changes to [CHANGELOG.md](CHANGELOG.md), not the README. Before
submitting a change:

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py
```

Keep the skill entrypoint focused. Put detailed rules in directly linked
references and deterministic logic in tested scripts. Use synthetic data only;
do not commit private rosters, conversations, credentials or exports.

Document the limits of a change. A passing calculator test is not a behavioral
evaluation or evidence of improved football predictions. Use the executable
[behavioral evaluations](evals/README.md) for changes to decision behavior.

Follow the [release guide](docs/releases.md) when changing the plugin version.
Published releases are immutable project artifacts: corrections get a new version.
