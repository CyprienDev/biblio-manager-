import unittest
from datetime import timedelta
from decimal import Decimal

from support import fixture
from biblio.models.account import Account
from biblio.models.ledger_entry import LedgerEntry
from biblio.account_ledger import AccountLedger
from biblio.reports import ReportGenerator
from biblio.return_service import ReturnService


class Tests(unittest.TestCase):
    def test_reports_and_no_mutation(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        ledger = AccountLedger()
        ledger.register(Account(member.id))
        ledger.post(LedgerEntry("f", member.id, Decimal("3"), day))
        report = ReportGenerator(list(manager.loans.values()), ledger)
        self.assertEqual(report.active_count(), 1)
        self.assertEqual(report.most_popular_books(), [(book.id, 1)])
        self.assertEqual(report.overdue_report(loan.date_retour_prevue + timedelta(days=1)), [loan])
        self.assertEqual(report.total_debt(), Decimal("3"))
        self.assertEqual(report.balances(), {member.id: Decimal("3")})
        self.assertEqual(len(ledger.entries), 1)
        ReturnService(manager).return_loan(loan.id, day)
        self.assertEqual(report.active_count(), 0)
        self.assertEqual(report.overdue_report(loan.date_retour_prevue + timedelta(days=1)), [])
