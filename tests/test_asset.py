from uuid import UUID
from domain.asset import Asset
from domain.state import State, AssetState
from domain.source import Source, SourceEnum
from domain.types import AssetType, AssetType
from domain.hash import FileHash
from domain.metadata import FileMetadata
import pytest

valid_hash = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

def test_asset_creation_raw():
    type_ = AssetType.image()
    source = Source(SourceEnum.FILESYSTEM)
    file_hash = FileHash(valid_hash)
    asset = Asset(type=type_, source=source, file_hash=file_hash)
    assert asset.state.value == AssetState.RAW
    assert isinstance(asset.id, UUID)
    assert asset.metadata == None



def test_file_hash_must_be_value_object():
    type_= AssetType.image()
    source = Source(SourceEnum.API)
    with pytest.raises(TypeError):
        Asset(type=type_, source=source, file_hash="1562adf")