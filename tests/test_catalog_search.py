import unittest

from biblio.catalog import Catalog
from biblio.models.book import Book


class Tests(unittest.TestCase):
    def test_partial_casefold_and_order(self):
        catalog = Catalog()
        first = Book(1, "Dune", "Frank Herbert", "a", 1, 1)
        second = Book(2, "Le Messie de Dune", "Frank Herbert", "b", 1, 1)
        third = Book(3, "Autre", "Élodie", "c", 1, 1)
        for book in (first, second, third):
            catalog.add_book(book)
        self.assertEqual(catalog.search(" dune "), [first, second])
        self.assertEqual(catalog.search("HERB"), [first, second])
        self.assertEqual(catalog.search("éLO"), [third])
        self.assertEqual(catalog.search("   "), [])
        self.assertEqual(catalog.search("absent"), [])
        self.assertIs(catalog.find_by_isbn("b"), second)
        self.assertEqual(catalog.search("dune"), [first, second])
