from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

class SourceEnum(Enum):
    FILESYSTEM = "filesystem"
    API = "api"
    USER_UPLOAD = "user_upload"
    GENERATED = "generated"


@dataclass(frozen=True, slots=True)
class Source:
    type: SourceEnum
    path: Optional[Path]

    @classmethod
    def filesystem(cls, path: Path) -> "Source":
        return cls(SourceEnum.FILESYSTEM, path)

    @classmethod
    def api(cls) -> "Source":
        return cls(SourceEnum.API, None)

    @classmethod
    def user_upload(cls) -> "Source":
        return cls(SourceEnum.USER_UPLOAD, None)

    @classmethod
    def generated(cls) -> "Source":
        return cls(SourceEnum.GENERATED, None)


