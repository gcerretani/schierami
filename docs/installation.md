# Installation and first use

Get a versioned package from [GitHub Releases](https://github.com/gcerretani/schierami/releases).
Do not confuse the assets with GitHub's automatically generated source archives.

| Asset | Use |
| --- | --- |
| `skill.zip` | One standalone skill, rooted at `schierami/SKILL.md`. |
| `schierami-plugin.zip` | Plugin bundle with `.codex-plugin/plugin.json` and `skills/`. |
| `SHA256SUMS` | SHA-256 hashes for both installable archives. |

Both packages include the skill resources and MIT notice. Neither includes
maintainer tests, release scripts, caches or private league data.

## ChatGPT

Where skill upload is enabled, open **Plugins > Skills > Create > Upload from your
computer** and select `skill.zip`. Review the contents and any scan results.
Availability depends on account, workspace and product settings. See OpenAI's
[current skill upload guide](https://help.openai.com/en/articles/20001066).

A local upload, sharing with a workspace and public directory publication are
separate operations. A GitHub release does not perform any of them automatically.
See [directory submission](submission.md) for distribution details.

## Codex: standalone local skill

Extract `skill.zip` and place the `schierami` directory in a supported skill
location, for example `$HOME/.agents/skills/schierami` for user scope or
`.agents/skills/schierami` for a project. Review an existing installation before
replacing it. Invoke it through the skill selector or `$schierami`.
See the [current local skill documentation](https://developers.openai.com/codex/skills).

For plugin-based distribution, use the plugin bundle and the host's supported
marketplace or plugin import flow. Do not put `schierami-plugin.zip` into a form
that explicitly expects a standalone skill. The
[plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
is the source of truth for supported import and marketplace formats.

## First request

Provide a roster, the relevant real and fantasy matchday, and any known custom
rules. Text, screenshots and accessible exports are all valid inputs. Write in
Italian or another preferred language; repository language does not determine
response language.

Schierami should recover information already available, ask only for important
missing rules, and distinguish verified facts from provisional advice. Current
news requires available research tools. Without them, the skill should explain
its freshness limits rather than claim live verification.

If Python execution is available, the optional calculators can check supported
inputs. They are not required for conversational advice and are not full platform
scoring engines. See the [contract](../skills/schierami/references/scoring-model.md).

Documentation links checked on 2026-09-05; host UI and availability may change.
