import unittest
from datetime import date
from biblio.models.loan import Loan
from biblio.models.member import Member
from biblio.models.book import Book


class Tests(unittest.TestCase):
    def test_overdue_and_early_return(self):
        start, due = date(2026, 9, 1), date(2026, 9, 10)
        loan = Loan(1, Book(1, "Dune", "Herbert", "x", 1, 1),
                    Member(1, "A", "a@b.fr", start), start, due)
        self.assertEqual(loan.days_overdue(start), 0)
        self.assertEqual(loan.days_overdue(due), 0)
        self.assertTrue(loan.is_overdue(date(2026, 9, 12)))
        loan.date_retour_reelle = date(2026, 9, 5)
        self.assertEqual(loan.days_overdue(date(2026, 9, 12)), 0)
