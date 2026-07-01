from tests.helpers.make_asset import make_asset
from tests.helpers.make_occurrence import make_occurrence
from application.projections.asset_projection import AssetProjection
from uuid import uuid4


def test_groups_occurrences_by_path():
    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id)
    occ_b = make_occurrence("report.txt", asset.id)
    occ_c = make_occurrence("report.pdf", asset.id)

    asset_group = (asset, [occ_a, occ_b, occ_c])

    projection = AssetProjection.from_occurrences(asset_group)

    assert projection.asset_id == asset.id
    assert len(projection.active_paths) == 2


def test_creates_path_observations():
    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id)
    occ_b = make_occurrence("report.txt", asset.id)
    occ_c = make_occurrence("report.pdf", asset.id)

    asset_group = (asset, [occ_a, occ_b, occ_c])

    projection = AssetProjection.from_occurrences(asset_group)

    paths = projection.active_paths

    assert sum([
        len(path.observations)
         for path in paths
        ]) == 3

def test_related_scan_ids():
    scan_1 = uuid4()
    scan_2 = uuid4()
    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id, scan_1)
    occ_b = make_occurrence("report.txt", asset.id, scan_1)
    occ_c = make_occurrence("report.txt", asset.id, scan_2)

    asset_group = (asset, [occ_a, occ_b, occ_c])

    projection = AssetProjection.from_occurrences(asset_group)

    paths = projection.active_paths

    for path in paths:
        assert len(path.related_scan_ids) == 2
        assert path.related_scan_ids == {scan_1, scan_2}

