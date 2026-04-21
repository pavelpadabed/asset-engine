from pathlib import Path
import datetime as dt

from application.services.scan_service import ScanService
from application.services.index_service import IndexService
from application.services.save_service import SaveService, AssetSaveStatus
from application.dto.scan_result import ScanResult
from interface.cli.presenters.asset_presenter import AssetPresenter

class ScanCommand:
    def __init__(
            self,scan_service: ScanService,
            index_service: IndexService,
            save_service: SaveService,
            presenter: ScanPresenter
    ) -> None:
        self.scan_service = scan_service
        self.index_service = index_service
        self.save_service = save_service
        self.presenter = presenter

    def execute(self, path: Path) -> ScanResult:
        start_time = dt.datetime.now()
        descriptors = self.scan_service.scan(path)
        assets = self.index_service.index(descriptors)
        total_files = 0
        new_assets = 0
        duplicates = 0
        total_size = 0
        for asset in assets:
            status = self.save_service.persist(asset)
            if status == AssetSaveStatus.NEW:
                new_assets += 1
            else:
                duplicates += 1
            total_files += 1
            total_size += asset.metadata.size
        end_time = dt.datetime.now()
        duration = end_time - start_time

        result = ScanResult(
            total_files=total_files,
            new_assets=new_assets,
            duplicates=duplicates,
            duration=duration,
            total_size=total_size
        )

        self.presenter.show_scan_result(result)

        return result



