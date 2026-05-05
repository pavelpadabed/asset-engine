from uuid import UUID
from domain.asset import Asset
from domain.source import SourceEnum,Source
from domain.types import AssetType
from domain.hash import FileHash


FIELDS_MAP = {
    "asset_id": lambda a: str(a.id),
    "asset_type": lambda a: a.asset_type.kind.value,
    "file_hash": lambda a: a.file_hash.value,
    "source": lambda a: a.source.source_type.value,

}

REVERSE_FIELDS_MAP = {
    "id": lambda r: UUID(r["asset_id"]),
    "asset_type": lambda r: AssetType(r["asset_type"]),
    "file_hash": lambda r: FileHash(r["file_hash"]),
    "source": lambda r: Source(SourceEnum(r["source"]))
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
        kwargs = {
            key: builder(row)
            for key, builder in REVERSE_FIELDS_MAP.items()
        }
        return Asset(**kwargs)
