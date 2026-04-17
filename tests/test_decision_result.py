from tests.helpers.make_asset import make_asset
from application.dto.deduplicate_result import GroupDecision, DecisionResult

def test_total_files_returns_correct_count():
    asset_1 = make_asset("test.txt")
    asset_2 = make_asset("report.pdf")
    asset_3 = make_asset("video.mp4")

    group = GroupDecision(
        to_keep=asset_1,
        to_delete=[asset_2, asset_3]
    )

    result = DecisionResult(
        groups=[group]
    )

    assert result.total_files == 3

def test_total_files_to_delete_returns_correct_count():
    asset_1 = make_asset("test.txt")
    asset_2 = make_asset("report.pdf")
    asset_3 = make_asset("video.mp4")

    group = GroupDecision(
        to_keep=asset_1,
        to_delete=[asset_2, asset_3]
    )

    result= DecisionResult(
        groups=[group]
    )

    assert result.total_files_to_delete == 2

def test_get_assets_to_delete_returns_correct_assets():
    asset_1 = make_asset("test.txt")
    asset_2 = make_asset("report.pdf")
    asset_3 = make_asset("video.mp4")

    group = GroupDecision(
        to_keep=asset_1,
        to_delete=[asset_2, asset_3]
    )

    result = DecisionResult(
        groups=[group]
    )

    assert result.get_assets_to_delete() == [asset_2, asset_3]

def test_total_groups_returns_correct_count():
    asset_1 = make_asset("test.txt")
    asset_2 = make_asset("report.pdf")

    group_1 = GroupDecision(
        to_keep=asset_1,
        to_delete=[]
    )

    group_2 = GroupDecision(
        to_keep=asset_2,
        to_delete=[]
    )

    result = DecisionResult(
        groups=[group_1, group_2]
    )

    assert result.total_groups == 2



