from domain.asset import Asset
from application.dto.deduplicate_result import GroupDecision, DecisionResult

class DecisionLayer:
    def build_decisions(
            self, groups: list[list[Asset]]
    ) -> DecisionResult:
        decision_groups = []

        for group in groups:
            keep = max(group, key=lambda x: x.metadata.modified_time)
            delete = [asset for asset in group if asset != keep]

            decision_groups.append(
                GroupDecision(to_keep=keep, to_delete=delete)
            )

        return DecisionResult(groups=decision_groups)







