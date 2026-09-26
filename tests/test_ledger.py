import unittest
from datetime import date
from decimal import Decimal
from biblio.models.account import Account
from biblio.models.ledger_entry import LedgerEntry
from biblio.account_ledger import AccountLedger


class Tests(unittest.TestCase):
    def test_entries_are_idempotent_and_separated(self):
        ledger = AccountLedger()
        ledger.register(Account(1))
        ledger.register(Account(2))
        entry = LedgerEntry("a", 1, Decimal("10.00"), date(2026, 9, 1))
        self.assertTrue(ledger.post(entry))
        self.assertFalse(ledger.post(entry))
        self.assertEqual(ledger.balance(1), Decimal("10"))
        self.assertEqual(ledger.balance(2), Decimal("0"))
        with self.assertRaises(ValueError):
            ledger.post(LedgerEntry("a", 1, Decimal("5"), entry.day))
        with self.assertRaises(ValueError):
            ledger.post(LedgerEntry("bad", 1, Decimal("NaN"), entry.day))
