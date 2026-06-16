from typing import NamedTuple
from datetime import datetime
from uuid import UUID


class PathObservation(NamedTuple):
    occurrence_id: UUID
    modified_at: datetime
    observed_at: datetime