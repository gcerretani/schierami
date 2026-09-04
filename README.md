# Schierami

**Schierami** e un assistente indipendente per il fantasy football italiano sulla Serie A, specializzato nella scelta della formazione giornata per giornata.

> **Il tuo assistente scientifico per il fantasy football italiano.**

La prima versione e un plugin **skills-only** per ChatGPT e Codex. Parte dalla rosa e dalle regole che l'utente fornisce nel contesto, per esempio tramite:

- screenshot o immagine;
- lista o tabella;
- file o export;
- screenshot o testo delle regole della lega;
- informazioni gia presenti nella conversazione.

Un URL di Leghe Fantacalcio puo identificare la lega, ma questa versione non dipende dal crawling o scraping automatico della piattaforma.

Schierami controlla probabili formazioni, infortuni, ballottaggi, ruolo tattico reale, piazzati, minutaggio atteso, matchup, congestione del calendario, rotazioni, statistiche sottostanti, modificatori e copertura della panchina.

L'obiettivo e uno solo: **scegliere il miglior XI possibile per quella giornata, con modulo e panchina coerenti con le regole della lega**.

## Metodo

Schierami usa un processo decision-first:

1. ricostruisce rosa, ruoli e regole che possono cambiare la scelta;
2. costruisce una formazione provvisoria e identifica i pochi **swing decisions** davvero decisivi;
3. ricerca solo le informazioni che possono cambiare quelle scelte;
4. valuta prima disponibilita, voto probabile e minutaggio atteso;
5. passa poi a ruolo tattico, piazzati, matchup e indicatori sottostanti;
6. confronta i moduli come sistemi completi, includendo modificatori e copertura della panchina;
7. espone l'incertezza e indica quale notizia dell'ultima ora potrebbe ribaltare un ballottaggio.

La procedura operativa e documentata in `skills/schierami/references/research-protocol.md` e `expert-playbook.md`.

## Principi evidence-based

Le regole decisionali di Schierami sono state confrontate con letteratura accademica su fantasy football e football analytics.

In particolare:

- la performance dei manager fantasy mostra una componente di abilita persistente nel tempo, pur con forte rumore e fortuna; questo supporta l'idea di ottimizzare un processo ripetibile invece di inseguire il risultato di una singola giornata;
- la selezione della squadra e stata formalizzata in letteratura come problema di ottimizzazione vincolata, quindi Schierami confronta il valore della formazione completa e non undici giocatori isolati;
- disponibilita, probabilita di voto e minutaggio atteso vengono trattati come input di primo livello prima dell'upside per 90 minuti;
- forma recente e bonus dell'ultima giornata vengono regressi verso segnali piu stabili quando non sono accompagnati da ruolo, minuti e opportunita ripetibili;
- xG/xA e statistiche sottostanti sono usati come indicatori di processo, non come oracoli;
- congestione del calendario ed Europa aumentano soprattutto incertezza di rotazione e rischio, non generano automaticamente una penalizzazione fissa per tutti;
- il modificatore difesa viene valutato come proprieta del sistema portiere-difensori e della formula specifica della lega;
- fonti indipendenti e recenti sono preferite a molte copie dello stesso report.

La mappa completa evidenza -> regola operativa e in `skills/schierami/references/scientific-evidence.md`.

## Riferimenti principali

- O'Brien, Gleeson & O'Sullivan (2021), *Identification of skill in an online game: The case of Fantasy Premier League*. PLOS ONE. https://doi.org/10.1371/journal.pone.0246698
- Bonomo, Duran & Marenco (2014), *Mathematical programming as a tool for virtual soccer coaches: a case study of a fantasy sport game*. https://doi.org/10.1111/itor.12068
- Maniezzo & Aspee Encina (2022), *Predictive Analytics for Real-time Auction Bidding Support: a Case on Fantasy Football*. https://doi.org/10.1007/s43069-022-00160-w
- Bhatt et al. (2019), *Who Should Be the Captain This Week? Leveraging Inferred Diversity-Enhanced Crowd Wisdom for a Fantasy Premier League Captain Prediction*. https://doi.org/10.1609/icwsm.v13i01.3213
- Pappalardo et al. (2019), *PlayeRank: Data-driven Performance Evaluation and Player Ranking in Soccer via a Machine Learning Approach*. https://doi.org/10.1145/3343172
- Julian, Page & Harper (2021), *The Effect of Fixture Congestion on Performance During Professional Male Soccer Match-Play: A Systematic Critical Review with Meta-Analysis*. https://doi.org/10.1007/s40279-020-01359-9
- Page et al. (2023), *The Effects of Fixture Congestion on Injury in Professional Male Soccer: A Systematic Review*. https://doi.org/10.1007/s40279-022-01799-5
- Scholtes & Karakus (2024), *Bayes-xG: player and position correction on expected goals using Bayesian hierarchical approach*. https://doi.org/10.3389/fspor.2024.1348983

## Privacy, termini e supporto

- Privacy: `docs/privacy.md`
- Termini: `docs/terms.md`
- Supporto: `docs/support.md`

## Struttura

```text
.codex-plugin/plugin.json
skills/schierami/
  SKILL.md
  agents/openai.yaml
  references/
brand/
docs/
LICENSE
```

## Filosofia

Schierami non usa classifiche generiche o il nome del giocatore come scorciatoia. Le decisioni privilegiano minuti attesi, ruolo reale, contesto tattico, fonti aggiornate e valore atteso complessivo della formazione.

Non promette di prevedere il calcio: cerca di prendere **decisioni migliori sotto incertezza** in modo ripetibile.

## Indipendenza

Schierami non e affiliato, sponsorizzato o approvato da Fantacalcio S.r.l., Lega Serie A, OpenAI, Sky, FotMob o dagli altri fornitori di dati citati nelle istruzioni della Skill. I nomi di terze parti sono usati solo per identificare piattaforme, competizioni o fonti informative.

## Licenza

Il progetto e distribuito sotto **MIT License**. Vedi `LICENSE`.
