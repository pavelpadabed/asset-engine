from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class FileMetadata:
    size: int
    modified_time: datetime