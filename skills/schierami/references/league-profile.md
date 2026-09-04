# League profile handling

Never assume a public user's league settings or roster.

Before making a recommendation that materially depends on league rules or roster membership, obtain the relevant context from one of these sources, in order:

1. Connected league tools, when available.
2. A public Leghe Fantacalcio league URL supplied by the user, such as `https://leghe.fantacalcio.it/<league-slug>`. Inspect the public league pages and navigable sections for roster/team information and league settings that are visible without authentication. See `public-league-pages.md`.
3. Rules, screenshots or exports supplied in the current conversation.
4. A direct user statement about the league.

A public league URL is sufficient context when it exposes the information needed for the task. Do not require authentication or an MCP merely because the data belongs to a fantasy league if the same data is publicly visible.

Relevant settings and facts can include:

- number of teams;
- team names and participants;
- current rosters and player ownership;
- auction budget and acquisition prices when publicly shown;
- allowed formations;
- defensive modifier and exact formula;
- substitutions and bench size;
- scoring bonuses and penalties;
- lineup deadline;
- roster constraints;
- competitions and current fantasy opponent when publicly visible.

If a public page does not expose a required fact, do not infer it from page structure or from another league. Fall back to a connected tool, user-provided material or an explicit statement.

If a setting is unknown and does not materially affect the recommendation, proceed without blocking and state the assumption only when useful. If it could flip the recommendation, make the uncertainty explicit rather than inventing a default.
