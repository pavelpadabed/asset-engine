from domain.asset import Asset
from domain.occurrence import Occurrence
from application.dto.deduplicate_result import GroupDecision, DecisionResult

class DecisionLayer:
    def build_decisions(
            self, groups: list[tuple[Asset, list[Occurrence]]]
    ) -> DecisionResult:
        decision_groups = []

        for asset, occurrences in  groups:
            keep = max(occurrences, key=lambda o: o.modified_time)
            delete = [
                occurrence
                for occurrence in occurrences
                if occurrence != keep
            ]

            decision_groups.append(
                GroupDecision(to_keep=keep, to_delete=delete)
            )

        return DecisionResult(groups=decision_groups)







