# Leghe Fantacalcio input handling

Use this reference when the user mentions or pastes a `leghe.fantacalcio.it` league URL.

## Policy and product rule

Do not automatically crawl, scrape or traverse Leghe Fantacalcio pages to reconstruct a roster or league settings unless an explicitly authorized access method is available. Fantacalcio's current Terms of Use prohibit software or other mechanisms used to copy or access platform pages/content, including scraping, without express written authorization.

A league URL can still identify which league the user means, but it is not by itself a supported data-ingestion method for Schierami's public skills-only version.

## Supported league-context inputs

Prefer user-provided material that is already in the conversation:

- screenshot or image of the roster;
- pasted player list or table;
- exported file;
- screenshot or pasted text of the relevant league rules;
- roster/rules already established in the conversation.

If the user provides only a Leghe Fantacalcio URL and the exact roster is required, ask for one compact artifact: preferably a screenshot of the roster. If a rule can materially change the XI, ask only for that rule or the relevant settings screenshot.

## What the platform can configure

Official Leghe Fantacalcio guides show that league administrators can configure, among other things:

- allowed formations and roster/bench composition;
- Switch and lineup timeout;
- number and type of substitutions;
- office-reserve behavior;
- vote source;
- bonus/malus values;
- head-to-head goal thresholds and bands;
- goalkeeper, defense, midfield, attack and module modifiers;
- other performance/captain factors depending on game mode.

These describe what the platform supports, not what a specific league selected. Never infer a league's settings from platform defaults or from observed scores alone.

## Known technical distinction

Independent proof-of-concept work has shown that detailed settings can be retrieved from authenticated Leghe Fantacalcio API calls such as roster, lineup and calculation settings. Those calls require authenticated session data and are not evidence that the same values are publicly available from a league slug.

Schierami's current public skills-only scope must not depend on those authenticated or undocumented endpoints.

## Decision rule

Collect only settings that can change the recommendation. If a missing setting cannot affect the XI, proceed. If it can flip module, modifier value or substitution insurance, make the assumption explicit or request one focused screenshot/paste.
