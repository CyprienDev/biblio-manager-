import unittest
from support import fixture
from biblio.inventory_service import InventoryService
from biblio.maintenance_service import MaintenanceService


class Tests(unittest.TestCase):
    def test_repair_and_missing_copy(self):
        _, book, _, manager = fixture()
        copy = book.copies[0]
        maintenance = MaintenanceService(manager.inventory)
        self.assertTrue(maintenance.start(copy.id))
        self.assertFalse(maintenance.start(copy.id))
        self.assertEqual(book.exemplaires_dispo, 0)
        self.assertTrue(maintenance.finish(copy.id))
        inventory = InventoryService(manager.inventory)
        inventory.start("i", 0)
        self.assertEqual(inventory.close("i"), {copy.id})
        self.assertEqual(copy.status, "lost")
        self.assertEqual(inventory.close("i"), set())
        self.assertFalse(maintenance.finish(copy.id))

    def test_scanned_and_checked_out_copies(self):
        day, book, member, manager = fixture()
        service = InventoryService(manager.inventory)
        service.start("i", 0)
        service.scan("i", book.copies[0].id)
        self.assertEqual(service.close("i"), set())
        service.start("j", 0)
        manager.create_loan(book, member, day)
        service.close("j")
        self.assertEqual(book.copies[0].status, "loaned")
