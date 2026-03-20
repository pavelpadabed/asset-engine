import sqlite3
from uuid import UUID
from domain.asset import Asset
from storage.repositories.asset_repository import AssetRepository
from storage.mappers.asset_mapper import AssetMapper

class SqliteAssetRepository(AssetRepository):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

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

    def list(self) -> list[Asset]:
        rows = self.connection.execute(
            "SELECT * FROM assets"
        ).fetchall()

        return [AssetMapper.from_row(row) for row in rows]


