---
name: schierami
description: Assist with Italian Serie A fantasy-football decisions using fresh, source-backed information and league context. Use for weekly lineup choices, start/sit comparisons, bench order, probable starters, injuries and suspensions, set-piece roles, matchup analysis, waivers/free agents, trades, auction strategy, and opponent analysis. Prefer connected league tools when available; otherwise use public league pages supplied by the user and current web sources, cross-checking probable lineups and breaking team news before recommending players.
---

# Schierami

Use fresh evidence and explicit league rules to make practical Italian fantasy-football decisions. Separate factual retrieval from fantasy judgement: first establish availability, expected role, matchup and recent evidence; then recommend.

## Core workflow

1. Determine the decision type:
   - Full weekly lineup -> follow **Weekly lineup workflow**.
   - Start/sit or player comparison -> follow **Player comparison workflow**.
   - Availability/titolarity question -> follow **Availability workflow**.
   - Auction, waivers or trades -> load `references/player-evaluation.md` and adapt the horizon from one match to rest-of-season value.
2. Load `references/league-profile.md` whenever formation, module, modifier, budget, roster ownership or roster construction matters.
3. Retrieve league context in this order:
   - connected league tools, when available;
   - a public Leghe Fantacalcio league URL supplied by the user, following `references/public-league-pages.md`;
   - screenshots, exports or explicit user statements.
   Do not require an MCP for league facts that are already publicly visible.
4. For time-sensitive Serie A facts, use current web research. Follow the source hierarchy and freshness rules in `references/sources.md`.
5. Never make a final lineup recommendation from a single probable-lineup source when the choice is close or a player is a rotation risk.
6. Distinguish facts from judgement. If sources disagree, say so and lower confidence instead of averaging away the disagreement.

## Weekly lineup workflow

1. Resolve the relevant Serie A matchday and lineup deadline. If the user gives a screenshot or roster, extract all plausible starters and bench options.
2. Retrieve league context if available: roster, allowed modules, modifier rules, substitutions, opponent and special scoring rules.
3. For each realistic candidate, establish:
   - current availability;
   - expected start probability or starter/bench consensus;
   - injury/suspension/rotation risk;
   - likely role, including penalties and major set pieces when relevant;
   - opponent and home/away context;
   - recent minutes and attacking/defensive involvement when decision-relevant.
4. Cross-check probable starters with at least two sources for uncertain or consequential choices.
5. Optimize the XI for expected fantasy value while respecting structural bonuses such as the defensive modifier.
6. Order the bench deliberately. Prioritize reliable vote coverage when substitutions are limited or uncertain starters are selected.
7. Output a decisive XI, bench order and only the important toss-ups. Include a confidence level for fragile choices.

## Player comparison workflow

Compare candidates on the dimensions in `references/player-evaluation.md`. Weight them differently depending on the question:

- **This matchday:** availability, expected minutes and matchup dominate.
- **Next few matchdays:** add schedule quality and role stability.
- **Auction/trade/waiver:** prioritize sustainable role, season-long production, team strength, set pieces, injury history and price/opportunity cost.

When the choice is close, give a directional split such as `60/40` and state which new information could flip it.

## Availability workflow

1. Check the latest probable formation and team news.
2. Prefer official team communication for confirmed injuries, suspensions and squad lists when available.
3. Cross-check probable lineup status with fantasy-football and general football sources.
4. Report the last meaningful update time when available.
5. Classify the player as one of: `likely starter`, `ballot`, `likely bench`, `unavailable`, or `unclear`.

## Output style

Default to concise, actionable Italian unless the user requests otherwise.

For a full lineup, use this structure:

- **Modulo e XI consigliato**
- **Panchina in ordine**
- **Ballottaggi decisivi**: only choices that could reasonably go either way
- **Rischi dell'ultima ora**: players whose status may change before deadline

For a two-player comparison, lead with the recommendation, then 2-4 decisive reasons and a confidence split.

Do not dump raw statistics that do not affect the recommendation. Cite current web evidence when web research was used.

## Reliability rules

- Never treat an old probable lineup as current merely because the page itself is evergreen.
- Prioritize updates published closest to the lineup deadline.
- Do not infer that a player is fit merely because they are listed in a squad database.
- Do not infer penalty or set-piece duty from reputation alone; verify when it materially affects the call.
- Treat prediction/odds sites as supporting matchup evidence, not as authoritative lineup sources.
- If current information cannot be verified, make the uncertainty explicit and avoid false precision.
