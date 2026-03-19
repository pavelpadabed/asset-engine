import sqlite3
from uuid import uuid4
from pathlib import Path
from datetime import datetime

from domain.asset import Asset
from domain.types import AssetType
from domain.source import Source
from domain.hash import FileHash
from domain.metadata import FileMetadata
from storage.sqlite.sqlite_asset_repository import SqliteAssetRepository

def test_save_asset():
    conn = sqlite3.connect(":memory:")

    with open("storage/sqlite/schema.sql") as f:
        conn.executescript(f.read())

    repo = SqliteAssetRepository(conn)

    asset = Asset(
        id=uuid4(),
        path=Path("/tmp/test.txt"),
        asset_type=AssetType.image(),
        file_hash=FileHash("a" * 64),
        source=Source.filesystem("local"),
        metadata=FileMetadata(
            size=123,
            modified_time=datetime.now()
        )
    )

    repo.save(asset)

    rows = conn.execute("SELECT * FROM assets").fetchall()

    assert len(rows) == 1


def test_get_asset():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    with open("storage/sqlite/schema.sql") as f:
        conn.executescript(f.read())

    repo = SqliteAssetRepository(conn)

    asset = Asset(
        id=uuid4(),
        path=Path("/tmp/test.txt"),
        asset_type=AssetType.image(),
        file_hash=FileHash("a" * 64),
        source=Source.filesystem("local"),
        metadata=FileMetadata(
            size=123,
            modified_time=datetime.now()
        )
    )

    repo.save(asset)

    result = repo.get(asset.id)

    assert result is not None
    assert isinstance(result, Asset)
    assert result.id == asset.id