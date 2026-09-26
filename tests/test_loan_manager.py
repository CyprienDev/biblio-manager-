import unittest
from support import fixture
from biblio.return_service import ReturnService


class Tests(unittest.TestCase):
    def test_borrow_and_return(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        self.assertEqual(book.exemplaires_dispo, 0)
        self.assertEqual(member.emprunts_en_cours, 1)
        service = ReturnService(manager)
        self.assertTrue(service.return_loan(loan.id, day))
        self.assertFalse(service.return_loan(loan.id, day))
        self.assertEqual(book.exemplaires_dispo, 1)
        self.assertEqual(member.emprunts_en_cours, 0)


    def test_empty_stock_rejected(self):
        from biblio.exceptions import BookNotAvailableError
        day, book, member, manager = fixture()
        manager.create_loan(book, member, day)
        with self.assertRaises(BookNotAvailableError):
            manager.create_loan(book, member, day)
        self.assertEqual(len(manager.loans), 1)
        self.assertEqual(member.emprunts_en_cours, 1)

    def test_quota_expiration_and_branch(self):
        from datetime import date
        from biblio.exceptions import MemberNotEligibleError, BookNotAvailableError
        day, book, member, manager = fixture(quota=1)
        with self.assertRaises(BookNotAvailableError):
            manager.create_loan(book, member, day, branch_id=99)
        with self.assertRaises(MemberNotEligibleError):
            manager.create_loan(book, member, date(2027, 1, 1))
        manager.create_loan(book, member, day)
        with self.assertRaises(MemberNotEligibleError):
            manager.create_loan(book, member, day)
        self.assertEqual(member.emprunts_en_cours, 1)
