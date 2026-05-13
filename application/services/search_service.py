from typing import Iterator
from datetime import datetime

from storage.repositories.asset_repository import AssetRepository
from domain.asset import Asset
from domain.occurrence import Occurrence
from application.criteria.occurrence_search_criteria import OccurrenceSearchCriteria

class SearchService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def _matches_ext(
            self, occurrence: Occurrence,
            normalized_ext: str | None
    ) -> bool:
        if normalized_ext is None:
            return True

        ext = occurrence.path.suffix.lstrip(".").lower()

        return ext == normalized_ext

    def _matches_name(
            self, occurrence: Occurrence,
            normalized_name: str | None
    ) -> bool:
        if normalized_name is None:
            return True
        occurrence_name = occurrence.path.stem.lower()

        return normalized_name in occurrence_name

    def _matches_time(
            self, occurrence: Occurrence,
            modified_before: datetime | None,
            modified_after: datetime | None
    ) -> bool:
        occurrence_time = occurrence.modified_time
        return (
            (modified_after is None or occurrence_time >= modified_after)
            and (modified_before is None or occurrence_time <= modified_before)
        )

    def _matches_size(
            self, occurrence: Occurrence,
            min_size: int | None,
            max_size: int | None
    ) -> bool:
        occurrence_size = occurrence.file_size

        return(
            (min_size is None or occurrence_size >= min_size)
            and (max_size is None or occurrence_size <= max_size)
        )



    def search(self, criteria: OccurrenceSearchCriteria) -> Iterator[Occurrence]:
        normalized_ext = criteria.extension.lower() if criteria.extension else None
        normalized_name = criteria.name_contains.lower() if criteria.name_contains else None
        modified_after = criteria.modified_after
        modified_before = criteria.modified_before
        min_size = criteria.min_size
        max_size = criteria.max_size

        filters = []

        if normalized_ext is not None:
            filters.append(lambda occurrence: self._matches_ext(occurrence, normalized_ext))
        if normalized_name is not None:
            filters.append(lambda occurrence: self._matches_name(occurrence, normalized_name))
        if modified_after is not None or modified_before is not None:
            filters.append(
                lambda occurrence: self._matches_time(occurrence, modified_after, modified_before)
            )
        if min_size is not None or max_size is not None:
            filters.append(
                lambda occurrence: self._matches_size(occurrence, min_size, max_size)
            )

        for occurrence in self.repository.list_occurrences():
            if not all(filter(occurrence) for filter in filters):
                continue
            yield occurrence

    # TODO: add support for tag-based search
    # e.g. search by tag: "interview", "report", etc.




