from uuid import UUID
from domain.asset import Asset
from domain.state import State, AssetState
from domain.source import Source, SourceEnum
from domain.types import Type, AssetType

def test_asset_creation_raw():
    type_ = Type(AssetType.IMAGE)
    source = Source(SourceEnum.FILESYSTEM)
    asset = Asset(type=type_, source=source)
    assert asset.state.value == AssetState.RAW
    assert isinstance(asset.id, UUID)
    assert asset.metadata == {}

def test_metadata_is_safe():
    type_ = Type(AssetType.VIDEO)
    source = Source(SourceEnum.FILESYSTEM)
    meta = {"x": 1}
    asset = Asset(type=type_, source=source, metadata=meta)
    meta["x"] = 13
    assert asset.metadata["x"] == 1

def test_metadata_from_property_is_safe():
    type_ = Type(AssetType.IMAGE)
    source = Source(SourceEnum.API)
    asset = Asset(type=type_, source=source, metadata={"x": 1})
    data = asset.metadata
    data["x"] = 34
    assert asset.metadata["x"] == 1