from domain.types import TypeEnum, AssetType
from dataclasses import FrozenInstanceError
import pytest


def test_type_factory():
    image = AssetType.image()
    assert image == AssetType.image()

def test_is_immutable():
    video = AssetType.video()

    with pytest.raises(FrozenInstanceError):
        video.kind = TypeEnum.IMAGE
