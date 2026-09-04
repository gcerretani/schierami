# Schierami

**Schierami** e un assistente indipendente per il fantasy football italiano sulla Serie A.

La prima versione e un plugin **skills-only** per ChatGPT e Codex. La Skill definisce un metodo ripetibile per:

- scegliere formazione e ordine della panchina;
- confrontare due o piu giocatori;
- controllare probabili formazioni, ballottaggi, infortuni e squalifiche;
- valutare matchup e statistiche recenti;
- ragionare su svincolati, scambi e asta.

Il metodo privilegia informazioni aggiornate, cross-check tra fonti e trasparenza quando le fonti sono in disaccordo.

## Struttura

```text
.codex-plugin/plugin.json
skills/schierami/
  SKILL.md
  agents/openai.yaml
  references/
docs/
```

## Roadmap

1. Pubblicare la versione skills-only nella directory ufficiale OpenAI.
2. Aggiungere un'app/MCP opzionale per dati strutturati e privati della lega: rosa, crediti, svincolati, avversario e impostazioni.
3. Integrare ulteriori fonti strutturate per stato giocatori e statistiche, quando legalmente e tecnicamente appropriato.

## Indipendenza

Schierami non e affiliato, sponsorizzato o approvato da Fantacalcio S.r.l., Lega Serie A, Sky, FotMob o dagli altri fornitori di dati citati nelle istruzioni della Skill. I nomi di terze parti sono usati solo per identificare fonti informative.
