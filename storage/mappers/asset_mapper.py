from pathlib import Path
from uuid import UUID
from domain.asset import Asset
from domain.source import Source
from domain.types import AssetType
from domain.hash import FileHash

class AssetMapper:
    @staticmethod
    def to_row(asset: Asset) -> dict:
        return {
            "asset_id": str(asset.id),
            "path": str(asset.path),
            "asset_type": asset.asset_type.value,
            "file_hash": asset.file_hash.value,
            "source": asset.source.value
        }

    @staticmethod
    def from_row(row: dict[str, object]) -> Asset:
        return Asset(
            id=UUID(row["asset_id"]),
            path=Path(row["path"]),
            assset_type=AssetType(row["asset_type"]),
            source=Source(row["source"]),
            file_hash=FileHash(row["file_hash"])
        )