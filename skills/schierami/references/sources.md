# Source hierarchy and freshness

Use this file together with `research-protocol.md`. The goal is to retrieve the smallest set of current, independent facts that can change the lineup recommendation.

## 1. League and roster facts

Use only context the user has supplied or explicitly established:

1. screenshots, images, lists, tables, exports or files;
2. screenshots or pasted text of league settings;
3. roster/rules already established in the conversation;
4. explicit user statements.

A Leghe Fantacalcio URL may identify the league, but the current skills-only release must not automatically crawl or scrape the platform. See `public-league-pages.md`. Never bypass authentication or infer hidden values.

## 2. Confirmed availability and official XI

Preferred order:

1. **Official club channels** - squad lists, medical updates, coach press conferences and official starting XI.
2. **Official competition sources** - fixtures, suspensions and disciplinary information.
3. A current specialist report that clearly attributes its information.

An official call-up confirms squad selection, not a starting place or 90-minute fitness.

## 3. Probable formations and expected minutes

When availability can change the XI:

1. use a current fantasy-specific probable-lineup source with a visible update time;
2. cross-check with an independent general-football or team-specialist source;
3. trace copied reports back to the original source when possible.

Useful sources can include Fantacalcio.it and Sky Sport Italia when their current reporting addresses the specific decision. Do not count syndicated copies as independent confirmations.

## 4. Tactical role and set pieces

Prefer:

- recent official lineups and match usage;
- current coach comments;
- reliable tactical/team reporting;
- current fantasy-specific set-piece hierarchies.

After transfers, coaching changes or recent changes in penalty takers, treat old hierarchies as priors rather than facts.

## 5. Player and team performance

Use current data from established providers with clear metric definitions and playing-time context.

Useful sources include:

- FotMob for minutes, starts, shots, xG/xA and team/match context;
- FBref when current Serie A coverage and the relevant metric are available;
- official Serie A/team data for fixtures, results and disciplinary context.

Prefer raw decision-relevant metrics to provider-wide overall ratings. Normalize for minutes and actual tactical role. Never average opaque ratings from different providers as if they were the same scale.

## 6. Matchup and game-state context

Prefer team strength, expected possession, chance creation/concession and tactical matchup. Home/away is one component, not a decision rule by itself.

Betting-market or prediction-site probabilities may be used only as secondary priors for likely game state. They must never override availability, expected minutes or real tactical role.

## Freshness rules

- **Official XI available:** it overrides all probable-lineup sources for that match.
- **Within 6 hours of deadline:** strongly prefer same-day reports, official sources and timestamped probable lineups.
- **6-24 hours:** use the latest probable formations plus press conferences/team updates.
- **More than 24 hours:** treat lineup information as preliminary.
- **Returning injury / late fitness test:** always search for the newest meaningful update.
- **Coach or formation change:** downgrade old tactical-role evidence until the new setup repeats.

## Source independence

For a close decision, two genuinely independent current sources are more useful than many outlets repeating one report. When sources conflict, preserve the scenarios, compare timestamps and lower information confidence instead of averaging incompatible claims.

## Search patterns

Search for the unresolved fact rather than generic advice:

- `[team] probabile formazione [opponent] oggi`
- `[player] titolare ballottaggio oggi`
- `[player] infortunio rientro conferenza allenatore`
- `[team] convocati [opponent]`
- `[player] rigorista punizioni corner [team]`
- `[coach] turnover coppe [team]`
- `[player] minuti xG xA Serie A`

Prefer pages whose update timestamp can be identified. Stop searching when the remaining uncertainty cannot change the lineup or when an official source resolves it.
