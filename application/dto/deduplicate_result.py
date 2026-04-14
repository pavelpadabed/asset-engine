from dataclasses import dataclass

from domain.asset import Asset

@dataclass
class GroupDecision:
    to_keep: Asset
    to_delete: list[Asset]


@dataclass
class DecisionResult:
    groups: list[GroupDecision]

    @property
    def total_groups(self):
        return len(self.groups)

    @property
    def total_files(self):
        return len(self.get_assets_to_delete())

    def get_assets_to_delete(self) -> list[Asset]:
        assets_to_delete = []

        for group in self.groups:
            assets_to_delete.extend(group.to_delete)

        return assets_to_delete
