from dataclasses import dataclass
import re

@dataclass(frozen=True, slots=True)
class FileHash:
    value: str
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValueError("FileHash value must be a string")

        raw_value = self.value.lower()

        if len(raw_value) != 64:
            raise ValueError(
                "FileHash must be exactly 64 hex characters long"
            )

        if not re.fullmatch("[0-9a-f]{64}", raw_value):
            raise ValueError(
                "FileHash must consist of 64 hexadecimal "
                "characters (0-9, a-f)"
            )

        object.__setattr__(self, "value", raw_value)