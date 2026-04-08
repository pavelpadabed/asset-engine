from domain.asset import Asset

class DecisionLayer:
    def build_decisions(
            self, groups: list[list[Asset]]
    ) -> list[dict[str, Asset | list[Asset]]]:
        decisions = []
        for group in groups:
            keep = max(group, key=lambda x: x.metadata.modified_time)
            delete = [a for a in group if a != keep]
            decisions.append({
                "keep": keep,
                "delete": delete
            })
        return decisions

    def extract_to_delete(
            self, decisions: list[dict[str, Asset | list[Asset]]]
    )-> list[Asset]:
        return [
            asset for decision in decisions
            for asset in decision['delete']
        ]


