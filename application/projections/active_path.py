from pathlib import Path
from datetime import datetime
from uuid import UUID
from dataclasses import dataclass

@dataclass
class ActivePath:
    path: Path
    related_scan_ids: set[UUID]
    latest_observed_at: datetime

# TODO (projection evolution): extend ActivePath semantics gradually
# - Add observation_count
#     - track how many times path was re-observed
#     - useful as duplicate confidence signal
#
# - Add latest_modified_time
#     - latest known modified time for observed file
#     - may help distinguish moved/changed copies
#
# - Add stale/confidence semantics
#     - ACTIVE / STALE / UNKNOWN candidate states
#     - only after projection semantics stabilize
#
# - Add confidence scoring
#     - estimate probability that path still physically exists
#     - based on recency, scan history, stale timeout, etc.
#
# - Add last_seen_scan_id helper
#     - optional optimization for latest scan reasoning
#
# - Implement stale timeout model
#     - gradually reduce confidence for paths not observed recently
#     - avoid hard deletion assumptions
#
# - Add first_observed_at
#     - preserve historical lifetime semantics
#     - useful for analytics/intelligence layer
#
# - Add historical_occurrence_count
#     - separate audit/history metric
#     - distinct from active projection grouping
#
# - Investigate moved-file heuristics
#     - old path disappears
#     - new path appears
#     - same asset_id + temporal proximity
#     - possible move instead of duplicate
#
# - Add duplicate confidence classification
#     - weak / medium / strong duplicate candidate
#     - based on:
#         - simultaneous scan presence
#         - active path count
#         - stale confidence
#         - recency signals