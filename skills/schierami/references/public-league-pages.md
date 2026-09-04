# Public Leghe Fantacalcio pages

Use this reference when the user provides a public league URL such as `https://leghe.fantacalcio.it/<league-slug>`.

## Purpose

Treat publicly visible league pages as first-party league context. They can reduce or eliminate the need for a custom MCP when roster ownership and some league details are already exposed without authentication.

## Workflow

1. Open the league root URL supplied by the user.
2. Follow visible/navigation links within the same `leghe.fantacalcio.it/<league-slug>` namespace.
3. Look specifically for pages or sections corresponding to teams/squadre, rosters/rose, participants, competitions, calendar/results and league settings.
4. Extract only facts actually shown publicly: team names, player ownership, roster composition, acquisition prices/credits if visible, competition context and other exposed settings.
5. Preserve source URLs and note when the page appears stale or season-mismatched.
6. If the public site does not expose a required fact, fall back to a connected league tool or user-provided context.

## Important constraints

- Publicly visible does not imply every datum exists; do not guess missing credits, scoring rules or deadlines.
- Do not bypass login, access controls or hidden/private endpoints merely because a public league page exists.
- Prefer the league's own public page over third-party copies for roster ownership.
- A league slug is league-specific. Never transfer roster or settings information between similarly named leagues.

## Practical implication

For questions such as "chi ho in rosa?", "chi e svincolato?" or "chi ha gia comprato questo giocatore?", first inspect the public league pages when the user has supplied the league URL. Only require an MCP when the needed data is not available publicly or when structured/private access would materially improve reliability.
