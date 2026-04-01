from typing import Iterable, Iterator
from datetime import datetime

from storage.repositories.asset_repository import AssetRepository
from domain.asset import Asset
from application.criteria.asset_search_criteria import AssetSearchCriteria

class SearchService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def _matches_ext(self, asset: Asset, normalized_ext: str | None) -> bool:
        if normalized_ext is None:
            return True

        ext = asset.path.suffix.lstrip(".").lower()

        return ext == normalized_ext

    def _matches_name(
            self, asset: Asset,
            normalized_name: str | None
    ) -> bool:
        if normalized_name is None:
            return True
        asset_name = asset.path.stem.lower()

        return normalized_name in asset_name

    def _matches_time(
            self, asset: Asset,
            modified_before: datetime | None,
            modified_after: datetime | None
    ) -> bool:
        asset_time = asset.metadata.modified_time
        return (
            (modified_after is None or asset_time >= modified_after)
            and (modified_before is None or asset_time <= modified_before)
        )

    def _matches_size(
            self, asset: Asset,
            min_size: int | None,
            max_size: int | None
    ) -> bool:
        asset_size = asset.metadata.size

        return(
            (min_size is None or asset_size >= min_size)
            and (max_size is None or asset_size <= max_size)
        )



    def search(self, criteria: AssetSearchCriteria) -> Iterator[Asset]:
        normalized_ext = criteria.extension.lower() if criteria.extension else None
        normalized_name = criteria.name_contains.lower() if criteria.name_contains else None
        modified_after = criteria.modified_after
        modified_before = criteria.modified_before
        min_size = criteria.min_size
        max_size = criteria.max_size

        filters = []

        if normalized_ext is not None:
            filters.append(lambda asset: self._matches_ext(asset, normalized_ext))
        if normalized_name is not None:
            filters.append(lambda asset: self._matches_name(asset, normalized_name))
        if modified_after is not None or modified_before is not None:
            filters.append(
                lambda asset: self._matches_time(asset, modified_after, modified_before)
            )
        if min_size is not None or max_size is not None:
            filters.append(
                lambda asset: self._matches_size(asset, min_size, max_size)
            )

        for asset in self.repository.list():
            if not all(filter(asset) for filter in filters):
                continue
            yield asset

    # TODO: add support for tag-based search
    # e.g. search by tag: "interview", "report", etc.




