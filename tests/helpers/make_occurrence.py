import datetime as dt
from pathlib import Path
from uuid import UUID, uuid4

from domain.occurrence import Occurrence


def make_occurrence(
        name: str, asset_id: UUID, file_size: int | None = None,
        modified_time: dt.datetime | None = None
) -> Occurrence:
    path = Path(f"/fake/{name}")

    return Occurrence(
        occurrence_id=uuid4(),
        asset_id=asset_id,
        path=path,
        scan_id=uuid4(),
        file_size=file_size if file_size is not None else 100,
        modified_time=(
            modified_time if modified_time is not None
            else dt.datetime.now()
        )
    )