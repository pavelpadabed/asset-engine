import sqlite3
from uuid import UUID
from typing import Iterator
from enum import Enum

from domain.hash import FileHash
from domain.asset import Asset
from domain.occurrence import Occurrence
from storage.repositories.asset_repository import AssetRepository
from storage.mappers.asset_mapper import AssetMapper
from storage.mappers.occurrence_mapper import OccurrenceMapper


class AssetSaveStatus(Enum):
    NEW = "new"
    ALREADY_INDEXED = "already indexed"


class SqliteAssetRepository(AssetRepository):
    def __init__(self, connection: sqlite3.Connection) -> None:
        connection.row_factory = sqlite3.Row
        self.connection = connection
        self._create_tables()

    def _create_tables(self) -> None:
        with open("storage/sqlite/schema.sql") as f:
            self.connection.executescript(f.read())


    def save(self, asset: Asset, occurrence: Occurrence) -> AssetSaveStatus:
        asset_row = AssetMapper.to_row(asset)
        occurrence_row = OccurrenceMapper.to_row(occurrence)
        existing_asset = self.search_by_hash(asset.file_hash)
        if existing_asset:
            asset_id = existing_asset.id
        else:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO assets("
                    "asset_id,asset_type, file_hash,"
                    "source, file_size, modified_time"
                    ") VALUES(?,?,?,?,?,?,?)",
                    (
                        asset_row["asset_id"],
                        asset_row["asset_type"],
                        asset_row["file_hash"],
                        asset_row["source"],
                        asset_row["file_size"],
                        asset_row["modified_time"],
                    )
                )
            asset_id = asset_row["asset_id"]

        self.connection.execute(
            "INSERT INTO occurrences(occurrence_id, asset_id, path, scan_id) "
            "VALUES(?,?,?,?)",
            (
                occurrence_row["occurrence_id"],
                str(asset_id),
                occurrence_row["path"],
                occurrence_row["scan_id"]
            )
        )

        status = (
            AssetSaveStatus.ALREADY_INDEXED
            if existing_asset else AssetSaveStatus.NEW
        )

        return status


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

    def iterate_assets_with_occurrences(self) -> Iterator[tuple[Asset, list[Occurrence]]]:
        grouped_by_ids = {}
        for row in self.connection.execute(
            """
            SELECT
                a.asset_id,
                a.asset_type,
                a.file_hash,
                a.source,
                a.file_size,
                a.modified_time,
                
                o.occurrence_id,
                o.path,
                o.scan_id
            FROM occurrences o
            JOIN assets a ON o.asset_id = a.asset_id
            """
        ):
            asset_id = row["asset_id"]
            occurrence = OccurrenceMapper.from_row(row)

            if asset_id not in grouped_by_ids:
                grouped_by_ids[asset_id] = (
                    AssetMapper.from_row(row),
                    [occurrence]
                )
            else:
                grouped_by_ids[asset_id][1].append(occurrence)

        for value in grouped_by_ids.values():
            yield (value[0], value[1])



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


