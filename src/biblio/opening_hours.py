from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OpeningHours:
    weekdays: frozenset[int] = frozenset(range(5))

    def __post_init__(self):
        if not self.weekdays or not self.weekdays <= set(range(7)):
            raise ValueError("Jours d'ouverture invalides")

    def is_open(self, day: date) -> bool:
        return day.weekday() in self.weekdays
