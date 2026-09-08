"""Track missing polished results independently of transcript insertion."""


class PolishWatch:
    def __init__(self):
        self.started: dict[int, float] = {}
        self.latest: int | None = None

    def begin(self, identity: int, now: float) -> None:
        self.latest = identity
        self.started[identity] = now

    def complete(self) -> None:
        # The server finishes each polishing attempt before the next full event.
        # A result therefore belongs to the latest full, even after insertion.
        self.started.pop(self.latest, None)
        self.latest = None

    def overdue(self, now: float, delay: float) -> int:
        return sum(now - started >= delay for started in self.started.values())

    def reset(self) -> None:
        self.started.clear()
        self.latest = None
