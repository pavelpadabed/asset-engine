from application.dto.scan_result import ScanResult
from utils.time_utils import format_duration

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
                f"Total size: {result.total_size}\n\n"
                f"New assets: {result.new_assets}\n"
                f"Duplicates: {result.duplicates}\n\n"
                f"Duration: {format_duration(result.duration)}"
            )

    # TODO:
    # - Implement format_size utility:
    #   - Convert bytes → KB / MB / GB
    #   - Human-readable output (e.g. "1.2 MB")
    #   - Consider rounding strategy (1–2 decimal places)
    #   - Handle edge cases (0 bytes, very small files)