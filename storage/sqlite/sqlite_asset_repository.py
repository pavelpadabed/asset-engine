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
        cursor = self.connection.cursor()
        cursor.execute(
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
        self.connection.commit()

    def get(self, asset_id: UUID) -> Asset | None:
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM assets WHERE asset_id = ?",
            (str(asset_id),))

        row = cursor.fetchone()

        if row is None:
            return None

        return AssetMapper.from_row(row)



