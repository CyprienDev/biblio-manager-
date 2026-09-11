
from dataclasses import dataclass
from datetime import date
from typing import ClassVar


@dataclass
class Member:
    MAX_LOANS: ClassVar[int] = 5

    id: int
    nom: str
    email: str
    date_inscription: date
    emprunts_en_cours: int = 0

    def can_borrow(self) -> bool:
        return self.emprunts_en_cours < self.MAX_LOANS

    def add_loan(self) -> bool:
        if not self.can_borrow():
            return False

        self.emprunts_en_cours += 1
        return True
