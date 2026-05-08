from domain.occurrence import Occurrence
from storage.repositories.asset_repository import AssetRepository

class DeleteService:
    def __init__(self, repository: AssetRepository) -> None:
        self.repository = repository

    def delete_occurrences(self, occurrences: list[Occurrence]) -> None:
        for occurrence in occurrences:
            occurrence.path.unlink(missing_ok=True)
            self.repository.delete(occurrence.id)

    # TODO (refactor): improve deletion robustness
    # - handle database errors (try/except)
    # - ensure consistency between filesystem and database
    # - consider transaction or rollback strategy
    # - add logging for failed deletions