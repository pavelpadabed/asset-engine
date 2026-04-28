from domain.asset import Asset
from domain.types import AssetType
from domain.source import Source
from domain.hash import FileHash
from domain.metadata import FileMetadata

from uuid import uuid4
from pathlib import Path
from datetime import datetime
from typing import Any

def make_asset(
        name: str, file_hash: Any | None = None,
        size: int | None = None
) -> Asset:
    path = Path("/tmp") / name

    return Asset (
        id=uuid4(),
        path=path,
        asset_type=AssetType.image(),
        file_hash=FileHash(file_hash if file_hash is not None else "a" * 64),
        source=Source.filesystem(Path("local")),
        metadata=FileMetadata(
            size=size if size is not None else 123,
            modified_time=datetime.now()
        )
    )