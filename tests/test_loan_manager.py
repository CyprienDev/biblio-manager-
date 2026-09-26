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
