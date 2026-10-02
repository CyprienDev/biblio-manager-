import unittest

from biblio.acquisition_service import AcquisitionService
from biblio.branches import BranchRegistry
from biblio.copy_inventory import CopyInventory
from biblio.models.book import Book
from biblio.models.branch import Branch
from biblio.models.copy import Copy
from biblio.models.supplier import Supplier
from biblio.receiving_service import ReceivingService


class Tests(unittest.TestCase):
    def setUp(self):
        self.branches = BranchRegistry()
        self.branches.add(Branch(1, "Centre"))
        self.acquisitions = AcquisitionService(self.branches)
        self.acquisitions.register_supplier(Supplier("s", "Librairie"))
        self.book = Book(1, "Dune", "Herbert", "9780441172719", 0, 0)
        self.order = self.acquisitions.place_order("o", "s", self.book, 3, 1)
        self.inventory = CopyInventory()
        self.service = ReceivingService(self.acquisitions, self.inventory)

    def test_partial_receipt_and_duplicate(self):
        self.assertTrue(self.service.receive("r1", "o", 1))
        self.assertFalse(self.service.receive("r1", "o", 1))
        self.assertEqual(self.order.remaining, 2)
        self.assertEqual(self.book.exemplaires_total, 1)
        self.assertTrue(self.service.receive("r2", "o", 2))
        self.assertEqual(self.order.remaining, 0)
        self.assertEqual(self.book.exemplaires_dispo, 3)
        self.assertEqual(len(self.inventory.available(self.book.id, 1)), 3)
        self.assertEqual(self.inventory.available(self.book.id, 2), [])
        self.assertTrue(self.book.borrow_copy())
        self.assertEqual(len(self.inventory.available(self.book.id)), 2)

    def test_invalid_receipts_do_not_mutate_stock(self):
        for quantity in (0, -1, 4, 1.5, True):
            with self.assertRaises(ValueError):
                self.service.receive("bad", "o", quantity)
        with self.assertRaises(KeyError):
            self.service.receive("unknown", "absent", 1)
        self.assertEqual(self.order.received, 0)
        self.assertEqual(self.book.exemplaires_total, 0)
        self.assertEqual(self.inventory.copies, {})
        self.assertEqual(self.service.receipts, {})

    def test_conflicting_reference_and_excess_after_partial(self):
        self.service.receive("r", "o", 2)
        with self.assertRaises(ValueError):
            self.service.receive("r", "o", 1)
        with self.assertRaises(ValueError):
            self.service.receive("r2", "o", 2)
        self.assertEqual(self.order.received, 2)
        self.assertEqual(self.book.exemplaires_total, 2)

    def test_order_validation(self):
        with self.assertRaises(ValueError):
            self.acquisitions.place_order("o", "s", self.book, 1, 1)
        for quantity in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                self.acquisitions.place_order("bad", "s", self.book, quantity, 1)
        with self.assertRaises(KeyError):
            self.acquisitions.place_order("bad", "unknown", self.book, 1, 1)
        with self.assertRaises(KeyError):
            self.acquisitions.place_order("bad", "s", self.book, 1, 99)
        self.assertEqual(list(self.acquisitions.orders), ["o"])

    def test_collision_is_atomic(self):
        self.inventory.copies["receipt:r:1"] = Copy("receipt:r:1", 99, 1)
        with self.assertRaises(ValueError):
            self.service.receive("r", "o", 1)
        self.assertEqual(self.book.copies, [])
        self.assertEqual(self.order.received, 0)
        self.assertEqual(self.service.receipts, {})

    def test_supplier_identity(self):
        self.assertFalse(self.acquisitions.register_supplier(Supplier("s", "Librairie")))
        with self.assertRaises(ValueError):
            self.acquisitions.register_supplier(Supplier("s", "Autre"))
