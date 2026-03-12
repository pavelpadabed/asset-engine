from pathlib import Path
from application.dto.file_descriptor import FileDescriptor
from typing import Iterator
from datetime import datetime

class ScanService:
    def scan(self, root_path: Path) -> Iterator[FileDescriptor]:
        for path in root_path.rglob("*"):
            if path.is_file() and not path.is_symlink():
                try:
                    stat = path.stat()
                except OSError:
                    continue

                size = stat.st_size
                modified_time = datetime.fromtimestamp(stat.st_mtime)

                yield FileDescriptor(
                    path=path,
                    size=size,
                    modified_time=modified_time
                )
