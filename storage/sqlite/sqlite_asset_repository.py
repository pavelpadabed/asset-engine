import sqlite3
from uuid import UUID
from typing import Iterator

from domain.hash import FileHash
from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository
from storage.mappers.asset_mapper import AssetMapper

class SqliteAssetRepository(AssetRepository):
    def __init__(self, connection: sqlite3.Connection) -> None:
        connection.row_factory = sqlite3.Row
        self.connection = connection
        self._create_tables()

    def _create_tables(self) -> None:
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS assets(
            asset_id TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            source TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            modified_time TEXT NOT NULL
            )
        """)

        self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_assets_file_hash
            ON assets(file_hash)
        """)

    def save(self, asset: Asset):
        row = AssetMapper.to_row(asset)
        with self.connection:
            self.connection.execute(
            "INSERT INTO assets(asset_id, path, asset_type, file_hash, "
            "source, file_size, modified_time) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            (row["asset_id"],
             row["path"],
             row["asset_type"],
             row["file_hash"],
             row["source"],
             row["file_size"],
             row["modified_time"]

            )
        )

    def get(self, asset_id: UUID) -> Asset | None:
        row = self.connection.execute(
            "SELECT * FROM assets WHERE asset_id = ?",
            (str(asset_id),)
        ).fetchone()

        if row is None:
            return None

        return AssetMapper.from_row(row)

    def delete(self, asset_id: UUID) -> None:
        with self.connection:
            self.connection.execute(
                "DELETE FROM assets WHERE asset_id = ?",
                (str(asset_id),)
            )

    def iterate(self) -> Iterator[Asset]:
        for row in self.connection.execute(
            "SELECT * FROM assets"
        ):
            yield AssetMapper.from_row(row)

    def list(self) -> list[Asset]:
        return list(self.iterate())

    def search_by_hash(self, file_hash: FileHash) -> Asset | None:
        with self.connection:
            row = self.connection.execute(
                "SELECT * FROM assets WHERE file_hash = ?",
                (file_hash.value,)
            ).fetchone()
            return AssetMapper.from_row(row) if row is not None else None

    # TODO: add tags table and relation (many-to-many)
    # asset_id ↔ tag


