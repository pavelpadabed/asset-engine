from domain.types import AssetType
from domain.source import Source
from domain.hash import FileHash
from application.dto.file_descriptor import FileDescriptor
from domain.metadata import FileMetadata
from domain.asset import Asset

class AssetFactory:
    @staticmethod
    def create(
            descriptor: FileDescriptor,
            file_hash: FileHash,
            source: Source,
            asset_type: AssetType
    ) -> Asset:

        metadata = FileMetadata(
            size=descriptor.size,
            modified_time=descriptor.modified_time
        )

        return Asset(
                path=descriptor.path,
                asset_type=asset_type,
                source=source,
                file_hash=file_hash,
                metadata=metadata
        )




