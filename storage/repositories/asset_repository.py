from typing import Protocol, Iterable, Iterator
from uuid import UUID
from datetime import datetime
from domain.asset import Asset
from domain.hash import FileHash
from domain.tag import Tag

from storage.sqlite.sqlite_asset_repository import AssetSaveStatus

class AssetRepository(Protocol):
    def save(self, asset: Asset) -> AssetSaveStatus:...

    def get(self, asset_id: UUID) -> None:...

    def iterate(self) -> Iterator[Asset]:...

    def iterate_assets_with_occurrences(self) -> Iterator[tuple[Asset, list[Occurrence]]]:...

    def list(self) -> list[Asset]:...

    def delete(self, asset_id: UUID) -> None:...

    def search_by_hash(self, file_hash: FileHash) -> Asset | None:...

    def search_by_tag(self, tag: Tag) -> Iterable[Asset]:...

    def search_by_time(
        self,
        start: datetime,
        end: datetime
    )-> Iterable[Asset]:...

    # TODO: implement tag-based filtering (requires DB schema update)
