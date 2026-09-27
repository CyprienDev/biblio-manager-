import unittest
from datetime import date
from decimal import Decimal
from biblio.models.account import Account
from biblio.models.ledger_entry import LedgerEntry
from biblio.models.payment import Payment
from biblio.account_ledger import AccountLedger
from biblio.payment_service import PaymentService


class Tests(unittest.TestCase):
    def setUp(self):
        self.day = date(2026, 9, 20)
        self.ledger = AccountLedger()
        self.ledger.register(Account(1))
        self.ledger.post(LedgerEntry("fine", 1, Decimal("10"), self.day))
        self.payments = PaymentService(self.ledger)

    def test_partial_and_duplicate(self):
        payment = Payment("p", 1, Decimal("3"), self.day)
        self.assertTrue(self.payments.pay(payment))
        self.assertFalse(self.payments.pay(payment))
        self.assertEqual(self.ledger.balance(1), Decimal("7"))

    def test_reject_overpayment(self):
        with self.assertRaises(ValueError):
            self.payments.pay(Payment("p", 1, Decimal("11"), self.day))
        self.assertEqual(self.ledger.balance(1), Decimal("10"))
