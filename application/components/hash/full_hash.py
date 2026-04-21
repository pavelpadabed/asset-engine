from pathlib import Path
import hashlib
from domain.hash import FileHash

CHUNK_SIZE = 8192

class FullHash:
    def calculate(self, path: Path) -> FileHash:
        sha = hashlib.sha256()

        with open(path, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                sha.update(chunk)

        digest = sha.hexdigest()

        return FileHash(digest)


print(FileHash)