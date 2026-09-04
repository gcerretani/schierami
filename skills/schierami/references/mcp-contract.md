# Future Schierami app / MCP contract

When a connected Schierami app exposes equivalent tools, prefer it for structured/private data. Tool names may differ; match by capability, not literal name.

## Desired capabilities

### `get_league_context`
Return league identity and relevant settings: team count, scoring, modules, modifier, substitutions and lineup deadline.

### `get_my_roster`
Return the user's current roster with fantasy role, Serie A club and acquisition price when available.

### `get_available_players`
Return free agents / svincolati filtered by role and optionally by search text.

### `get_matchday`
Return current fantasy matchday, Serie A fixtures and the user's fantasy opponent when available.

### `get_player_status`
Return normalized current status with source timestamps: availability, starter probability/consensus, injury/suspension, expected role and relevant notes.

### `get_probable_lineups`
Return probable XI and ballots for one or more Serie A matches, preserving per-source data rather than hiding disagreement.

### `get_player_stats`
Return current-season and recent-window statistics with minutes and data-source metadata.

### `get_match_context`
Return matchup context for a club/player: opponent, venue, recent team performance and relevant attack/defence indicators.

## Data-quality requirements

Every dynamic result should include:

- source/provider;
- fetched or updated timestamp;
- season/matchday where relevant;
- explicit `unknown`/missing values instead of fabricated defaults.

For consensus fields, retain the underlying source values so ChatGPT can reason about disagreement.
