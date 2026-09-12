from typing import Dict, List, Optional

from .models.book import Book


class Catalog:
    def __init__(self):
        self._books: Dict[int, Book] = {}

    def add_book(self, book: Book) -> bool:
        if book.id in self._books:
            return False

        self._books[book.id] = book
        return True

    def remove_book(self, book_id: int) -> bool:
        if book_id not in self._books:
            return False

        del self._books[book_id]
        return True

    def search(self, query: str) -> List[Book]:
        query = query.strip().casefold()
        if not query:
            return []

        return [
            book
            for book in self._books.values()
            if query in book.titre.casefold() or query in book.auteur.casefold()
        ]

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self._books.values():
            if book.isbn == isbn:
                return book

        return None
