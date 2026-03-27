from dataclasses import dataclass
from datetime import datetime

@dataclass
class AssetSearchCriteria:
    name_contains: str | None = None
    extension: str | None = None
    modified_before: datetime | None = None
    modified_after: datetime | None = None
    min_size: int | None = None
    max_size: int | None = None