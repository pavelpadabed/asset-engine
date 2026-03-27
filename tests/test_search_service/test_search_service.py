from application.services.search_service import SearchService
from application.criteria.asset_search_criteria import AssetSearchCriteria
from tests.test_search_service.fake_repo import FakeRepository
from tests.helpers.make_asset import make_asset

def test_search_ext():

    asset_1 = make_asset("test.mp3")

    asset_2 = make_asset("test.txt")

    repo = FakeRepository([asset_1, asset_2])
    service = SearchService(repo)
    criteria = AssetSearchCriteria(extension="mp3")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert result[0].path.suffix == ".mp3"

def test_name_contains():
    asset_1 = make_asset("test_file.mp3")

    asset_2 = make_asset("file_1.txt")

    repo = FakeRepository([asset_1, asset_2])
    service = SearchService(repo)
    criteria = AssetSearchCriteria(name_contains="test")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert "test" in result[0].path.stem
    assert result[0].path == asset_1.path


def test_no_criteria_all_assets():
    asset_1 = make_asset("test.txt")

    asset_2 = make_asset("report.mp4")

    repo = FakeRepository([asset_1, asset_2])
    service = SearchService(repo)
    criteria = AssetSearchCriteria()

    result = list(service.search(criteria))

    assert len(result) == 2
    assert {a.path for a in result} == {asset_1.path, asset_2.path}

def test_combi_search():
    asset_1 = make_asset("report.mp3")

    asset_2 = make_asset("test_file.txt")

    asset_3 = make_asset("report.mp4")

    repo = FakeRepository([asset_1, asset_2, asset_3])
    service = SearchService(repo)
    criteria = AssetSearchCriteria(name_contains="report",extension="mp4")

    result = list(service.search(criteria))

    assert len(result) == 1
    assert result[0].path == asset_3.path


