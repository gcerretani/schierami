# Decision-first research protocol

Use this protocol to gather only information that can change the recommended XI. The goal is not to collect every statistic; it is to reduce decision uncertainty before the lineup deadline.

## Two-pass workflow

### Pass A - frame the decision

1. Reconstruct roster, fantasy roles and relevant league rules.
2. Enumerate the legal modules that are realistically competitive.
3. Build a provisional XI from known role quality and expected availability.
4. Identify the **swing decisions**: normally 2-5 choices that can change module, XI or bench order.
5. List the smallest unknowns capable of flipping each swing decision.

Do not research every squad member equally. Obvious starters and unusable reserves need only an availability sanity check.

### Pass B - resolve swing decisions

Research unknowns in this order:

1. **P0 legality:** role, module, deadline, modifier and substitution rules.
2. **P1 availability:** suspension, injury, call-up, start probability, substitute probability and expected minutes.
3. **P2 conditional role:** real tactical position, penalties, direct free kicks, corners and likely substitution timing.
4. **P3 matchup:** opponent, venue, expected game state, team chance creation/concession and tactical zone affected.
5. **P4 repeatable production:** shots, box shots, non-penalty xG, key passes/xA, dangerous touches and role-specific indicators.
6. **P5 weak tie-breakers:** market probabilities, extreme weather, referee or narrative context. Use only when the decision remains genuinely close and the datum has a credible mechanism.

A lower-priority datum must not override a clear higher-priority edge.

## Internal evidence card

For every consequential candidate, keep a compact internal card:

```text
Player / fantasy role / club / opponent
Availability: likely start | ballot | likely bench | unavailable | unclear
Expected minutes: range or qualitative class
Valid-vote risk: low | medium | high
Real role: tactical position and duties
Set pieces: penalty / direct FK / corners / none / uncertain
Matchup: favourable | neutral | difficult, with one mechanism
Underlying evidence: only decision-relevant metrics and sample window
Structural value: modifier, module and bench implications
Information confidence: high | medium | low
Decision gap: clear | moderate | toss-up
Flip condition: the specific new fact that would reverse the choice
```

Do not show the whole card unless the user asks for the analysis.

## Source classes by question

### Confirmed availability and official XI

Prefer:

1. official club squad list, medical update, press conference or starting XI;
2. official competition communication for suspensions and fixtures;
3. a current specialist report that clearly attributes the information.

An official call-up proves squad selection, not that the player is fit for 90 minutes or starting.

### Probable lineup and expected minutes

Prefer a current fantasy-specific probable-lineup source with visible update time, then an independent general-football or team-specialist source. Trace copied reports to their original source. Do not count syndication as independent confirmation.

### Tactical role and set pieces

Prefer recent matches and official lineups, current coach comments, reliable tactical reporting and a current fantasy-specific set-piece hierarchy. A static pre-season hierarchy is only a prior after transfers, coaching changes or recent penalties taken by someone else.

### Player and team metrics

Prefer raw or clearly defined metrics from one established provider. Compare players within the same source, competition, role and time window. Use minutes, starts and sample size alongside per-90 rates.

Do not average opaque overall ratings from FotMob, SofaScore and WhoScored; published research shows systematic differences among those systems. Use raw components instead.

### Matchup and game state

Prefer official fixtures plus team/player event data. Use betting-market or prediction probabilities only as secondary priors for likely game state, never as evidence of starting status or individual role.

## Freshness rules

- **Official XI available:** overrides every probable lineup for that match.
- **Within 6 hours of the fantasy deadline:** prioritize same-day news, press conferences and timestamped probable lineups.
- **6-24 hours:** use the latest probable lineups plus official/team news.
- **More than 24 hours:** treat lineup information as preliminary.
- **Injury return or late fitness test:** seek the newest source regardless of older consensus.
- **Coach or formation change:** downgrade historical role evidence until the new structure repeats.
- **Set-piece change:** privilege the most recent credible evidence, but distinguish one emergency event from a stable hierarchy.

## Sample-size and shrinkage rules

At the beginning of a season or after very few appearances:

1. start from previous-season role, multi-season skill and expected team strength;
2. update strongly for confirmed tactical or personnel changes;
3. update cautiously for goals, assists, conversion rate and per-90 metrics from tiny samples;
4. use current minutes and starting status immediately because they describe opportunity, not finishing luck;
5. report when a metric is too sample-sensitive to drive the choice.

A role change is information. One converted shot is mostly an outcome.

## Search patterns

Use narrow queries around the unresolved fact:

- `[player] [team] titolare ballottaggio [opponent] oggi`
- `[team] convocati [opponent] [date]`
- `[coach] conferenza [opponent] [player]`
- `[player] infortunio rientro allenamento [date]`
- `[team] probabile formazione [opponent] aggiornata`
- `[player] rigorista punizioni corner [team]`
- `[player A] [player B] minutes xG xA Serie A`
- `[team] xG xGA home away Serie A current season`

Search for the fact, not for generic advice such as `chi schierare`. Advice articles may be an additional expert prior, but the final reasoning must rest on verifiable inputs.

## Independence and conflict resolution

When sources disagree:

1. compare timestamps;
2. identify whether one source has direct access or merely repeats another;
3. privilege official confirmation for factual status;
4. preserve distinct scenarios instead of averaging incompatible claims;
5. lower information confidence;
6. state the flip condition when material.

A diverse source set is better than many copies of one report.

## Stop rule

Stop researching a swing decision when:

- an official source resolves it;
- two genuinely independent, current sources agree and no credible contradiction remains;
- remaining uncertainty cannot change the XI or bench order;
- the expected-value gap is already large enough that another low-priority datum is unlikely to reverse it;
- the deadline requires action and the unresolved uncertainty is clearly disclosed.

More sources are not automatically better.

## Fallback and source suggestions

If a decisive fact cannot be verified:

- give the best provisional recommendation;
- identify exactly what remains unknown;
- suggest the most direct way to close it.

Examples:

- `Per decidere 4-3-3 o 3-4-3 serve la formula esatta del modificatore: manda lo screenshot della relativa voce nelle impostazioni della lega.`
- `La titolarità resta incerta: controlla convocati/conferenza del club e l'ultimo aggiornamento delle probabili formazioni.`
- `Il ruolo sui piazzati è cambiato da poco: verifica chi ha battuto gli ultimi rigori/corner con l'attuale allenatore.`

Ask for one focused artifact, not the entire regulation or account.

## Citation discipline

Cite the current sources that materially support the recommendation. Separate:

- verified facts;
- probabilistic interpretation;
- fantasy judgement.

The scientific literature defines the process; current sources decide the current lineup.
