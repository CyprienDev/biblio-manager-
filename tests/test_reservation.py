import unittest
from datetime import date
from biblio.models.book import Book
from biblio.models.reservation import Reservation
from biblio.reservation import ReservationManager


class Tests(unittest.TestCase):
    def test_fifo_cancellation_and_uniqueness(self):
        day = date(2026, 9, 19)
        book = Book(1, "Dune", "Herbert", "x", 1, 0)
        manager = ReservationManager()
        first = Reservation("r1", 1, 1, day)
        second = Reservation("r2", 1, 2, day)
        third = Reservation("r3", 1, 3, day)
        for item in (first, second, third):
            self.assertTrue(manager.reserve(book, item))
        self.assertFalse(manager.reserve(book, Reservation("r4", 1, 1, day)))
        self.assertTrue(manager.queue.cancel("r2"))
        self.assertIs(manager.notify_next(1, day), first)
        self.assertIs(manager.notify_next(1, day), third)
        self.assertIsNone(manager.notify_next(1, day))
        self.assertEqual(second.status, "cancelled")

    def test_available_book_rejected(self):
        day = date(2026, 9, 19)
        manager = ReservationManager()
        self.assertFalse(manager.reserve(Book(1, "A", "B", "x", 1, 1),
                                         Reservation("r", 1, 1, day)))

    def test_unknown_and_middle_cancellation_preserve_other_members(self):
        from biblio.reservation_queue import ReservationQueue
        queue = ReservationQueue()
        reservations = [Reservation(str(i), 1, i, date(2026, 10, 19)) for i in range(3)]
        for item in reservations:
            queue.add(item)
        self.assertFalse(queue.cancel("unknown"))
        self.assertTrue(queue.cancel("1"))
        self.assertEqual([item.status for item in reservations], ["waiting", "cancelled", "waiting"])
        self.assertFalse(queue.cancel("1"))
        self.assertIs(queue.next(1), reservations[0])
