from domain.occurrence import Occurrence

class FakeRepository:
    def __init__(self, occurrences: list[Occurrence]) -> None:
        self.occurrences = occurrences

    def list_occurrences(self) -> list[Occurrence]:
        return self.occurrences