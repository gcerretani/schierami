# Scientific evidence behind Schierami

This document separates evidence from inference. It does not claim that academic research can guarantee a fantasy-football win. It identifies findings that can improve repeated pre-deadline decisions and states when a rule is transferred or derived.

## Evidence grades

- **Grade A - direct:** peer-reviewed research on soccer fantasy games, or a systematic review directly relevant to the decision mechanism.
- **Grade B - transferable:** peer-reviewed association-football research that supports a component of fantasy evaluation, but does not test Italian fantasy lineups directly.
- **Grade C - exploratory:** preprint, single-season retrospective model, thesis or limited validation. Use as a useful hypothesis, not settled truth.
- **Derived:** a mathematical or logical consequence of the user's scoring, formation or substitution rules. Validate the rule inputs; no paper is needed to prove arithmetic.

## Evidence-to-rule map

### E1. Skill is persistent, but luck remains - Grade A

A study of about one million Fantasy Premier League managers found correlated performance across seasons. Long-term planning and consistently good decisions were the prime factors associated with success, while noisy real matches preserved a substantial role for luck. Higher-ranked managers also tended to converge on a strong core of common choices at important moments.

**Operational rule:** optimize a repeatable process and avoid judging expertise from one gameweek. Use consensus as a useful prior, not as an automatic answer.

Source: O'Brien, Gleeson & O'Sullivan (2021), *Identification of skill in an online game: The case of Fantasy Premier League*. https://doi.org/10.1371/journal.pone.0246698

### E2. Choose the legal lineup globally - Grade A

Mathematical-programming studies on soccer fantasy games model the problem as constrained team selection rather than eleven independent choices. An Argentinian fantasy model entered a public contest and finished among the highest scorers; later FPL and Italian Serie A work also optimized valid formations under budget and role constraints.

**Operational rule:** compare complete legal modules, including structural bonuses and replacement rules. Do not simply choose the highest-ranked player at each position.

Sources:

- Bonomo, Duran & Marenco (2014), *Mathematical programming as a tool for virtual soccer coaches: a case study of a fantasy sport game*. https://doi.org/10.1111/itor.12068
- Maniezzo & Aspee Encina (2022), *Predictive Analytics for Real-time Auction Bidding Support: a Case on Fantasy Football*. https://doi.org/10.1007/s43069-022-00160-w
- Venter & van Vuuren (2024), *An optimisation approach towards soccer Fantasy Premier League team selection*. https://doi.org/10.5784/40-1-753

### E3. Availability and expected minutes are first-order inputs - Grade A/C

The Bonomo model explicitly included a starting-lineup factor and emphasized good substitutes. OpenFPL found that advanced models beat a last-five-points baseline, but the commercial comparator remained strongest at identifying zero-point/non-playing cases; the paper attributes part of that edge to proprietary expected-minutes projections.

**Operational rule:** estimate start probability, substitute probability, expected minutes and vote probability before comparing upside. A strong per-90 player is not automatically a strong lineup choice.

Sources:

- Bonomo, Duran & Marenco (2014). https://doi.org/10.1111/itor.12068
- Groos (2025), *OpenFPL: An open-source forecasting method rivaling state-of-the-art Fantasy Premier League services* [preprint]. https://arxiv.org/abs/2508.09992

### E4. Combine player, team and opponent information over several horizons - Grade C

OpenFPL used position-specific ensembles with player-, team- and opponent-level features averaged over one, three, five, ten and 38 matches. It prospectively outperformed a last-five-points baseline across positions, although it remains a preprint and FPL scoring differs from Italian fantasy scoring.

**Operational rule:** use recent information for role and fitness changes, medium windows for current involvement, and longer windows as a stabilizing prior. Do not let one arbitrary recent window dominate.

Source: Groos (2025). https://arxiv.org/abs/2508.09992

### E5. No single forecasting method is universally best - Grade A/C

Italian Serie A auction research found large uncertainty, incomplete series and high variance; differences among forecasting algorithms were not statistically apparent in its validation. A later preprint found simple rolling forecasts, averaging and Monte Carlo approaches competitive, with robust variants not uniformly superior.

**Operational rule:** prefer converging evidence and calibrated uncertainty over allegiance to one model. When forecasts disagree, identify the input causing the disagreement instead of averaging blindly.

Sources:

- Maniezzo & Aspee Encina (2022). https://doi.org/10.1007/s43069-022-00160-w
- Ramezani & Dinh (2026), *A data-driven framework for team selection in Fantasy Premier League* [preprint]. https://arxiv.org/abs/2505.02170

### E6. Independent crowd diversity can improve a difficult choice - Grade A

In an FPL captain-selection study, a small semantically diverse crowd outperformed random crowds, most individual participants and crowds made only from previously top-ranked experts.

**Operational rule:** cross-check close calls with genuinely independent information streams. Ten sites repeating the same report are one signal, not ten.

Source: Bhatt et al. (2019), *Who Should Be the Captain This Week? Leveraging Inferred Diversity-Enhanced Crowd Wisdom for a Fantasy Premier League Captain Prediction*. https://doi.org/10.1609/icwsm.v13i01.3213

### E7. Recent form is real but dramatically overused - Grade A

A fantasy-soccer study found that a hot-hand signal explained about 10% of future performance variability but more than 60% of variation in user demand.

**Operational rule:** treat recent form as a modest update, not the forecast. Upgrade it only when supported by minutes, tactical role and underlying opportunities; regress isolated bonuses toward the longer-term baseline.

Source: Kotrba (2023), *Testing hot hand hypothesis at the individual athletes' level in soccer*. Economics Bulletin 43(3), 1356-1365. https://ideas.repec.org/a/ebl/ecbull/eb-23-00052.html

