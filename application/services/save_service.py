from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository
from storage.sqlite.sqlite_asset_repository import AssetSaveStatus



class SaveService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def persist(self, asset: Asset) -> AssetSaveStatus:
        return self.repository.save(asset)