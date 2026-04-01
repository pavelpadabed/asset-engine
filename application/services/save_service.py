from typing import Iterable

from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository

class SaveService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def persist(self, assets: Iterable[Asset]) -> int:
        count = 0

        for asset in assets:
            self.repository.save(asset)
            count += 1

        return count