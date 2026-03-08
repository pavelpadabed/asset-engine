from dataclasses import dataclass
import re

MAX_LENGTH = 32

@dataclass(frozen=True, slots=True)
class Tag:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Tag value must be a string")

        norm_value = self.value.strip().lower()

        if not norm_value:
            raise ValueError("Tag value cannot be empty or whitespace")

        if  len(norm_value) > MAX_LENGTH:
            raise ValueError("Tag value must be between 1 and 32 characters")

        if not re.fullmatch(r"(?=.*[a-z0-9])[a-z0-9_-]+", norm_value):
            raise ValueError(
                "Tag value may contain only lowercase letters, digits, '-' or '_', "
                "and must include at least one letter or digit"
            )

        object.__setattr__(self, "value", norm_value)
