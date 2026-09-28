import unittest
from datetime import timedelta
from decimal import Decimal
from support import fixture
from biblio.fine_calculator import FineCalculator


class Tests(unittest.TestCase):
    def test_due_day(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        self.assertEqual(FineCalculator().calculate_fine(loan, loan.date_retour_prevue),
                         Decimal("0"))

    def test_late_cap_and_early(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        calculator = FineCalculator()
        self.assertEqual(calculator.calculate_fine(loan, day), Decimal("0"))
        self.assertEqual(calculator.calculate_fine(
            loan, loan.date_retour_prevue + timedelta(days=2)), Decimal("1"))
        self.assertEqual(calculator.calculate_fine(
            loan, loan.date_retour_prevue + timedelta(days=100)), Decimal("20"))

    def test_returned_on_due_day_stays_free(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        loan.date_retour_reelle = loan.date_retour_prevue
        self.assertEqual(FineCalculator().calculate_fine(
            loan, loan.date_retour_prevue + timedelta(days=10)), Decimal("0"))
