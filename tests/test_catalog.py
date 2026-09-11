import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from biblio.models.book import Book


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.book = Book(
            id=1,
            titre="Dune",
            auteur="Frank Herbert",
            isbn="9780441172719",
            exemplaires_total=2,
            exemplaires_dispo=2,
        )

    def test_book_is_available_when_a_copy_is_in_stock(self):
        self.assertTrue(self.book.is_available())

    def test_borrow_copy_decreases_available_copies(self):
        self.assertTrue(self.book.borrow_copy())
        self.assertEqual(1, self.book.exemplaires_dispo)

    def test_borrow_copy_fails_when_no_copy_is_available(self):
        self.book.borrow_copy()
        self.book.borrow_copy()

        self.assertFalse(self.book.borrow_copy())
        self.assertEqual(0, self.book.exemplaires_dispo)

    def test_return_copy_increases_available_copies(self):
        self.book.borrow_copy()

        self.assertTrue(self.book.return_copy())
        self.assertEqual(2, self.book.exemplaires_dispo)

    def test_return_copy_fails_when_stock_is_full(self):
        self.assertFalse(self.book.return_copy())
        self.assertEqual(2, self.book.exemplaires_dispo)


if __name__ == "__main__":
    unittest.main()
