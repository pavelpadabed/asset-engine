from typing import Iterator

from application.components.hash.hash_calculator import HashCalculator
from application.dto.file_descriptor import FileDescriptor
from application.components.type_detector import detect

from domain.source import Source
from domain.asset import Asset
from domain.factories.asset_factory import AssetFactory

class IndexService:
    def __init__(self, hasher: HashCalculator, source: Source) -> None:
        self.hasher = hasher
        self.source = source

    def index(self,
              descriptors: Iterator[FileDescriptor]
    ) -> Iterator[Asset]:

        for descriptor in descriptors:
            path = descriptor.path

            asset_type = detect(path)
            if asset_type is None:
                continue

            file_hash = self.hasher.calculate(path)

            yield AssetFactory.create(
                descriptor,
                file_hash,
                self.source,
                asset_type
            )



