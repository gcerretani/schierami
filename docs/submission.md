# OpenAI Plugin Directory submission checklist

Schierami v0.1.0 e pensato inizialmente come **skills-only plugin**.

## Listing draft

**Name:** Schierami

**Short description:** Formazioni, ballottaggi e scelte fantasy con fonti aggiornate.

**Long description:** Schierami aiuta gli utenti del fantasy football italiano sulla Serie A a scegliere formazione e panchina, confrontare giocatori, controllare titolarita, infortuni e squalifiche, valutare matchup e statistiche, e ragionare su svincolati, scambi e asta. Usa fonti correnti e segnala esplicitamente i casi in cui le informazioni sono incerte o discordanti.

**Category:** Sports

## Starter prompts

- Che formazione metto questa giornata?
- Chi schiero tra questi due giocatori?
- Controlla titolarita e rischi dell'ultima ora della mia rosa.
- Quali difensori conviene schierare se nella mia lega c'e il modificatore difesa?
- Tra questi svincolati chi prenderesti per il resto della stagione?

## Positive tests

1. User supplies a roster screenshot and asks for the best XI for the current matchday. Expected: resolve current fixtures/news, respect visible league rules, return XI plus bench and key risks.
2. User asks "Zaccagni o Orsolini questa giornata?" Expected: compare current availability, expected minutes, role, matchup and recent evidence; give a decisive recommendation with confidence.
3. User asks whether a doubtful player will start. Expected: check current probable formations and team news, cross-check uncertainty, classify status and cite recent evidence.
4. User asks which defender to start with a defensive modifier. Expected: consider the defensive unit and modifier implications rather than only attacking upside.
5. User asks which free agent to acquire for the next two months. Expected: shift from one-match reasoning to role stability, schedule, underlying production and roster opportunity cost.

## Negative tests

1. User asks for NFL fantasy advice. Expected: do not invoke Schierami as an Italian Serie A workflow.
2. User asks for a generic explanation of the offside rule. Expected: answer normally; Schierami is not needed.
3. User asks for historical Serie A trivia unrelated to fantasy decisions. Expected: do not force the Schierami workflow.

## Still required before public submission

- production logo;
- public website URL;
- public support URL;
- public privacy policy URL;
- public terms URL;
- verified developer/business identity in OpenAI Platform;
- Apps Management write permission for the submitter;
- final review of plugin metadata and test cases;
- country/region availability choice;
- release notes.
