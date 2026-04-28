from pathlib import Path
import datetime as dt

from application.services.scan_service import ScanService
from application.services.index_service import IndexService
from application.services.save_service import SaveService, AssetSaveStatus
from application.dto.scan_result import ScanResult
from interface.cli.presenters.scan_presenter import ScanPresenter

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
        already_indexed = 0
        duplicates = 0
        total_size = 0
        seen_hashes = set()
        for asset in assets:
            value = asset.file_hash.value
            is_duplicate = value in seen_hashes

            if not is_duplicate:
                seen_hashes.add(value)

            status = self.save_service.persist(asset)

            if status == AssetSaveStatus.NEW:
                new_assets += 1
            elif status == AssetSaveStatus.ALREADY_INDEXED:
                already_indexed += 1

            if is_duplicate:
                duplicates += 1

            total_files += 1
            total_size += asset.metadata.size
        end_time = dt.datetime.now()
        duration = end_time - start_time

        result = ScanResult(
            total_files=total_files,
            new_assets=new_assets,
            already_indexed=already_indexed,
            duplicates=duplicates,
            duration=duration,
            total_size=total_size
        )

        self.presenter.show_scan_result(result)

        return result
    # TODO (refactor): simplify ScanCommand.execute
    # - Reduce branching (if / elif / else) complexity
    # - Separate responsibilities:
    #   - duplicate detection within scan (seen_hashes)
    #   - persistence (save_service)
    #   - counters aggregation (new / already_indexed / duplicates)
    # - Avoid mixing logic in one loop block
    # - Consider extracting helpers:
    #     - _is_duplicate_in_scan(value, seen_hashes)
    #     - _update_counters(status, is_duplicate)
    # - Improve naming (value → file_hash_value)
    # - Aim for flatter, more readable flow (less nested conditions)




