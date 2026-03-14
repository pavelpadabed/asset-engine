from enum import Enum
from dataclasses import dataclass

class TypeEnum(Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"


@dataclass(frozen=True, slots=True)
class AssetType:
    value: TypeEnum

    @classmethod
    def image(cls) -> "AssetType":
        return cls(TypeEnum.IMAGE)

    @classmethod
    def audio(cls) -> "AssetType":
        return cls(TypeEnum.AUDIO)

    @classmethod
    def video(cls) -> "AssetType":
        return cls(TypeEnum.VIDEO)

    @classmethod
    def pdf(cls) -> "AssetType":
        return cls(TypeEnum.PDF)




