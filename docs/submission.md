# OpenAI Plugin Directory submission checklist

Schierami v0.1.0 is a **skills-only plugin** specialized in Italian Serie A fantasy-football lineup decisions.

## Listing draft

**Name:** Schierami

**Short description:** Il tuo esperto per scegliere formazione e panchina.

**Long description:** Schierami e un assistente indipendente per il fantasy football italiano sulla Serie A. Parte dalla rosa e dalle regole fornite dall'utente tramite screenshot, lista, tabella, file o contesto gia presente nella conversazione. Analizza titolarita, minutaggio atteso, ruolo tattico reale, piazzati, matchup, rotazioni, congestione del calendario, statistiche sottostanti e regole della lega per consigliare il miglior XI, il modulo e l'ordine della panchina con un metodo evidence-based.

**Category:** Sports

**Brand payoff:** Il tuo assistente scientifico per il fantasy football italiano.

## Starter prompts

- Questa e la mia rosa: che formazione metto questa giornata?
- Chi schiero tra questi due giocatori?
- Controlla titolarita e rischi dell'ultima ora della mia rosa.
- Quali difensori conviene schierare se nella mia lega c'e il modificatore difesa?
- Ti mando lo screenshot della mia rosa e delle regole: scegli modulo, XI e panchina.

## Positive tests

1. **Roster screenshot + full XI.** User supplies a roster screenshot and asks for the best XI for the current matchday. Expected: reconstruct roster, identify swing decisions, research current fixtures/news, respect stated league rules, return module, XI, bench and key risks.
2. **Missing decisive league rule.** User supplies a roster but says only that there is a defensive modifier without giving the formula. Expected: provide a provisional recommendation if possible and ask only for the specific modifier screenshot/text if the formula could flip the module; never invent defaults.
3. **Start/sit comparison.** User asks "Zaccagni o Orsolini questa giornata?" Expected: compare current availability, expected minutes, tactical role, set pieces, matchup and repeatable underlying evidence; give a decisive recommendation and the condition that could reverse it.
4. **Doubtful starter near deadline.** User asks whether a doubtful player will start. Expected: use the latest probable formations and team news, privilege official sources, cross-check genuinely independent reports, classify status and cite current evidence.
5. **Defensive modifier optimization.** User asks which defenders to field with a defensive modifier. Expected: optimize goalkeeper plus defensive unit and structural modifier value rather than ranking defenders independently; account for vote reliability and bench coverage.

## Additional QA tests before submission

- early-season tiny-sample case: do not chase a two-match scoring streak without role/minutes support;
- post-European fixture: increase rotation uncertainty without applying an automatic benching rule;
- conflicting probable-lineup sources: preserve scenarios and lower information confidence;
- poor bench coverage: prefer valid-vote probability when a speculative starter creates excessive no-vote risk;
- user provides only a Leghe Fantacalcio URL: do not crawl/scrape it; request one compact roster screenshot or pasted list if roster data is needed.

## Negative tests

1. User asks for NFL fantasy advice. Expected: do not invoke Schierami as an Italian Serie A workflow.
2. User asks for a generic explanation of the offside rule. Expected: answer normally; Schierami is not needed.
3. User asks for historical Serie A trivia unrelated to a lineup decision. Expected: do not force the Schierami workflow.

## Public URLs

Until a dedicated website is deployed, the public repository can be used as the project website:

- Website: https://github.com/gcerretani/schierami
- Support: https://github.com/gcerretani/schierami/blob/main/docs/support.md
- Privacy: https://github.com/gcerretani/schierami/blob/main/docs/privacy-draft.md
- Terms: https://github.com/gcerretani/schierami/blob/main/docs/terms-draft.md

## Release notes draft

**Schierami 0.1.0**

Initial public release. Evidence-based Serie A fantasy-football lineup assistant for choosing module, XI and bench. Uses current team news, expected minutes, tactical role, set pieces, matchup, repeatable performance indicators, league-specific rules, defensive-modifier logic and substitution coverage. The decision process is backed by a documented evidence map covering fantasy-sports optimization, football analytics, uncertainty and common decision biases.

## Manual platform requirements

The submitter must complete the OpenAI-side requirements in the official submission flow, including developer/business identity verification if requested, required Apps Management permission, geographic availability selection, logo upload, final metadata review and submission for review.
