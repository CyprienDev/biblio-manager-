from dataclasses import dataclass, field
from datetime import date, timedelta

from .opening_hours import OpeningHours


@dataclass
class BusinessCalendar:
    hours: OpeningHours = field(default_factory=OpeningHours)
    closures: set[date] = field(default_factory=set)

    def is_open(self, day: date) -> bool:
        return self.hours.is_open(day) and day not in self.closures

    def add_days(self, start: date, count: int) -> date:
        if count < 0:
            raise ValueError("Nombre de jours négatif")
        result = start
        while count:
            result += timedelta(days=1)
            if self.is_open(result):
                count -= 1
        return result
