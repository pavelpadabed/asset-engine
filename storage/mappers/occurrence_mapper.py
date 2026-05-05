from uuid import UUID
from pathlib import Path
import datetime as dt

from domain.occurrence import Occurrence

FIELDS_MAP = {
    "occurrence_id": lambda o: str(o.id),
    "asset_id": lambda o: str(o.asset_id),
    "path": lambda o: str(o.path),
    "scan_id": lambda o: str(o.scan_id),
    "file_size": lambda o: int(o.file_size),
    "modified_time": lambda o: o.modified_time.isoformat()
}

REVERSE_FIELDS_MAP = {
    "occurrence_id": lambda r: UUID(r["occurrence_id"]),
    "asset_id": lambda r: UUID(r["asset_id"]),
    "path": lambda r: Path(r["path"]),
    "scan_id": lambda r: UUID(r["scan_id"]),
    "file_size": lambda r: int(r["file_size"]),
    "modified_time": lambda r: dt.datetime.fromisoformat(r["modified_time"])
}

class OccurrenceMapper:
    @staticmethod
    def to_row(occurrence: Occurrence) -> dict:
        return {
            key: extractor(occurrence)
            for key, extractor
            in FIELDS_MAP.items()
        }

    @staticmethod
    def from_row(row: dict[str, str | int]) -> Occurrence:
        kwargs = {
            key: builder(row)
            for key, builder in REVERSE_FIELDS_MAP.items()
        }
        return Occurrence(**kwargs)