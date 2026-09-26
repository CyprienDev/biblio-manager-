from .copy import Copy
from ..availability import is_available


class Book:
    def __init__(self, id, titre, auteur, isbn, exemplaires_total, exemplaires_dispo):
        if not 0 <= exemplaires_dispo <= exemplaires_total:
            raise ValueError("Stock invalide")
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.copies = [
            Copy(f"{id}-{i + 1}", id, status=(
                "available" if i < exemplaires_dispo else "loaned"))
            for i in range(exemplaires_total)
        ]

    @property
    def exemplaires_total(self):
        return len(self.copies)

    @property
    def exemplaires_dispo(self):
        return sum(is_available(copy) for copy in self.copies)

    def is_available(self):
        return self.exemplaires_dispo > 0

    def borrow_copy(self):
        for copy in self.copies:
            if is_available(copy):
                copy.status = "loaned"
                return True
        return False

    def return_copy(self):
        for copy in self.copies:
            if copy.status == "loaned":
                copy.status = "available"
                return True
        return False
