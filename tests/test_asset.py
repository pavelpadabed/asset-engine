from uuid import UUID
from domain.asset import Asset
from pathlib import Path
from domain.state import State, AssetState
from domain.source import Source, SourceEnum
from domain.types import AssetType
from domain.hash import FileHash
import pytest

def test_asset_creation_raw():
    type_ = AssetType.image()
    path = Path("/tmp/test.txt")
    source = Source(SourceEnum.FILESYSTEM)
    file_hash = FileHash("a" * 64)
    asset = Asset(path=path,asset_type=type_, source=source, file_hash=file_hash)
    assert asset.state.value == AssetState.RAW
    assert isinstance(asset.id, UUID)
    assert asset.metadata == None



def test_file_hash_must_be_value_object():
    type_= AssetType.image()
    source = Source(SourceEnum.API)
    file_hash = FileHash("b" * 64)
    with pytest.raises(TypeError):
        Asset(asset_type=type_, source=source, file_hash=file_hash)