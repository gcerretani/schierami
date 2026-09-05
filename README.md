# Schierami

**Fantasy soccer lineup advice built around your league's actual rules.**

Schierami is an independent skill for ChatGPT and Codex. It helps choose your
starting lineup, formation, captain and bench order using your roster, your rules
and the current football information available to the host assistant.

It is designed for association football (soccer), including Italian fantacalcio,
not American fantasy football. Classic, Mantra and custom leagues are handled as
distinct rule systems, regardless of platform or real-world competition.

**The repository is written in English. Advice follows the user's language,
including Italian.** English documentation does not impose English responses.

## Get started

Download **`skill.zip`** from the [latest GitHub release](https://github.com/gcerretani/schierami/releases/latest)
and follow the [installation guide](docs/installation.md). The separate
`schierami-plugin.zip` contains the plugin manifest and bundled skill; it is not
the same upload format as a standalone skill.

Provide a roster screenshot, list or export, identify the matchday, and include
relevant league settings when available. For example:

> Here is my roster. Pick the lineup and bench for the next matchday. We use a
> defensive modifier; ask me for its formula if it changes the best formation.

Schierami reuses accessible context before asking questions. If a missing rule
could change the decision, it asks for that specific rule instead of assuming a
platform default. With incomplete information it gives useful conditional advice,
not invented certainty.

## What it does

- Compares complete legal lineups, including positional constraints, substitutes
  and rule-dependent bonuses, rather than ranking players in isolation.
- Focuses research on the few uncertain choices that could change the lineup,
  using current sources appropriate to the competition and the question.
- Separates confirmed facts, assumptions, unresolved rules and sporting forecasts;
  explains the information that would reverse a close recommendation.
- Uses deterministic validation, additive optimization and scenario evaluation
  only when the supplied rules and quantitative inputs support those claims.

The method is informed by research on fantasy sports and football analytics.
See the [evidence-to-rule map](skills/schierami/references/scientific-evidence.md)
for papers, transfer limits and mathematical deductions. These references do not
prove that this skill has better predictive performance than alternatives.

## Forecasting and evaluation

The skill includes a standard-library-only empirical forecasting baseline, a
strict forecast-bundle contract, exact or seeded joint-block scenario evaluation,
and a chronological benchmark with probability and distribution metrics.
Current-news research remains a host responsibility; the Python modules process
supplied data and do not scrape providers or install packages.

Read the [forecasting contract](skills/schierami/references/forecasting.md) and
[scientific validation guide](docs/forecast-validation.md). A correct calculation,
a synthetic benchmark or an unvalidated baseline is **not evidence of improved
football predictions**. The baseline does not learn opponent adjustments, goals,
assists or match-level correlations, and no real-data superiority is claimed.

## Scope and limits

Schierami has no hosted backend, account service or automatic lineup submission.
Research, file access and optional Python execution depend on the host's tools
and permissions. It does not request passwords or session tokens.

Classic, Mantra and custom-rule **guidance** does not mean a complete executable
scoring engine for every platform. The bundled deterministic engine includes
lineup validation, additive XI optimization, explicit scenario scoring, whole-lineup
scenario comparison and a dispatcher that records the executed contract. Rule
calculation stays separate from the empirical forecast baseline. Neither layer
implements every platform's substitution logic or turns an unsupported real rule
into an assumed default. See the
[deterministic engine contract](skills/schierami/references/scoring-model.md).

For full-lineup calculations, `skills/schierami/scripts/run_lineup.py` is the
preferred deterministic entry point. It emits an observable run report containing
checks, blockers and execution scope; this is operational traceability, not hidden
chain-of-thought.

## Project map

| Location | Purpose |
| --- | --- |
| [skills/schierami](skills/schierami) | Installable workflow, references, examples, schemas, scripts and icon. |
| [.codex-plugin/plugin.json](.codex-plugin/plugin.json) | Plugin identity, listing metadata and canonical version. |
| [AGENTS.md](AGENTS.md) | Concise repository operating guide for coding agents. |
| [docs](docs/README.md) | Installation, development, release and submission guides. |
| [evals](evals/README.md) | Synthetic executable behavioral process evaluations. |
| [tools](tools) and [tests](tests) | Maintainer tooling and automated checks; excluded from installable bundles. |
| [CHANGELOG.md](CHANGELOG.md) | Version history and the source of GitHub release notes. |

For development, start with [CONTRIBUTING.md](CONTRIBUTING.md); coding agents should
also read [AGENTS.md](AGENTS.md). For help, see [support](docs/support.md),
[privacy](docs/privacy.md) and [terms of use](docs/terms.md).

## License and independence

[MIT License](LICENSE). Schierami is not affiliated with or endorsed by OpenAI,
Fantacalcio S.r.l., any league, club or data provider. A GitHub release is a project
release, not approval or publication in a third-party plugin directory.
