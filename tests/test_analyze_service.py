from uuid import uuid4

from tests.helpers.make_asset import make_asset
from tests.helpers.make_occurrence import make_occurrence
from application.projections.asset_projection import AssetProjection
from application.services.duplicate_service import DuplicateService

def test_returns_re_observed():
    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id)
    occ_b = make_occurrence("report.txt", asset.id)

    asset_group = (asset, [occ_a, occ_b])

    projection = AssetProjection.from_occurrences(asset_group)

    result = DuplicateService().analyze(projection)

    assert result.outcome == "re_observed"

def test_returns_strong_duplicate_candidate():
    scan_id = uuid4()
    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id, scan_id)
    occ_b = make_occurrence("report_copy.txt", asset.id, scan_id)

    asset_group = (asset, [occ_a, occ_b])
    projection = AssetProjection.from_occurrences(asset_group)

    result = DuplicateService().analyze(projection)

    assert result.outcome == "strong_duplicate_candidate"

def test_returns_possible_moved():
    scan_id_1 = uuid4()
    scan_id_2 = uuid4()

    asset = make_asset()
    occ_a = make_occurrence("report.txt", asset.id, scan_id_1)
    occ_b = make_occurrence("report_copy.txt", asset.id, scan_id_2)

    asset_group = (asset, [occ_a, occ_b])
    projection = AssetProjection.from_occurrences(asset_group)

    result = DuplicateService().analyze(projection)

    assert result.outcome == "possible_moved"






