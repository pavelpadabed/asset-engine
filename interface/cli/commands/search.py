from application.services.search_service import SearchService
from application.criteria.asset_search_criteria import AssetSearchCriteria
from interface.cli.presenters.asset_presenter import AssetPresenter

class SearchCommand:
    def __init__(
            self, search_service: SearchService,
            presenter: AssetPresenter
    ) -> None:
        self.search_service = search_service
        self.presenter = presenter

    def execute(self, criteria: AssetSearchCriteria) -> None:
        assets = self.search_service.search(criteria)
        self.presenter.show_search_result(assets)