import unittest
from datetime import date
from decimal import Decimal
from biblio.models.account import Account
from biblio.models.ledger_entry import LedgerEntry
from biblio.models.payment import Payment
from biblio.account_ledger import AccountLedger
from biblio.payment_service import PaymentService
from biblio.models.refund import Refund
from biblio.refund_service import RefundService


class Tests(unittest.TestCase):
    def setUp(self):
        self.day = date(2026, 9, 20)
        self.ledger = AccountLedger()
        self.ledger.register(Account(1))
        self.ledger.post(LedgerEntry("fine", 1, Decimal("10"), self.day))
        self.payments = PaymentService(self.ledger)

    def test_cumulative_refunds_and_duplicate(self):
        self.payments.pay(Payment("p", 1, Decimal("5"), self.day))
        service = RefundService(self.payments)
        refund = Refund("r1", "p", Decimal("3"), self.day)
        self.assertTrue(service.refund(refund))
        self.assertFalse(service.refund(refund))
        with self.assertRaises(ValueError):
            service.refund(Refund("r2", "p", Decimal("3"), self.day))
        self.assertEqual(self.ledger.balance(1), Decimal("8"))
        self.assertTrue(service.refund(Refund("r3", "p", Decimal("2"), self.day)))
        self.assertEqual(self.ledger.balance(1), Decimal("10"))
