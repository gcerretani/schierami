# Source hierarchy and freshness

## 1. League and roster facts

Prefer, in this order:

1. Connected league tools for structured/private league facts such as roster, credits, opponent, available players and scoring settings.
2. Public Leghe Fantacalcio pages when the user supplies a league URL or slug and the required data is visible without authentication. Treat these pages as valid first-party league context, not as generic web speculation. See `public-league-pages.md`.
3. User-provided screenshots, exports or explicit statements.

Do not require an MCP for data that the league itself exposes publicly. Conversely, do not attempt to bypass authentication, call undocumented private endpoints solely to evade access controls, or infer hidden values from unrelated public leagues.

## 2. Probable formations and availability

Use multiple independent sources when a decision is close.

Preferred order:

1. **Official club channels** — confirmed squad lists, medical updates, suspensions, coach press conferences and official starting XI.
2. **Fantacalcio.it** — probable formations, percentage/ballot context, injuries, doubts, suspensions, fantasy-specific role notes and updates.
3. **Sky Sport Italia** — probable formations and reporter/team-news cross-check.
4. Other reputable Italian football outlets only when the first three are incomplete or conflicting.

When the first match is close to kickoff, search specifically for same-day updates and official formations for matches already released.

## 3. Player and team performance

Use current-season statistics from established football-stat providers, preferring sources with transparent event data and minutes played.

Useful sources include:

- FotMob for current player/team metrics, minutes, shots, xG/xA and match context.
- FBref when current competition coverage is available and the metric definition matches the question.
- Official Serie A/team data for schedule, results and disciplinary context.

Always normalize for minutes and role. A raw season total can mislead when players have different playing time.

## 4. Matchup and prediction context

Use table position, recent team performance, home/away context and chance creation/concession before using prediction sites. Forebet or betting-market probabilities can be used only as a secondary signal for expected game state; never let them override confirmed team news.

## Freshness rules

- **Within 6 hours of deadline:** strongly prefer same-day reports and official sources.
- **6-24 hours:** use latest probable formations plus press conferences/team updates.
- **More than 24 hours:** treat lineups as preliminary and flag likely changes.
- For a player returning from injury or involved in a late fitness test, search for the most recent update even if an older probable lineup lists them as starter.

## Search patterns

Use targeted queries instead of generic browsing, for example:

- `[team] probabile formazione [opponent] oggi`
- `[player] titolare ballottaggio oggi`
- `[player] infortunio conferenza allenatore`
- `[team] convocati [opponent]`
- `[player] rigorista punizioni corner [team]`

Prefer pages whose update timestamp can be identified.
