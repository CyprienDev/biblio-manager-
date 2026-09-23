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

    def can_borrow(self, quota: int = MAX_LOANS) -> bool:
        return self.emprunts_en_cours < quota

    def add_loan(self, quota: int = MAX_LOANS) -> bool:
        if not self.can_borrow(quota):
            return False
        self.emprunts_en_cours += 1
        return True

    def remove_loan(self) -> bool:
        if self.emprunts_en_cours == 0:
            return False
        self.emprunts_en_cours -= 1
        return True
