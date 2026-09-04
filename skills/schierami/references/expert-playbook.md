# Evidence-based expert lineup playbook

Use this as the operating manual for weekly lineup decisions. Evidence IDs refer to `scientific-evidence.md`.

## 1. Solve the right problem first

Determine the legal modules, scoring formula, substitution rules, modifier and deadline before optimizing.

Default objective:

`lineup EV = sum(player EV) + expected structural bonuses + expected substitution value`

For a head-to-head league, change the objective to win probability only when opponent and threshold context are reliable enough to make that calculation meaningful. Otherwise maximize own expected points. [D1]

## 2. Apply the availability gate before upside

For each candidate, reason through:

`player EV = P(start) * EV if starting + P(sub appearance) * EV if substitute`

No-vote contributes zero before legal substitution value is considered.

Prioritize:

1. probability of a valid vote;
2. expected minutes;
3. role conditional on starting or entering;
4. only then per-minute upside.

Do not treat probable-lineup percentages as calibrated probabilities. Use them as evidence combined with official news, coach patterns and source freshness. [E3, E14]

## 3. Estimate conditional production, not raw reputation

Once availability is acceptable, estimate what the player can produce if he plays:

- actual tactical position and zones;
- box presence and shot quality;
- chance creation and key passes;
- penalties, direct free kicks and corners;
- team possession and territorial expectation;
- opponent strengths, weaknesses and likely game script;
- role-specific clean-sheet, save or card exposure;
- recent role change, coach change or injury return.

A famous player used deep or wide with low involvement can be worse than a less famous player with an advanced, stable role. [E9]

## 4. Use several time horizons

Build a prior from the longer sample, then update it:

- **1-3 matches:** fitness, role change, tactical experiment, recent minutes;
- **5-10 matches:** current involvement and team phase;
- **season/multi-season:** stable skill, finishing and baseline production.

Recent fantasy points alone are a weak forecast. A true role change can justify a large update; a single goal cannot. [E4, E7, E12]

## 5. Read underlying involvement correctly

Prefer repeatable opportunity indicators over realized bonuses:

- expected minutes;
- shots and shots in the box;
- non-penalty xG;
- key passes and xA;
- touches or receptions in dangerous zones;
- set-piece share;
- team xG/xGA and opponent concession profile.

Normalize for minutes and distinguish per-90 rate from expected total minutes. Use xG as a chance-quality baseline, not an oracle; apply only modest player-specific finishing adjustments backed by sufficient history. [E10]

## 6. Model the game script, but resist favourite bias

Classify the likely match:

- dominant favourite against a low block;
- transition-heavy open game;
- underdog counterattacking setup;
- low-event tactical game;
- team likely to chase after conceding.

Ask which role benefits. Do not select a player merely because his team is favourite; users systematically overweight that shortcut. [E8]

## 7. Treat independent consensus as a prior

For close or fragile decisions:

- seek at least two independent information streams;
- trace several articles back to the original report when possible;
- distinguish confirmed facts from consensus guesses;
- value a diverse mix of official news, specialist team reporting and data evidence.

Ten copied reports are one signal. A strong consensus can define a safe baseline, but the best decision may diverge when league rules or role context differ. [E1, E6]

## 8. Handle congestion without folklore

Do not assume `played in Europe = must be benched`.

Increase uncertainty when there is:

- two to four days of recovery;
- heavy recent minutes;
- travel;
- recent injury;
- a coach with a documented rotation pattern;
- a plausible replacement competing for the role.

Then verify current team news. Congestion raises injury and rotation concern, but evidence for a universal performance collapse is mixed. [E13]

## 9. Optimize the whole legal XI

For every plausible module:

1. select the best combination under role constraints;
2. add expected modifier and structural bonuses;
3. add expected substitution value;
4. check concentration of no-vote and correlated downside;
5. compare module-level expected value and robustness.

Do not choose players independently and then force a module around them. [E2, D2, D3]

## 10. Use variance deliberately

Expected value is the default. Use variance only after the expected-value gap is small.

Prefer floor when:

- substitution coverage is weak;
- the XI already contains several doubtful starters;
- the modifier rewards stable votes;
- a no-vote is especially costly.

Prefer ceiling when:

- the safe option is only marginally better in expectation;
- the risky player's upside comes from a real role advantage;
- bench coverage is strong;
- reliable head-to-head context shows that a higher-variance path improves win probability.

Never choose a weak differential solely because an opponent owns the favourite. [D1]

## 11. Defensive modifier procedure

Use the exact league formula. Evaluate goalkeeper and defenders as one unit:

- valid-vote probability;
- expected editorial or statistical vote floor, depending on league source;
- clean-sheet and goal-concession environment;
- save volume if relevant;
- card, penalty-concession and error risk;
- attacking/set-piece upside after reliability;
- covariance within the unit.

Compare the expected modifier contribution of a four-defender module with the attacker or midfielder displaced. Do not equate modifier value with clean-sheet probability alone. [D2]

## 12. Position-specific tie-breakers

### Goalkeepers

Prioritize expected goals conceded under the league's penalty structure, clean-sheet chance, defensive quality and save opportunity. Avoid blindly choosing the home goalkeeper.

### Defenders

With a modifier, prefer reliable valid votes and low error/card risk before marginal attacking upside. Without a modifier, give more weight to advanced full-backs, wing-backs and set-piece center-backs when the matchup supports their route to bonus.

### Midfielders

Prefer advanced role, box entries, chance creation, set pieces and stable minutes. Discount nominally attacking names used as deep controllers or ball-winners when the scoring system rewards goals and assists.

### Forwards

Expected minutes, centrality, penalty-box role and penalty duty dominate. Do not bench a striker solely for a scoring drought if chances and role remain strong; do not chase a recent scorer whose opportunity remains poor. [E7, E10, E12]

## 13. Bench order is insurance

Order the bench by expected value conditional on being used, constrained by legal substitutions:

1. ensure role-compatible cover for the most likely no-votes;
2. prioritize vote probability when coverage is scarce;
3. among similarly reliable options, prefer upside;
4. avoid putting the only safe replacement behind a speculative option when order matters.

A risky starter can be correct with strong insurance and wrong with no insurance. [E2, D3]

## 14. Do not mix opaque ratings

WhoScored, FotMob and SofaScore ratings are systematically different. Do not average them or use a raw `7.2 vs 7.0` comparison across providers. Prefer raw events and compare a player with peers within the same source, role and time window. [E11]

## 15. Remove predictable human bias

Before finalizing, check:

- Am I chasing last week's bonus? [E7, E12]
- Am I starting a star because of reputation?
- Am I overvaluing the match favourite? [E8]
- Am I treating copied reports as independent consensus? [E6]
- Am I ignoring a role or coach change?
- Am I overreacting to a tiny sample?
- Am I confusing a good outcome with a good decision? [E12]

## 16. Express two kinds of confidence

Keep separate:

- **information confidence:** how reliable and fresh are availability, role and source inputs?
- **decision gap:** how much better is the preferred option under those inputs?

A 70/30 decision can still have low information confidence. A 52/48 decision can rest on excellent information but remain a genuine toss-up.

## 17. Audit decisions over batches

After matches, review the process without hindsight:

- Were the availability and minutes scenarios reasonable before the deadline?
- Did the player occupy the expected role?
- Was the matchup read correctly?
- Did the recommendation rely on repeatable opportunities or a narrative?
- Was the bench ordered coherently?

Evaluate calibration across many decisions. One lucky goal or unlucky post is not enough to validate or reject the method. [E1, E12]
