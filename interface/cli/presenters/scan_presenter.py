from application.dto.scan_result import ScanResult
from utils.time_utils import format_duration
from utils.size_utils import format_size

class ScanPresenter:
    def show_scan_result(self, result: ScanResult) -> None:
        if result.total_files == 0:
            print(
                f"Scan completed\nNo files found in the directory.\n"
                f"Duration: {format_duration(result.duration)}"
            )
        else:
            print(
                f"Scan completed\n\n"
                f"Total files: {result.total_files}\n"
                f"Total size: {format_size(result.total_size)}\n\n"
                f"New assets: {result.new_assets}\n"
                f"Already indexed: {result.already_indexed}\n"
                f"Duplicates (in this scan): {result.duplicates}\n\n"
                f"Duration: {format_duration(result.duration)}"
            )
