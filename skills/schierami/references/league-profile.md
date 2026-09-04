# League profile handling

Never assume the user's league settings or roster.

Before making a recommendation that materially depends on league rules or roster membership, obtain the relevant context from one or more of these sources:

1. A public Leghe Fantacalcio league URL supplied by the user, such as `https://leghe.fantacalcio.it/<league-slug>`. Inspect public pages for roster/team information and league settings visible without authentication. See `public-league-pages.md`.
2. A screenshot, image or other visual representation supplied in the conversation.
3. A pasted list, table, export or file.
4. Roster and rules already established in the current conversation.
5. A direct user statement.

A public league URL is sufficient when it exposes the information needed for the task. Do not require a specific input format if the roster can be reconstructed reliably from available context.

Relevant settings and facts can include:

- user's team and current roster;
- allowed formations;
- defensive modifier and exact formula;
- substitutions and bench size/order rules;
- scoring bonuses and penalties;
- lineup deadline;
- number of teams when strategically relevant;
- current fantasy opponent or match context when publicly visible and useful.

Do not waste time collecting settings that cannot change the lineup decision.

If a required fact is not visible, do not infer it from another league or from platform defaults. If the missing setting could flip the recommendation, state the uncertainty. Otherwise proceed with the information available.
