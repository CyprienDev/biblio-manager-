import unittest
from datetime import date, timedelta
from biblio.models.reservation import Reservation
from biblio.pickup_service import PickupService


class Tests(unittest.TestCase):
    def test_inclusive_deadline_and_idempotence(self):
        day = date(2026, 9, 20)
        reservation = Reservation("r", 1, 1, day, "ready", day)
        service = PickupService()
        self.assertFalse(service.expire(reservation, day))
        self.assertTrue(service.collect(reservation, day))
        self.assertFalse(service.collect(reservation, day))
        late = Reservation("r2", 1, 2, day, "ready", day)
        self.assertFalse(service.collect(late, day + timedelta(days=1)))
        self.assertEqual(late.status, "expired")
