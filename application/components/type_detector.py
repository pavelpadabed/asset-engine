from domain.types import AssetType
from pathlib import Path

IMAGE = AssetType.image()
AUDIO = AssetType.audio()
VIDEO = AssetType.video()
PDF = AssetType.pdf()

EXTENSION_MAP = {
    ".jpg": IMAGE,
    ".jpeg": IMAGE,
    ".png": IMAGE,

    ".mp3": AUDIO,
    ".wav": AUDIO,

    ".mp4": VIDEO,
    ".mov": VIDEO,

    ".pdf": PDF
}

def detect(path: Path) -> AssetType | None:
    suffix = path.suffix.lower()
    return EXTENSION_MAP.get(suffix)