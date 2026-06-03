from dataclasses import dataclass

from application.projections.asset_projection import AssetProjection

@dataclass
class DuplicateAnalysis:
    projection: AssetProjection
    outcome: str


# TODO: revisit outcome type after rules stabilize