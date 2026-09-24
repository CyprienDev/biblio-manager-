from dataclasses import dataclass
from datetime import date

from .book import Book
from .member import Member


@dataclass
class Loan:
    id: int
    livre: Book
    membre: Member
    date_emprunt: date
    date_retour_prevue: date
    date_retour_reelle: date | None = None
    copy_id: str | None = None

    def __post_init__(self):
        if self.date_retour_prevue < self.date_emprunt:
            raise ValueError("Échéance antérieure à l'emprunt")

    def days_overdue(self, on: date | None = None) -> int:
        end = self.date_retour_reelle or on or date.today()
        return max(0, (end - self.date_retour_prevue).days)

    def is_overdue(self, on: date | None = None) -> bool:
        return self.days_overdue(on) > 0
