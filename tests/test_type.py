from domain.types import Type, AssetType
from dataclasses import FrozenInstanceError
import pytest


def test_type_factory():
    image = Type(AssetType.VIDEO)
    assert image.value == AssetType.VIDEO

def test_is_immutable():
    video = Type(AssetType.VIDEO)

    with pytest.raises(FrozenInstanceError):
        video.value = AssetType.IMAGE
