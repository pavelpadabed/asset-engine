from enum import Enum
from dataclasses import dataclass
from domain.exceptions import InvalidTransitionError

class AssetState(Enum):
    RAW = "raw"
    NORMALIZED = "normalized"
    EXPORTED = "exported"
    FAILED = "failed"


ALLOWED_TRANSITIONS = {
    AssetState.RAW: {
        AssetState.NORMALIZED,
        AssetState.FAILED
    },
    AssetState.NORMALIZED: {
        AssetState.EXPORTED,
        AssetState.FAILED
    },
    AssetState.EXPORTED: set(),
    AssetState.FAILED: set()
}


@dataclass(frozen=True)
class State:
    value: AssetState

    @classmethod
    def raw(cls) -> "State":
        return cls(AssetState.RAW)

    @classmethod
    def normalized(cls) -> "State":
        return cls(AssetState.NORMALIZED)

    @classmethod
    def exported(cls) -> "State":
        return cls(AssetState.EXPORTED)

    @classmethod
    def failed(cls) -> "State":
        return cls(AssetState.FAILED)

    def can_transition_to(self, target: "State") -> bool:
        return target.value in ALLOWED_TRANSITIONS[self.value]

    def transition_to(self, target: "State") -> "State":
        if not self.can_transition_to(target):
            raise InvalidTransitionError(
                f"Invalid transition from {self.value} to {target}"
            )
        return target