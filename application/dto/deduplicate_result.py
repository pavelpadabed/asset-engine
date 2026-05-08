from dataclasses import dataclass

from domain.occurrence import Occurrence

@dataclass
class GroupDecision:
    to_keep: Occurrence
    to_delete: list[Occurrence]


@dataclass
class DecisionResult:
    groups: list[GroupDecision]

    @property
    def total_groups(self):
        return len(self.groups)

    @property
    def total_files_to_delete(self):
        return len(self.get_occurrences_to_delete())

    @property
    def total_files(self):
        return self.total_groups + self.total_files_to_delete

    def get_occurrences_to_delete(self) -> list[Occurrence]:
        occurrences_to_delete = []

        for group in self.groups:
            occurrences_to_delete.extend(group.to_delete)

        # TODO: Add total_size calculation to DecisionResult
        # - implement method or property to calculate total size of occurrences_to_delete
        # - sum asset sizes from group.to_delete across all groups
        # - expose as decision_result.total_size
        # - use in presenter to show total space to be freed

        return occurrences_to_delete
