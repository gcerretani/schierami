# League profile handling

Never assume the user's league settings or roster.

## Supported inputs

Obtain league context from material the user has explicitly supplied in the conversation:

1. screenshot or image of the roster;
2. pasted player list or table;
3. exported file;
4. screenshot or pasted text of league settings;
5. roster and rules already established in the conversation;
6. direct user statements.

A Leghe Fantacalcio URL can identify which league the user means, but the current skills-only version must not depend on automatically crawling or scraping the platform. See `public-league-pages.md`.

## Minimal rule checklist

Collect only settings that can change the recommendation. In priority order:

1. **Allowed formations** - needed to compare legal modules.
2. **Defensive modifier** - enabled/disabled and exact formula or table.
3. **Substitutions** - maximum number, Traditional/Dynamic/Hybrid behavior, and any role constraints.
4. **Bench and Switch behavior** - only when they change no-vote insurance or module flexibility.
5. **Vote source and scoring peculiarities** - only when they materially change player value.
6. **Head-to-head goal thresholds/bands** - only when the user wants opponent-aware risk optimization rather than pure expected points.
7. **Lineup deadline** - needed for freshness and late-news handling.

Other settings should be ignored unless they can change the XI.

## Confidence handling

Classify league inputs internally as:

- **confirmed** - explicitly visible in user-provided material;
- **stated** - explicitly told by the user;
- **unknown** - not available.

Never infer exact rules from platform defaults, previous lineups, observed scores, or another league.

If a missing rule cannot change the recommended XI, proceed. If it can flip module, modifier value or substitution coverage, ask for one focused screenshot or one direct answer rather than requesting the whole regulation.
