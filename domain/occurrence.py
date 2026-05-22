from uuid import UUID
from pathlib import Path
from datetime import datetime

class Occurrence:
    __slots__ = (
        "_occurrence_id", "_asset_id", "_path", "_scan_id", "_observed_at",
        "_file_size", "_modified_time"
    )
    def __init__(
            self, occurrence_id: UUID,
            asset_id: UUID, path: Path,
            scan_id: UUID, observed_at: datetime, file_size: int, modified_time: datetime,
    ) -> None:
        if not isinstance(occurrence_id, UUID):
            raise TypeError("occurrence_id must be an instance of UUID")
        if not isinstance(asset_id, UUID):
            raise TypeError("asset_id must be an instance of UUID")
        if not isinstance(path, Path):
            raise TypeError("path must be an instance of Path")
        if not isinstance(scan_id, UUID):
            raise TypeError("scan_id must be an instance of UUID")
        if not isinstance(observed_at, datetime):
            raise TypeError("observed_at must be an instance of datetime")
        if not isinstance(file_size, int):
            raise TypeError("file_size must be integer")
        if not isinstance(modified_time, datetime):
            raise TypeError("modified_time must be an instance of datetime")

        self._occurrence_id = occurrence_id
        self._asset_id = asset_id
        self._path = path
        self._scan_id = scan_id
        self._observed_at = observed_at
        self._file_size = file_size
        self._modified_time = modified_time

    def __repr__(self) -> str:
        return(
            "Occurrence("
            f"id={self._occurrence_id}, "
            f"asset_id={self._asset_id}, "
            f"path={self._path}, "
            f"scan_id={self._scan_id}, "
            f"observed_at={self._observed_at}, "
            f"size={self._file_size}, "
            f"modified_time={self._modified_time})"
        )

    @property
    def occurrence_id(self) -> UUID:
        return self._occurrence_id

    @property
    def id(self) -> UUID:
        return self._occurrence_id

    @property
    def asset_id(self) -> UUID:
        return self._asset_id

    @property
    def path(self) -> Path:
        return self._path

    @property
    def scan_id(self) -> UUID:
        return self._scan_id

    @property
    def observed_at(self) -> datetime:
        return self._observed_at

    @property
    def file_size(self) -> int:
        return self._file_size

    @property
    def modified_time(self) -> datetime:
        return self._modified_time

