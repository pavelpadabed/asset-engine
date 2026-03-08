from uuid import uuid4, UUID
from domain.types import Type
from domain.source import Source
from domain.state import State

class Asset:
    __slots__ = ("_type", "_source", "_id", "_state", "_metadata")
    def __init__(
            self, type: Type,
            source: Source,
            metadata: dict | None = None
    ) -> None:
        if not isinstance(type, Type):
            raise TypeError("type must be an instance of Type")
        if not isinstance(source, Source):
            raise TypeError("source must be an instance Source")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a dict or None")
        self._type = type
        self._source = source
        self._id = uuid4()
        self._state = State.raw()
        self._metadata = metadata.copy() if metadata else {}

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

    def _change_state(self, target: State) -> None:
        self._state = self._state.transition_to(target)

    def mark_normalized(self) -> None:
        self._change_state(State.normalized())

    def mark_exported(self) -> None:
        self._change_state(State.exported())

    def mark_failed(self) -> None:
        self._change_state(State.failed())
