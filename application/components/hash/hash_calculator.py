from application.components.hash.full_hash import FullHash
from pathlib import Path
from domain.hash import FileHash


class HashCalculator:
    def __init__(self) -> None:
        self.full_hash = FullHash()

    def calculate(self, path: Path) -> FileHash:
        return self.full_hash.calculate(path)