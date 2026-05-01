from uuid import UUID
from pathlib import Path

class Occurrence:
    __slots__ = ("_occurrence_id", "_asset_id", "_path", "_scan_id")
    def __init__(
            self, occurrence_id: UUID,
            asset_id: UUID, path: Path,
            scan_id: UUID
    ) -> None:
        if not isinstance(occurrence_id, UUID):
            raise TypeError("occurrence_id must be an instance of UUID")
        if not isinstance(asset_id, UUID):
            raise TypeError("asset_id must be an instance of UUID")
        if not isinstance(path, Path):
            raise TypeError("path must be an instance of Path")
        if not isinstance(scan_id, UUID):
            raise TypeError("scan_id must be an instance of UUID")

        self._occurrence_id = occurrence_id
        self._asset_id = asset_id
        self._path = path
        self._scan_id = scan_id

    def __repr__(self) -> str:
        return(
            "Occurrence("
            f"id={self._occurrence_id}, "
            f"asset_id={self._asset_id}, "
            f"path={self._path}, "
            f"scan_id={self._scan_id})"
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