### E8. The favourite-team shortcut is overweighted - Grade A

Fantasy users rely on past performance and on whether a player belongs to the match favourite, but research found that users overestimate the benefit of the favourite-team heuristic.

**Operational rule:** use team strength and implied game state as context, but never let favourite status override expected minutes, individual role or the way the matchup creates chances.

Source: Kotrba (2020), *Heuristics in fantasy sports: is it profitable to strategize based on favourite of the match?* https://doi.org/10.1007/s11299-020-00231-7

### E9. Tactical role and multi-dimensional actions beat a universal rating - Grade B

PlayeRank used millions of match events across many competitions and a role-aware, multi-dimensional evaluation, outperforming comparison methods against professional-scout assessments.

**Operational rule:** evaluate what a player is asked to do and where his repeatable actions occur. Nominal fantasy position and one overall rating are insufficient.

Source: Pappalardo et al. (2019), *PlayeRank: Data-driven Performance Evaluation and Player Ranking in Soccer via a Machine Learning Approach*. https://doi.org/10.1145/3343172

### E10. xG is a baseline, not an oracle - Grade B

Bayesian xG research found that broad position effects diminished when richer shot-context variables were included, while some player-specific finishing effects persisted. Those effects require enough data and uncertainty-aware estimation.

**Operational rule:** prioritize chance volume and quality, but do not treat all xG as identical or permanently assume every player finishes at league average. Make only modest finishing adjustments supported by a meaningful multi-season sample.

Source: Scholtes & Karakus (2024), *Bayes-xG: player and position correction on expected goals (xG) using Bayesian hierarchical approach*. https://doi.org/10.3389/fspor.2024.1348983

### E11. Public algorithmic ratings are not interchangeable - Grade B

A study of 2,190 players and 73 performance metrics found systematic differences among WhoScored, FotMob and SofaScore ratings. The systems weight events differently and use opaque algorithms.

**Operational rule:** never average provider ratings as if they were measurements on the same scale. Prefer raw decision-relevant components; use ratings only within source and context.

Source: Ball, Huynh & Varley (2025), *Comparing player rating systems as a metric for assessing individual performance in soccer*. https://doi.org/10.1080/02640414.2025.2471208

### E12. Lucky outcomes contaminate evaluation - Grade B

A quasi-experimental football study compared nearly identical shots that hit the post and either scored or did not. Lucky goals causally improved subsequent managerial decisions and performance ratings.

**Operational rule:** separate process from outcome. Do not chase a player merely because a low-probability event happened last week, and do not downgrade a good role solely because the bonus failed to arrive.

Source: Gauriot & Page (2019), *Fooled by Performance Randomness: Overrewarding Luck*. https://doi.org/10.1162/rest_a_00783

### E13. Congestion is a risk modifier, not an automatic benching rule - Grade A transferable

A systematic review with meta-analysis found no clear universal reduction in total running performance under fixture congestion and reported heterogeneous evidence. A separate systematic review found overall injury risk increased during congested periods.

**Operational rule:** do not apply a blanket penalty to everyone who played in Europe. Increase uncertainty around minutes, rotation and physical risk; then use player history, coach behaviour, travel, recovery time and current news.

Sources:

- Julian, Page & Harper (2021), *The Effect of Fixture Congestion on Performance During Professional Male Soccer Match-Play: A Systematic Critical Review with Meta-Analysis*. https://doi.org/10.1007/s40279-020-01359-9
- Page et al. (2023), *The Effects of Fixture Congestion on Injury in Professional Male Soccer: A Systematic Review*. https://doi.org/10.1007/s40279-022-01799-5

### E14. Partial observability must remain explicit - Grade A

A Bayesian reinforcement-learning fantasy manager reached around the top percentile against 2.5 million users despite incomplete information. The problem was modeled as sequential decision-making under uncertain beliefs rather than deterministic prediction.

**Operational rule:** maintain scenario beliefs, update them with new information and expose when a recommendation is fragile. Do not convert uncertain team news into false certainty.

Source: Matthews, Ramchurn & Chalkiadakis (2012), *Competing with Humans at Fantasy Football: Team Formation in Large Partially-Observable Domains*. https://doi.org/10.1609/aaai.v26i1.8259

## Derived rules from game mechanics

These rules are not empirical findings. They follow from the scoring system once its inputs are known.

### D1. Correct objective

- Total-points league: maximize expected fantasy points.
- Head-to-head with thresholds: if opponent and threshold information are reliable enough, compare lineups by probability of winning or crossing the relevant threshold; otherwise default to own expected points.
- Use variance only when expected values are close or when a known contest state makes variance valuable.

### D2. Defensive modifier

Compute the expected contribution of goalkeeper plus eligible defenders under the exact modifier formula. A fourth reliable defender can be worth more than a marginal attacker even without direct bonus upside. The size of that edge is league-specific; never assume a generic modifier table.

### D3. Bench insurance

The value of a risky starter includes the conditional value of the legal replacement if he receives no valid vote. Bench order therefore depends on role compatibility, vote probability and upside conditional on substitution, not fame.

## What the literature does not establish

- No study proves a guaranteed winning strategy for Italian Fantacalcio.
- Most direct evidence comes from FPL or other soccer fantasy formats with different scoring and transfer rules.
- Automated event ratings are not the same as Italian editorial votes.
- Exact weights for minutes, matchup, xG, form and risk are not universal constants.
- Retrospective top-percentile results can overstate future performance through model selection and season-specific fit.
- Preprints should be treated as provisional until peer review and independent replication.

Schierami should therefore use the literature to define priorities, debias decisions and represent uncertainty, while adapting every choice to current Serie A evidence and the user's actual league rules.
