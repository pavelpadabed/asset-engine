from application.services.search_service import SearchService
from application.criteria.occurrence_search_criteria import OccurrenceSearchCriteria
from tests.test_search_service.fake_repo import FakeRepository
from tests.helpers.make_occurrence import make_occurrence
from tests.helpers.make_asset import make_asset

def test_search_ext():

    asset = make_asset()
    occurrence_1 = make_occurrence("test.txt", asset.id)
    occurrence_2 = make_occurrence("test.mp3", asset.id)

    repo = FakeRepository([occurrence_1, occurrence_2])
    service = SearchService(repo)
    criteria = OccurrenceSearchCriteria(extension="mp3")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert result[0].path.suffix == ".mp3"

def test_name_contains():
    asset = make_asset()
    occurrence_1 = make_occurrence("test.txt", asset.id)
    occurrence_2 = make_occurrence("file.mp3", asset.id)


    repo = FakeRepository([occurrence_1, occurrence_2])
    service = SearchService(repo)
    criteria = OccurrenceSearchCriteria(name_contains="test")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert "test" in result[0].path.stem
    assert result[0].path == occurrence_1.path


def test_no_criteria_all_results():
    asset = make_asset()

    occurrence_1 = make_occurrence("test.txt", asset.id)
    occurrence_2 = make_occurrence("file.mp3", asset.id)

    repo = FakeRepository([occurrence_1, occurrence_2])
    service = SearchService(repo)
    criteria = OccurrenceSearchCriteria()

    result = list(service.search(criteria))

    assert len(result) == 2
    assert {a.path for a in result} == {occurrence_1.path, occurrence_2.path}

def test_combi_search():
    asset = make_asset()
    occurrence_1 = make_occurrence("test.txt", asset.id)
    occurrence_2 = make_occurrence("file.mp3", asset.id)
    occurrence_3 = make_occurrence("report.mp4", asset.id)

    repo = FakeRepository([occurrence_1, occurrence_2, occurrence_3])
    service = SearchService(repo)
    criteria = OccurrenceSearchCriteria(name_contains="report",extension="mp4")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert result[0].path == occurrence_3.path


