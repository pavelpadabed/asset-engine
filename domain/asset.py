from uuid import uuid4, UUID
from domain.types import Type
from domain.source import Source
from domain.state import State
from domain.tag import Tag
from domain.hash import FileHash

class Asset:
    __slots__ = ("_type", "_source", "_id", "_state", "_metadata", "_tags", "_hash")
    def __init__(
            self, type: Type,
            source: Source,
            file_hash: FileHash,
            metadata: dict | None = None,
            tags: set[Tag] | None = None,

    ) -> None:
        if not isinstance(type, Type):
            raise TypeError("type must be an instance of Type")
        if not isinstance(source, Source):
            raise TypeError("source must be an instance Source")
        if not isinstance(file_hash, FileHash):
            raise TypeError("file_hash must be an instance of FileHash")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a dict or None")
        self._type = type
        self._source = source
        self._id = uuid4()
        self._state = State.raw()
        self._hash = file_hash
        self._metadata = metadata.copy() if metadata else {}
        self._tags = set(tags) if tags else set()
        self._hash = file_hash

    def __repr__(self) -> str:
        return (
            f"Asset(id={self._id}, type={self._type}, "
            f"source={self._source}, state={self._state})"
        )

    @property
    def type(self) -> "Type":
        return self._type

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
    def metadata(self) -> dict:
        return self._metadata.copy()

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

    def remove_tag(self, tag) -> None:
        if not isinstance(tag, Tag):
            raise TypeError("tag must be an instance of Tag")
        self._tags.discard(tag)

