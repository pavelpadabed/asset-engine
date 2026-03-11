from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass(slots=True)
class FileDescriptor:
    path: Path
    size: int
    modified_time: datetime
