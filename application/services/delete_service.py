from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository

class DeleteService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def delete_assets(self, assets: list[Asset]) -> None:
        for asset in assets:
            asset.path.unlink(missing_ok=True)
            self.repository.delete(asset.id)

    # TODO (refactor): improve deletion robustness
    # - handle database errors (try/except)
    # - ensure consistency between filesystem and database
    # - consider transaction or rollback strategy
    # - add logging for failed deletions