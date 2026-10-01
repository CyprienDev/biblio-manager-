from . import circulation_report, financial_report


class ReportGenerator:
    def __init__(self, loans, ledger):
        self.loans = loans
        self.ledger = ledger

    def active_count(self):
        return len(circulation_report.active_loans(self.loans))

    def overdue_report(self, on):
        return circulation_report.overdue_report(self.loans, on)

    def most_popular_books(self, limit=10):
        return circulation_report.most_popular_books(self.loans, limit)

    def balances(self):
        return financial_report.balances(self.ledger)

    def total_debt(self):
        return financial_report.total_debt(self.ledger)
