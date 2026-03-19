from uuid import uuid4, UUID
from pathlib import Path
from domain.types import AssetType
from domain.source import Source
from domain.state import State
from domain.tag import Tag
from domain.hash import FileHash
from domain.metadata import FileMetadata

class Asset:
    __slots__ = ("_path","_asset_type", "_source", "_id", "_state", "_metadata", "_tags", "_hash")
    def __init__(
            self, path: Path,
            asset_type: AssetType,
            source: Source,
            file_hash: FileHash,
            id: UUID | None = None,
            metadata: FileMetadata | None = None,
            tags: set[Tag] | None = None,
    ) -> None:
        if not isinstance(path, Path):
            raise TypeError("path must be an instance Path")
        if not isinstance(asset_type, AssetType):
            raise TypeError("type must be an instance of AssetType")
        if not isinstance(source, Source):
            raise TypeError("source must be an instance Source")
        if not isinstance(file_hash, FileHash):
            raise TypeError("file_hash must be an instance of FileHash")
        if metadata is not None and not isinstance(metadata, FileMetadata):
            raise TypeError("metadata must be FileMetadata")
        self._path = path
        self._asset_type = asset_type
        self._source = source
        self._id = id if id is not None else uuid4()
        self._state = State.raw()
        self._hash = file_hash
        self._metadata = metadata
        self._tags = set(tags) if tags else set()

    def __repr__(self) -> str:
        return (
            f"Asset(id={self._id}, type={self._asset_type}, "
            f"source={self._source}, state={self._state})"
        )

    @property
    def path(self) -> Path:
        return self._path

    @property
    def asset_type(self) -> "AssetType":
        return self._asset_type

    @property
    def source(self) -> "Source":
        return self._source

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def state(self) -> "State":
        return self._state

    @property
    def metadata(self) -> FileMetadata | None:
        return self._metadata

    @property
    def tags(self) -> set[Tag]:
        return set(self._tags)

    @property
    def file_hash(self) -> FileHash:
        return self._hash

    def _change_state(self, target: State) -> None:
        self._state = self._state.transition_to(target)

    def mark_normalized(self) -> None:
        self._change_state(State.normalized())

    def mark_exported(self) -> None:
        self._change_state(State.exported())

    def mark_failed(self) -> None:
        self._change_state(State.failed())

    def add_tag(self, tag: Tag) -> None:
        if not isinstance(tag, Tag):
            raise TypeError("tag must be an instance of Tag")
        self._tags.add(tag)

    def remove_tag(self, tag: Tag) -> None:
        if not isinstance(tag, Tag):
            raise TypeError("tag must be an instance of Tag")
        self._tags.discard(tag)

