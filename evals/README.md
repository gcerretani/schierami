# Behavioral evaluation checklist

These are synthetic manual evaluation scenarios, not completed evaluations or
proof of predictive performance. Keep actual run records separate and do not
publish private user data. Automated tests live in [tests](../tests).

| Case | Expected behavior |
| --- | --- |
| Modifier enabled, formula missing | Ask for the formula if it can change the module; keep invariant recommendations. |
| Roster in an accessible attachment | Read it before asking for the same roster again. |
| Mantra with unknown substitution mode | Clarify Basic/Easy/Master when coverage depends on it; never call `ordered_slots` a Mantra engine. |
| Custom rules on an offline league | Interpret the supplied rules, test ambiguity with a small example, do not import platform defaults. |
| Real and fantasy matchday mismatch | Resolve the intended competition/round before using fixtures. |
| Two sites copying one report | Treat them as one information origin, not independent confirmation. |
| Old article with a current site header | Verify the article's season, match and update; do not claim freshness from the header. |
| No live research available | Provide useful provisional advice and state the freshness limit. |
| Italian request with English resources | Answer in Italian without changing role labels or league terminology. |
| English request about another soccer league | Answer in English and choose relevant local sources, not automatic Serie A assumptions. |
| Last-week lucky goal, unchanged opportunities | Avoid automatically promoting the player based only on the outcome. |
| NFL lineup or unrelated football trivia | Do not force the fantasy-soccer lineup workflow onto an unrelated task. |

For comparisons, hold model, inputs, available tools and research budget constant.
Record version, date, scenario, evidence, rule errors, unnecessary questions,
unsupported claims, tool calls and latency. Judge only information available
before the deadline; distinguish a lucky result from a sound decision process.
No behavioral benchmark score is claimed by the packaging or unit-test suite.
