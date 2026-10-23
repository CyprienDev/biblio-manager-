import unittest
from datetime import date
from support import fixture
from biblio.models.reservation import Reservation
from biblio.reservation_queue import ReservationQueue
from biblio.renewal_policy import RenewalPolicy


class Tests(unittest.TestCase):
    def test_extension_and_reservation_refusal(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        queue = ReservationQueue()
        policy = RenewalPolicy(manager.policy.subscriptions, queue)
        previous = loan.date_retour_prevue
        self.assertTrue(manager.extend_loan(loan.id, day, policy))
        self.assertGreater(loan.date_retour_prevue, previous)
        queue.add(Reservation("r", book.id, 99, day))
        previous = loan.date_retour_prevue
        self.assertFalse(manager.extend_loan(loan.id, day, policy))
        self.assertEqual(loan.date_retour_prevue, previous)
        self.assertFalse(policy.can_extend(loan, date(2027, 1, 1)))

    def test_expired_subscription_and_closed_loan(self):
        from datetime import timedelta
        from biblio.models.subscription import Subscription
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        subscriptions = manager.policy.subscriptions
        subscriptions.register(Subscription(member.id, day, day))
        policy = RenewalPolicy(subscriptions, ReservationQueue())
        self.assertTrue(policy.can_extend(loan, day))
        self.assertFalse(policy.can_extend(loan, day + timedelta(days=1)))
        self.assertFalse(policy.can_extend(loan, day - timedelta(days=1)))
        loan.date_retour_reelle = day
        self.assertFalse(policy.can_extend(loan, day))
