from enum import Enum
from dataclasses import dataclass

class AssetType(Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"


@dataclass(frozen=True)
class Type:
    value: AssetType




