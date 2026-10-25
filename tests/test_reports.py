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

    def test_financial_totals_preserve_cents_and_ignore_credit(self):
        from datetime import date
        from biblio.financial_report import balances, total_debt
        ledger = AccountLedger()
        for account_id, amount in ((1, "0.10"), (2, "0.20"), (3, "-1.00")):
            ledger.register(Account(account_id))
            ledger.post(LedgerEntry(str(account_id), account_id, Decimal(amount), date(2026, 10, 12)))
        self.assertEqual(total_debt(ledger), Decimal("0.30"))
        self.assertEqual(balances(ledger), {1: Decimal("0.10"), 2: Decimal("0.20"), 3: Decimal("-1.00")})
        self.assertEqual(len(ledger.entries), 3)
        self.assertEqual(total_debt(AccountLedger()), Decimal("0"))
