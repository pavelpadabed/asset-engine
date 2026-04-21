from typing import Protocol, Iterable, Iterator
from uuid import UUID
from datetime import datetime
from domain.asset import Asset
from domain.hash import FileHash
from domain.tag import Tag

class AssetRepository(Protocol):
    def save(self, asset: Asset) -> None:...

    def get(self, asset_id: UUID) -> None:...

    def iterate(self) -> Iterator[Asset]:...

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
