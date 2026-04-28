import sqlite3
from uuid import uuid4
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
        with open("storage/sqlite/schema.sql") as f:
            self.connection.executescript(f.read())


    def save(self, asset: Asset):
        row = AssetMapper.to_row(asset)
        existing_asset = self.search_by_hash(asset.file_hash)
        if existing_asset:
            asset_id = existing_asset.id
        else:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO assets("
                    "asset_id, path, asset_type, file_hash,"
                    "source, file_size, modified_time"
                    ") VALUES(?,?,?,?,?,?,?)",
                    (
                        row["asset_id"],
                        row["path"],
                        row["asset_type"],
                        row["file_hash"],
                        row["source"],
                        row["file_size"],
                        row["modified_time"],
                    )
                )
            asset_id = row["asset_id"]
        occurrence_id = str(uuid4())
        scan_id = "test_scan"

        print("OCCURRENCE ASSET ID:", asset_id)

        self.connection.execute(
            "INSERT INTO occurrences(occurrence_id, asset_id, path, scan_id) "
            "VALUES(?,?,?,?)",
            (
                occurrence_id,
                str(asset_id),
                row["path"],
                scan_id
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
    # TODO (storage design): revisit duplicate handling strategy
    # Current behavior:
    # - Every scan persists ALL files (including duplicates)
    # - DB grows linearly (e.g. 38 → 76 after second scan)
    # - No uniqueness constraint on file_hash
    #
    # Problem:
    # - DeduplicateService works on DB → sees "duplicates" across scans
    # - After multiple scans, DB contains repeated entries → misleading results
    #   (e.g. reports 38 duplicates instead of real 1)
    #
    # Important:
    # - Adding UNIQUE(file_hash) is NOT acceptable
    #   → it removes information about duplicate occurrences
    #
    # Options to consider:
    # A) Keep current append-only model (MVP, simple, but grows DB)
    # B) Introduce normalized schema:
    #     - assets (unique by hash)
    #     - occurrences (each file instance / scan)
    # C) Track scan_id / source to distinguish scan sessions
    #
    # Goal:
    # - Preserve real duplicate semantics
    # - Keep DeduplicateService correct
    # - Avoid DB pollution across repeated scans


