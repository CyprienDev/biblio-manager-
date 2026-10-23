import unittest
from biblio.models.book import Book
from biblio.copy_inventory import CopyInventory


class Tests(unittest.TestCase):
    def test_stock_single_source(self):
        book = Book(1, "Dune", "Herbert", "x", 2, 2)
        inventory = CopyInventory()
        inventory.register_book(book)
        book.copies[0].status = "repair"
        self.assertEqual(book.exemplaires_dispo, 1)
        self.assertEqual(inventory.available(1), [book.copies[1]])
        self.assertTrue(book.borrow_copy())
        self.assertFalse(book.borrow_copy())
        self.assertTrue(book.return_copy())
        self.assertEqual(book.copies[0].status, "repair")
        inventory.register_book(book)
        self.assertEqual(len(inventory.copies), 2)
        with self.assertRaises(ValueError):
            inventory.register_book(Book(1, "Autre", "Auteur", "y", 1, 1))

    def test_only_available_state_is_borrowable(self):
        from biblio.availability import is_available
        from biblio.models.copy import Copy
        for status in ("loaned", "repair", "lost", "transit", "reserved"):
            with self.subTest(status=status):
                self.assertFalse(is_available(Copy("c", 1, status=status)))
        self.assertTrue(is_available(Copy("c", 1)))
