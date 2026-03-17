from pathlib import Path
from uuid import UUID
from datetime import datetime
from domain.asset import Asset
from domain.source import Source
from domain.types import AssetType
from domain.hash import FileHash
from domain.metadata import FileMetadata

FIELDS_MAP = {
    "asset_id": lambda a: str(a.id),
    "path": lambda a: str(a.path),
    "asset_type": lambda a: a.asset_type.value,
    "file_hash": lambda a: a.file_hash.value,
    "source": lambda a: a.source.value,
    "file_size": lambda a: a.metadata.size,
    "modified_time": lambda a: a.metadata.modified_time.isoformat()
}

REVERSE_FIELDS_MAP = {
    "asset_id": lambda r: UUID(r["asset_id"]),
    "path": lambda r: Path(r["path"]),
    "asset_type": lambda r: AssetType(r["asset_type"]),
    "file_hash": lambda r: FileHash(r["file_hash"]),
    "source": lambda r: Source(r["source"])
}

class AssetMapper:
    @staticmethod
    def to_row(asset: Asset) -> dict:
        return {
            key: extractor(asset)
            for key, extractor
            in FIELDS_MAP.items()
        }

    @staticmethod
    def from_row(row: dict[str, str | int]) -> Asset:
        size = row["file_size"]
        modified_time = datetime.fromisoformat(row['modified_time'])
        metadata = FileMetadata(size, modified_time)
        kwargs = {
            key: builder(row)
            for key, builder in REVERSE_FIELDS_MAP.items()
        }
        return Asset(**kwargs, metadata=metadata)
