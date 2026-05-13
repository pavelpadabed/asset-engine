from uuid import UUID

from tests.helpers.make_asset import make_asset
from tests.helpers.make_occurrence import make_occurrence


def test_occurrence_creation():
    asset = make_asset()
    size = 500
    occurrence = make_occurrence(name="test.mp4",asset_id=asset.id, file_size=size)
    assert occurrence.asset_id == asset.id
    assert isinstance(occurrence.id, UUID)
    assert isinstance(occurrence.scan_id, UUID)
    assert occurrence.file_size == 500
