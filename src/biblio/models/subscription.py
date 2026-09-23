from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Subscription:
    member_id: int
    start: date
    end: date
    quota: int = 5

    def __post_init__(self):
        if self.end < self.start or self.quota < 1:
            raise ValueError("Abonnement invalide")

    def is_active(self, on: date) -> bool:
        return self.start <= on <= self.end
