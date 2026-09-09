from dataclasses import dataclass


@dataclass
class Book:
    id: int
    titre: str
    auteur: str
    isbn: str
    exemplaires_total: int
    exemplaires_dispo: int

    def is_available(self) -> bool:
        return self.exemplaires_dispo > 0

    def borrow_copy(self) -> bool:
        if not self.is_available():
            return False

        self.exemplaires_dispo -= 1
        return True

    def return_copy(self) -> bool:
        if self.exemplaires_dispo >= self.exemplaires_total:
            return False

        self.exemplaires_dispo += 1
        return True
