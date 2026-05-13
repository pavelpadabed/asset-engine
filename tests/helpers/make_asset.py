from domain.asset import Asset
from domain.types import AssetType
from domain.source import Source
from domain.hash import FileHash

from uuid import uuid4
from pathlib import Path


def make_asset(
         file_hash: FileHash | None = None,
        asset_type: AssetType | None = None
) -> Asset:

    return Asset (
        id=uuid4(),
        asset_type=asset_type if asset_type is not None else AssetType.image(),
        file_hash=FileHash(file_hash if file_hash is not None else "a" * 64),
        source=Source.filesystem(Path("local")),

    )