from domain.asset import Asset

class FakeRepository:
    def __init__(self, assets: list[Asset]) -> None:
        self.assets = assets

    def list(self) -> list[Asset]:
        return self.assets