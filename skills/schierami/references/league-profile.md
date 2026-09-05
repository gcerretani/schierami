# Scoped league profile

## Identity and provenance

Separate real competition(s)/season, fantasy league, fantasy competition, team, game system and host platform. A cup can have different rules from its league. Keep roster timestamp and fantasy-to-real-matchday mapping. Resolve team/name collisions, transfers and role changes against the relevant competition's list.

Store each rule as a fact with value, status, source/locator and optional as-of and valid-until dates. Use the [profile schema](../schemas/league-profile.schema.json) and [synthetic example](../examples/league-profile.json) as internal structures, not a questionnaire to hand to the user. A cell/range or quoted settings label is a better locator than "Excel". Separate observed evidence from inferred values.

Statuses: confirmed, user_stated, hypothesis, unknown, conflicted, not_applicable. Unknown/conflicted/not_applicable values are null, never false or zero. Keep both conflicting alternatives and their sources. A hypothesis cannot become confirmed through repetition by the assistant. Check hypotheses that could flip the choice.

## Decision-relevant inventory

- Roster, eligible roles, modules/slots, starter and bench counts, captain/vice.
- Vote source; event bonus/malus, role-dependent scoring, clean sheets and saves.
- Each modifier's activation, inputs, thresholds, rounding, target and timing.
- No-vote exceptions, maximum substitutions, priority/order, module changes, adaptation penalties, office reserves, Switch and whether they consume changes.
- Contest objective, points for win/draw/loss, goal bands, gap/tie rules, opponent data needed by scoring, home factors, ties and knockout qualification.
- Global or rolling deadline, time zone, locks, postponements and double gameweeks.

Names such as Classic, Mantra or "defense modifier" are pointers, not formulas. At first intake ask briefly whether there are custom scoring or substitution rules. Then collect only details that can affect the request. Do not require auction budget or transfer rules for a lineup decision unless they constrain eligibility.

## Reuse, updates and conflicts

Read accessible files before asking for their contents. Inspect all relevant sheets, not only an indexed snippet; do not treat an inaccessible attachment as nonexistent. Preserve source and extraction uncertainty for visual/ambiguous cells. If a file is unreadable, request only the missing part in a usable form.

Reuse the profile only within its scope and accessible storage. Refresh after announced rule/roster changes or season/competition changes. A newer message explicitly correcting a rule can supersede the old fact; retain the reason. Otherwise ask about material conflicts rather than selecting the convenient value. Sports news freshness is separate from the usually slower-changing rules.

Do not promise cross-chat persistence or write private profiles to a public repo.

## Completeness is decision-specific

Tag a gap as blocking legality, potentially flipping the decision, or irrelevant to this request. Resolve the first two using clarification-policy.md. Explain the assumed objective when opponent forecasts are unavailable. If an opponent-dependent modifier exists, opponent data may be needed even to calculate one's own score.

The executable scenario contract is a separate projection of confirmed rules; schema-valid profile data alone does not prove those rules are complete or true.
