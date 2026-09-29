import unittest
from support import fixture
from biblio.transfer_service import TransferService


class Tests(unittest.TestCase):
    def test_transit_and_single_receipt(self):
        _, book, _, manager = fixture()
        service = TransferService(manager.inventory)
        copy = book.copies[0]
        service.start("t", copy.id, 2)
        self.assertEqual(book.exemplaires_dispo, 0)
        self.assertTrue(service.receive("t"))
        self.assertFalse(service.receive("t"))
        self.assertEqual(book.exemplaires_total, 1)
        self.assertEqual(copy.branch_id, 2)
        self.assertEqual(manager.inventory.available(book.id, 0), [])
        self.assertEqual(manager.inventory.available(book.id, 2), [copy])
        copy.status = "loaned"
        with self.assertRaises(ValueError):
            service.start("t2", copy.id, 3)
