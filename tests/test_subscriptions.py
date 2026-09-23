import unittest
from datetime import date
from biblio.models.member import Member
from biblio.models.subscription import Subscription
from biblio.subscription_manager import SubscriptionManager
from biblio.borrowing_policy import BorrowingPolicy


class Tests(unittest.TestCase):
    def test_boundaries_quota_and_counter(self):
        start, end = date(2026, 9, 1), date(2026, 9, 30)
        member = Member(1, "A", "a@example.com", start)
        subscriptions = SubscriptionManager()
        policy = BorrowingPolicy(subscriptions)
        self.assertFalse(policy.can_borrow(member, start))
        subscriptions.register(Subscription(1, start, end, 1))
        self.assertTrue(policy.can_borrow(member, end))
        self.assertFalse(policy.can_borrow(member, date(2026, 10, 1)))
        self.assertTrue(member.add_loan(1))
        self.assertFalse(policy.can_borrow(member, start))
        self.assertFalse(member.add_loan(1))
        self.assertTrue(member.remove_loan())
        self.assertFalse(member.remove_loan())
