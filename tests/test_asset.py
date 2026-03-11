from uuid import UUID
from domain.asset import Asset
from domain.state import State, AssetState
from domain.source import Source, SourceEnum
from domain.types import Type, AssetType
from domain.hash import FileHash
import pytest

valid_hash = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

def test_asset_creation_raw():
    type_ = Type(AssetType.IMAGE)
    source = Source(SourceEnum.FILESYSTEM)
    file_hash = FileHash(valid_hash)
    asset = Asset(type=type_, source=source, file_hash=file_hash)
    assert asset.state.value == AssetState.RAW
    assert isinstance(asset.id, UUID)
    assert asset.metadata == {}

def test_metadata_is_safe():
    type_ = Type(AssetType.VIDEO)
    source = Source(SourceEnum.FILESYSTEM)
    file_hash = FileHash(valid_hash)
    meta = {"x": 1}
    asset = Asset(type=type_, source=source, file_hash=file_hash, metadata=meta)
    meta["x"] = 13
    assert asset.metadata["x"] == 1

def test_metadata_from_property_is_safe():
    type_ = Type(AssetType.IMAGE)
    source = Source(SourceEnum.API)
    file_hash = FileHash(valid_hash)
    asset = Asset(type=type_, source=source, file_hash=file_hash, metadata={"x": 1})
    data = asset.metadata
    data["x"] = 34
    assert asset.metadata["x"] == 1


def test_file_hash_must_be_value_object():
    type_= Type(AssetType.IMAGE)
    source = Source(SourceEnum.API)
    with pytest.raises(TypeError):
        Asset(type=type_, source=source, file_hash="1562adf")