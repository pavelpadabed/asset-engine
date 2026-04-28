from enum import Enum

from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository

class AssetSaveStatus(Enum):
    NEW = "new"
    ALREADY_INDEXED = "already indexed"

class SaveService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def persist(self, asset: Asset) -> AssetSaveStatus:
        status = (
            AssetSaveStatus.ALREADY_INDEXED
            if self.repository.search_by_hash(asset.file_hash)
            else AssetSaveStatus.NEW
        )
        self.repository.save(asset)
        return status
