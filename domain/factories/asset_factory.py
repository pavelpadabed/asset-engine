from domain.types import AssetType
from domain.source import Source
from domain.hash import FileHash
from domain.asset import Asset

class AssetFactory:
    @staticmethod
    def create(
            file_hash: FileHash,
            source: Source,
            asset_type: AssetType
    ) -> Asset:


        return Asset(
                asset_type=asset_type,
                source=source,
                file_hash=file_hash,
        )




