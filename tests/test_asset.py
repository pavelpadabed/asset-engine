from uuid import UUID
from domain.asset import Asset
from domain.state import AssetState
from domain.source import Source, SourceEnum
from domain.types import AssetType
from tests.helpers.make_asset import make_asset
import pytest

def test_asset_creation_raw():
    asset = make_asset()
    assert asset.state.value == AssetState.RAW
    assert isinstance(asset.id, UUID)



def test_file_hash_must_be_value_object():
    type_= AssetType.image()
    source = Source(SourceEnum.API)
    file_hash = "b" * 64
    with pytest.raises(TypeError):
        Asset(asset_type=type_, source=source, file_hash=file_hash)