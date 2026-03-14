from application.dto.file_descriptor import FileDescriptor
from application.services.index_service import IndexService
from application.components.hash.hash_calculator import HashCalculator
from domain.source import Source
from domain.asset import Asset
from domain.hash import FileHash
from datetime import datetime

def test_index_service(tmp_path):
    file = tmp_path / "test.jpg"
    file.write_text("hello")

    descriptor = FileDescriptor(
        path=file,
        size = 5,
        modified_time=datetime.now()
    )

    hasher = HashCalculator()

    source = Source.filesystem(tmp_path)

    service = IndexService(hasher, source)

    results = list(service.index([descriptor]))

    asset = results[0]

    assert len(results) == 1
    assert isinstance(asset, Asset)

    assert isinstance(asset.source, Source)
    assert asset.source == source

    assert isinstance(asset.file_hash, FileHash)
    assert asset.metadata.size == 5
