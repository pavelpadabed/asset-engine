from tests.helpers.make_asset import make_asset
from tests.helpers.make_occurrence import make_occurrence
from application.dto.deduplicate_result import GroupDecision, DecisionResult

def test_total_files_returns_correct_count():
    asset = make_asset()
    occurrence_1 = make_occurrence("report.pdf", asset.id)
    occurrence_2 = make_occurrence("report_copy.pdf", asset.id)
    occurrence_3 = make_occurrence("report_1.pdf", asset.id)

    group = GroupDecision(
        to_keep=occurrence_1,
        to_delete=[occurrence_2, occurrence_3]
    )

    result = DecisionResult(
        groups=[group]
    )

    assert result.total_files == 3

def test_total_files_to_delete_returns_correct_count():
    asset = make_asset()
    occurrence_1 = make_occurrence("video.mp4", asset.id)
    occurrence_2 = make_occurrence("video_copy.mp4", asset.id)
    occurrence_3 = make_occurrence("video_1.mp4", asset.id)


    group = GroupDecision(
        to_keep=occurrence_1,
        to_delete=[occurrence_2, occurrence_3]
    )

    result= DecisionResult(
        groups=[group]
    )

    assert result.total_files_to_delete == 2

def test_get_occurrences_to_delete_returns_correct_assets():
    asset = make_asset()
    occurrence_1 = make_occurrence("video.mp4", asset.id)
    occurrence_2 = make_occurrence("video_copy.mp4", asset.id)
    occurrence_3 = make_occurrence("video_1.mp4", asset.id)


    group = GroupDecision(
        to_keep=occurrence_1,
        to_delete=[occurrence_2, occurrence_3]
    )

    result = DecisionResult(
        groups=[group]
    )

    assert result.get_occurrences_to_delete() == [occurrence_2, occurrence_3]

def test_total_groups_returns_correct_count():
    asset = make_asset()
    occurrence_1 = make_occurrence("video.mp4", asset.id)
    occurrence_2 = make_occurrence("video_copy.mp4", asset.id)
    occurrence_3 = make_occurrence("video_1.mp4", asset.id)

    group_1 = GroupDecision(
        to_keep=occurrence_1,
        to_delete=[]
    )

    group_2 = GroupDecision(
        to_keep=occurrence_2,
        to_delete=[]
    )

    result = DecisionResult(
        groups=[group_1, group_2]
    )

    assert result.total_groups == 2



