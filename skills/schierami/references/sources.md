# Source hierarchy and freshness

## 1. League and roster facts

Use the user's own context first:

1. Public Leghe Fantacalcio pages when the user supplies a league URL or slug and the required data is visible without authentication. Treat these pages as first-party league context. See `public-league-pages.md`.
2. User-provided screenshots, images, lists, tables, exports or files.
3. Roster/rules already established in the conversation.
4. Explicit user statements.

Do not require a special integration when the needed roster or league facts are already present in the conversation or publicly visible. Do not bypass authentication or infer hidden values.

## 2. Probable formations and availability

Use multiple independent sources when a decision is close.

Preferred order:

1. **Official club channels** — confirmed squad lists, medical updates, suspensions, coach press conferences and official starting XI.
2. **Fantacalcio.it** — probable formations, ballot percentages/context, injuries, doubts, suspensions and fantasy-specific role notes.
3. **Sky Sport Italia** — probable formations and reporter/team-news cross-check.
4. Other reputable Italian football outlets when the first three are incomplete or conflicting.

When kickoff is close, search specifically for same-day updates and official XI already released.

## 3. Player and team performance

Use current-season statistics from established football-stat providers, preferring data with minutes played and transparent metric definitions.

Useful sources include:

- FotMob for current player/team metrics, minutes, shots, xG/xA and match context.
- FBref when current competition coverage is available and metric definitions match the question.
- Official Serie A/team data for schedule, results and disciplinary context.

Normalize for minutes and actual role. Raw season totals can mislead when playing time differs.

## 4. Matchup and game-state context

Use team strength, home/away context, expected possession, chance creation/concession, tactical matchup and likely game script before prediction sites. Forebet or betting-market probabilities may be used only as a secondary signal; never let them override team news or tactical role.

## Freshness rules

- **Within 6 hours of deadline:** strongly prefer same-day reports and official sources.
- **6-24 hours:** use latest probable formations plus press conferences/team updates.
- **More than 24 hours:** treat lineups as preliminary and flag likely changes.
- For a player returning from injury or involved in a late fitness test, search for the most recent update regardless of older probable lineups.

## Search patterns

Use targeted queries, for example:

- `[team] probabile formazione [opponent] oggi`
- `[player] titolare ballottaggio oggi`
- `[player] infortunio conferenza allenatore`
- `[team] convocati [opponent]`
- `[player] rigorista punizioni corner [team]`
- `[coach] turnover coppe [team]`

Prefer pages whose update timestamp can be identified.
