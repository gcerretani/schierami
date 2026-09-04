# OpenAI Plugin Directory submission checklist

Schierami v0.1.0 e pensato come **skills-only plugin** specializzato nella scelta della formazione giornata per giornata.

## Listing draft

**Name:** Schierami

**Short description:** Il tuo esperto per scegliere formazione e panchina.

**Long description:** Schierami parte dalla rosa dell'utente, fornita tramite URL pubblico della lega, screenshot, lista, tabella, file o contesto gia presente nella conversazione. Analizza titolarita, ballottaggi, ruolo tattico reale, piazzati, minutaggio atteso, matchup, rotazioni, congestione del calendario, statistiche sottostanti e regole della lega per consigliare il miglior XI, il modulo e l'ordine della panchina per la giornata corrente.

**Category:** Sports

## Starter prompts

- Questa e la mia rosa: che formazione metto questa giornata?
- Chi schiero tra questi due giocatori?
- Controlla titolarita e rischi dell'ultima ora della mia rosa.
- Quali difensori conviene schierare se nella mia lega c'e il modificatore difesa?
- Questa e la URL pubblica della mia lega: ricostruisci la mia rosa e consigliami l'XI.

## Positive tests

1. User supplies a roster screenshot and asks for the best XI for the current matchday. Expected: reconstruct roster, resolve current fixtures/news, respect visible league rules, return XI plus bench and key risks.
2. User provides a public Leghe Fantacalcio URL and identifies their team. Expected: use publicly visible roster context, then research current Serie A information and recommend the lineup.
3. User asks "Zaccagni o Orsolini questa giornata?" Expected: compare current availability, expected minutes, tactical role, set pieces, matchup and recent underlying evidence; give a decisive recommendation with confidence.
4. User asks whether a doubtful player will start. Expected: check current probable formations and team news, cross-check uncertainty, classify status and cite recent evidence.
5. User asks which defenders to field with a defensive modifier. Expected: optimize the goalkeeper/defensive unit and structural modifier value rather than ranking defenders independently.

## Negative tests

1. User asks for NFL fantasy advice. Expected: do not invoke Schierami as an Italian Serie A workflow.
2. User asks for a generic explanation of the offside rule. Expected: answer normally; Schierami is not needed.
3. User asks for historical Serie A trivia unrelated to a lineup decision. Expected: do not force the Schierami workflow.

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
