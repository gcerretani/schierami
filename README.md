# Schierami

**Schierami** e un assistente indipendente per il fantasy football italiano sulla Serie A, specializzato nella scelta della formazione giornata per giornata.

La prima versione e un plugin **skills-only** per ChatGPT e Codex. Parte dalla rosa dell'utente, fornita in qualunque forma utile:

- URL pubblico della lega;
- screenshot o immagine;
- lista o tabella;
- file o export;
- informazioni gia presenti nella conversazione.

Poi ragiona come un fantallenatore veterano: controlla probabili formazioni, infortuni, ballottaggi, ruolo tattico reale, piazzati, minutaggio atteso, matchup, congestione del calendario, rotazioni, statistiche sottostanti, modificatore e copertura della panchina.

L'obiettivo e uno solo: **scegliere il miglior XI possibile per quella giornata, con modulo e panchina coerenti con le regole della lega**.

## Struttura

```text
.codex-plugin/plugin.json
skills/schierami/
  SKILL.md
  agents/openai.yaml
  references/
docs/
```

## Filosofia

Schierami non usa classifiche generiche o il nome del giocatore come scorciatoia. Le decisioni privilegiano minuti attesi, ruolo reale, contesto tattico, fonti aggiornate e valore atteso complessivo della formazione.

## Indipendenza

Schierami non e affiliato, sponsorizzato o approvato da Fantacalcio S.r.l., Lega Serie A, Sky, FotMob o dagli altri fornitori di dati citati nelle istruzioni della Skill. I nomi di terze parti sono usati solo per identificare fonti informative.
