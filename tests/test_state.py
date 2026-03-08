from domain.state import State, AssetState
from domain.exceptions import InvalidTransitionError
import pytest

def test_raw_factory():
    state = State.raw()
    assert state.value == AssetState.RAW


def test_can_transition_to_norm():
    raw = State.raw()
    normalized = State.normalized()
    assert raw.can_transition_to(normalized)


def test_cannot_trans_to_exported():
    raw = State.raw()
    exported = State.exported()
    assert not raw.can_transition_to(exported)


def test_raw_trans_to_exported_raises():
    raw = State.raw()
    exported = State.exported()

    with pytest.raises(InvalidTransitionError):
        raw.transition_to(exported)