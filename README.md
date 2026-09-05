# Schierami

**Schierami** e un assistente indipendente ed evidence-informed per le decisioni di formazione nel fantasy football.

> **Regole reali, fonti attuali, decisioni sotto incertezza.**

La skill non assume che ogni lega sia Serie A, Leghe Fantacalcio o Classic. Separa il campionato reale, la competizione fantasy, il sistema di gioco e la piattaforma; accetta rose e regolamenti da screenshot, file, export, testo, URL utilizzabili o contesto gia disponibile.

## Cosa cambia nella 0.2

- supporto esplicito a **Classic, Mantra e regolamenti personalizzati**;
- profilo di lega con provenienza e stati `confirmed`, `user_stated`, `hypothesis`, `unknown`, `conflicted` e `not_applicable`;
- politica di chiarimento: cerca prima nei dati accessibili e chiede all'utente solo cio che puo cambiare la scelta;
- separazione tra ricerca sportiva, interpretazione delle regole e calcolo deterministico;
- gerarchia delle fonti per tipo di informazione, non una lista di siti obbligatori;
- gestione esplicita di soglie non lineari, sostituzioni, modificatori, panchina e obiettivi head-to-head;
- script opzionali per validare una formazione e calcolare scenari supportati, con errori espliciti sulle regole non implementate;
- test di regressione per evitare duplicati, formazioni illegali e calcoli silenziosamente incompleti.

## Metodo

Schierami segue un flusso decision-first:

1. recupera rosa, competizione e regole gia disponibili;
2. distingue fatti confermati, ipotesi, conflitti e dati mancanti;
3. chiede una regola privata solo se valori plausibili possono cambiare legalita o raccomandazione;
4. costruisce una formazione provvisoria e identifica pochi **swing decisions**;
5. ricerca solo i fatti pubblici che possono ribaltare quelle scelte;
6. combina disponibilita, minutaggio, ruolo tattico, piazzati, matchup e indicatori sottostanti;
7. confronta intere formazioni legali, includendo sostituzioni e bonus strutturali secondo l'ordine reale delle regole;
8. espone assunzioni, limiti e la notizia o regola che potrebbe cambiare il consiglio.

Una regola chiamata "modificatore difesa" o un'etichetta come "Mantra" non viene trattata come formula completa: se la configurazione esatta conta, Schierami la verifica o la chiede.

## Evidence-informed, non infallibile

La letteratura accademica viene usata per definire priorita e ridurre bias: ottimizzazione vincolata della formazione, valore del minutaggio, regressione della forma recente, uso prudente di xG/xA, differenze tra rating, fixture congestion e decisioni sotto osservabilita parziale. La mappa evidenza -> regola operativa e in `skills/schierami/references/scientific-evidence.md`.

Gli articoli non dimostrano chi segnera nella prossima giornata. Le informazioni correnti vengono cercate nelle fonti appropriate alla domanda e alla competizione; una fonte e considerata usata solo se e stata realmente consultata per un fatto decisivo.

## Struttura

```text
.codex-plugin/plugin.json
skills/schierami/
  SKILL.md
  agents/openai.yaml
  references/
  schemas/
  examples/
  scripts/
  tests/
docs/
brand/
LICENSE
```

I calcolatori in `scripts/` sono volutamente limitati: validano input espliciti e scenari supportati, ma non simulano ogni piattaforma e non inventano probabilita. Una regola non supportata deve restare visibile e viene gestita manualmente o con un motore verificato, mai ignorata.

## Riferimenti scientifici principali

- O'Brien, Gleeson & O'Sullivan (2021), *Identification of skill in an online game: The case of Fantasy Premier League*. https://doi.org/10.1371/journal.pone.0246698
- Bonomo, Duran & Marenco (2014), *Mathematical programming as a tool for virtual soccer coaches*. https://doi.org/10.1111/itor.12068
- Bhatt et al. (2019), *Who Should Be the Captain This Week?* https://doi.org/10.1609/icwsm.v13i01.3213
- Pappalardo et al. (2019), *PlayeRank*. https://doi.org/10.1145/3343172
- Julian, Page & Harper (2021), fixture congestion meta-analysis. https://doi.org/10.1007/s40279-020-01359-9
- Scholtes & Karakus (2024), *Bayes-xG*. https://doi.org/10.3389/fspor.2024.1348983

## Privacy, termini e indipendenza

Schierami non deve pubblicare rose o regolamenti privati nel repository. Usa soltanto modalita di accesso disponibili e autorizzate; non richiede password o token di sessione in chat.

- Privacy: `docs/privacy.md`
- Termini: `docs/terms.md`
- Supporto: `docs/support.md`

Schierami non e affiliato, sponsorizzato o approvato da Fantacalcio S.r.l., Lega Serie A, OpenAI o dai fornitori citati. I nomi di terze parti identificano soltanto piattaforme, competizioni o fonti informative.

## Licenza

MIT License. Vedi `LICENSE`.
