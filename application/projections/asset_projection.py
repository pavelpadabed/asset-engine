from dataclasses import dataclass
from uuid import UUID
from collections import defaultdict

from application.projections.active_path import ActivePath
from domain.asset import Asset
from domain.occurrence import Occurrence

@dataclass
class AssetProjection:
    asset_id: UUID
    active_paths: list[ActivePath]

    @classmethod
    def from_occurrences(
            cls, asset_group: tuple[Asset, list[Occurrence]]
    ) -> "AssetProjection":
        asset, occurrences = asset_group
        asset_id = asset.id

        grouped_by_path = defaultdict(list)
        for occurrence in occurrences:
            grouped_by_path[occurrence.path].append(occurrence)

        active_paths = []
        for key, value in grouped_by_path.items():
            latest_occurrence = max(value, key=lambda o: o.observed_at)
            active_paths.append(
                ActivePath(
                path=key,
                related_scan_ids={
            occurrence.scan_id
            for occurrence in value
        },
                latest_observed_at=latest_occurrence.observed_at
            ))

        return AssetProjection(
            asset_id=asset_id,
            active_paths=active_paths
        )
        



