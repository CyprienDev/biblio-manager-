from .availability import is_available


class CopyInventory:
    def __init__(self):
        self.copies = {}

    def register_book(self, book):
        ids = [copy.id for copy in book.copies]
        if len(ids) != len(set(ids)):
            raise ValueError("Identifiants d'exemplaires dupliqués")
        for copy in book.copies:
            if copy.id in self.copies and self.copies[copy.id] is not copy:
                raise ValueError("Exemplaire déjà enregistré")
        for copy in book.copies:
            self.copies[copy.id] = copy

    def get(self, copy_id):
        return self.copies[copy_id]

    def available(self, book_id, branch_id=None):
        return [copy for copy in self.copies.values()
                if copy.book_id == book_id and is_available(copy)
                and (branch_id is None or copy.branch_id == branch_id)]
