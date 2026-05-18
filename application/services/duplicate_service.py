from storage.repositories.asset_repository import AssetRepository
from domain.asset import Asset
from domain.occurrence import Occurrence

class DuplicateService:
    def __init__(
            self,
            repository: AssetRepository
    ) -> None:
        self.repository = repository

    def detect_duplicates(self) -> list[tuple[Asset,list[Occurrence]]]:
        return [
            (asset, occurrences)
            for asset, occurrences in
            self.repository.iterate_assets_with_occurrences()
            if len(occurrences) > 1
        ]
