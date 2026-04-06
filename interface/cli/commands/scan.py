from pathlib import Path

from application.services.scan_service import ScanService
from application.services.index_service import IndexService
from application.services.save_service import SaveService
from application.services.duplicate_service import DuplicateService
from interface.cli.presenters.asset_presenter import AssetPresenter

class ScanCommand:
    def __init__(
            self,scan_service: ScanService,
            index_service: IndexService,
            save_service: SaveService,
            duplicate_service: DuplicateService,
            presenter: AssetPresenter
    ) -> None:
        self.scan_service = scan_service
        self.index_service = index_service
        self.save_service = save_service
        self.duplicate_service = duplicate_service
        self.presenter = presenter

    def execute(self, path: Path) -> None:
        descriptors = self.scan_service.scan(path)
        assets = self.index_service.index(descriptors)
        count = self.save_service.persist(assets)
        self.presenter.show_scan_result(count)
        duplicates = self.duplicate_service.detect_duplicates()
        self.presenter.show_duplicates(duplicates)