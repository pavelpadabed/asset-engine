from domain.asset import Asset
from application.dto.deduplicate_result import GroupDecision, DecisionResult

class DecisionLayer:
    def build_decisions(
            self, groups: list[tuple[Asset, list[Occurrence]]]
    ) -> DecisionResult:
        decision_groups = []

        for asset, occurrences in  groups:
            keep = occurrences[0]
            delete = occurrences[1:]

            decision_groups.append(
                GroupDecision(to_keep=keep, to_delete=delete)
            )

        return DecisionResult(groups=decision_groups)







