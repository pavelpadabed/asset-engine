from collections import defaultdict

from storage.sqlite.sqlite_asset_repository import SqliteAssetRepository
from domain.asset import Asset

class DuplicateService:
    def __init__(
            self,
            repository: SqliteAssetRepository
    ) -> None:
        self.repository = repository

    def detect_duplicates(self) -> list[list[Asset]]:
        duplicates = defaultdict(list)
        for asset in self.repository.iterate():
            duplicates[asset.file_hash].append(asset)

        return [d for d in duplicates.values() if len(d) > 1]
