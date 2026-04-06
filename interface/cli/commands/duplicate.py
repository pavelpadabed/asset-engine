from application.services.duplicate_service import DuplicateService
from interface.cli.presenters.asset_presenter import AssetPresenter

class DuplicateCommand:
    def __init__(
            self, d_service: DuplicateService,
            presenter: AssetPresenter
    ) -> None:
        self.d_service = d_service
        self.presenter = presenter

    def execute(self) -> None:
        duplicates = self.d_service.detect_duplicates()
        self.presenter.show_duplicate_result(duplicates)