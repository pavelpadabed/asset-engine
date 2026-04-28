from datetime import timedelta
from dataclasses import dataclass

@dataclass
class ScanResult:
    total_files: int
    new_assets: int
    already_indexed: int
    duplicates: int
    duration: timedelta
    total_size: int