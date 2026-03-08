from enum import Enum
from dataclasses import dataclass

class SourceEnum(Enum):
    FILESYSTEM = "filesystem"
    API = "api"
    USER_UPLOAD = "user_upload"
    GENERATED = "generated"


@dataclass(frozen=True)
class Source:
    value: SourceEnum

