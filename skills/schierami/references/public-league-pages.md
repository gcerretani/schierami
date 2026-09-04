# Public Leghe Fantacalcio pages

Use this reference when the user provides a public league URL such as `https://leghe.fantacalcio.it/<league-slug>`.

## Purpose

Treat publicly visible league pages as first-party context for reconstructing the user's roster and any visible league rules needed to recommend the best lineup.

## Workflow

1. Open the league root URL supplied by the user.
2. Follow visible/navigation links within the same league namespace.
3. Look for pages or sections corresponding to squadre/rose, participants, competitions, calendar/results and settings.
4. Extract only facts actually shown publicly: team names, player ownership, roster composition, competition context and relevant visible settings.
5. Identify the user's team from the current conversation or ask only if it cannot be inferred and is necessary.
6. Preserve source URLs and note if the page appears stale or season-mismatched.
7. If a required fact is not public, use screenshots, lists, files or explicit context supplied by the user instead.

## Important constraints

- Publicly visible does not mean every setting is available; do not guess missing scoring rules or deadlines.
- Do not bypass login or access controls.
- Prefer the league's own public page over third-party copies for roster ownership.
- Never transfer roster or settings information between similarly named leagues.

## Practical implication

If the public league page exposes the user's squad, Schierami can use it directly as roster input and then focus its research on the current Serie A matchday: probable lineups, injuries, tactical roles, matchups and other factors that affect who should be fielded.
