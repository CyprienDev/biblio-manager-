import unittest
from datetime import date, timedelta
from decimal import Decimal

from biblio.account_ledger import AccountLedger
from biblio.acquisition_service import AcquisitionService
from biblio.borrowing_policy import BorrowingPolicy
from biblio.branches import BranchRegistry
from biblio.business_calendar import BusinessCalendar
from biblio.copy_inventory import CopyInventory
from biblio.exceptions import BookNotAvailableError
from biblio.fine_calculator import FineCalculator
from biblio.loan_manager import LoanManager
from biblio.models.account import Account
from biblio.models.book import Book
from biblio.models.branch import Branch
from biblio.models.ledger_entry import LedgerEntry
from biblio.models.member import Member
from biblio.models.payment import Payment
from biblio.models.reservation import Reservation
from biblio.models.subscription import Subscription
from biblio.models.supplier import Supplier
from biblio.payment_service import PaymentService
from biblio.pickup_service import PickupService
from biblio.receiving_service import ReceivingService
from biblio.reservation import ReservationManager
from biblio.return_service import ReturnService
from biblio.subscription_manager import SubscriptionManager
from biblio.transfer_service import TransferService


class WorkflowTests(unittest.TestCase):
    def test_acquisition_loan_reservation_transfer_return_and_payment(self):
        for origin, destination in ((1, 2), (2, 1)):
            with self.subTest(origin=origin, destination=destination):
                day = date(2026, 11, 2)
                branches = BranchRegistry()
                branches.add(Branch(1, "Centre"))
                branches.add(Branch(2, "Nord"))
                inventory = CopyInventory()
                book = Book(1, "Dune", "Herbert", "9780441172719", 0, 0)
                acquisitions = AcquisitionService(branches)
                acquisitions.register_supplier(Supplier("s", "Librairie"))
                order = acquisitions.place_order("o", "s", book, 1, origin)
                receiving = ReceivingService(acquisitions, inventory)
                self.assertTrue(receiving.receive("receipt", "o", 1))
                self.assertFalse(receiving.receive("receipt", "o", 1))
                self.assertEqual(order.remaining, 0)
                copy = book.copies[0]
                self.assertIs(inventory.get(copy.id), copy)

                members = [Member(i, f"Lecteur {i}", f"{i}@example.com", day)
                           for i in (1, 2)]
                subscriptions = SubscriptionManager()
                for member in members:
                    subscriptions.register(Subscription(member.id, day, date(2027, 1, 1)))
                manager = LoanManager(inventory, BorrowingPolicy(subscriptions), BusinessCalendar())
                loan = manager.create_loan(book, members[0], day, branch_id=origin)
                reservation = Reservation("r", book.id, members[1].id, day)
                reservations = ReservationManager()
                self.assertTrue(reservations.reserve(book, reservation))
                self.assertEqual(book.exemplaires_dispo, 0)
                with self.assertRaises(BookNotAvailableError):
                    manager.create_loan(book, members[1], day, branch_id=origin)
                self.assertEqual(members[1].emprunts_en_cours, 0)

                returned_on = loan.date_retour_prevue + timedelta(days=2)
                returns = ReturnService(manager)
                self.assertTrue(returns.return_loan(loan.id, returned_on))
                self.assertFalse(returns.return_loan(loan.id, returned_on))
                self.assertEqual(members[0].emprunts_en_cours, 0)
                fine = FineCalculator().calculate_fine(loan)
                self.assertGreater(fine, Decimal("0"))
                ledger = AccountLedger()
                ledger.register(Account(members[0].id))
                ledger.post(LedgerEntry("fine", members[0].id, fine, returned_on))
                payment = Payment("p", members[0].id, fine, returned_on)
                payments = PaymentService(ledger)
                self.assertTrue(payments.pay(payment))
                self.assertFalse(payments.pay(payment))
                self.assertEqual(ledger.balance(members[0].id), Decimal("0"))

                transfers = TransferService(inventory)
                transfers.start("t", copy.id, destination)
                self.assertEqual(book.exemplaires_dispo, 0)
                self.assertTrue(transfers.receive("t"))
                self.assertFalse(transfers.receive("t"))
                self.assertEqual(inventory.available(book.id, origin), [])
                self.assertEqual(inventory.available(book.id, destination), [copy])
                self.assertIs(reservations.notify_next(book.id, returned_on), reservation)
                self.assertTrue(PickupService().collect(reservation, returned_on))
                second_loan = manager.create_loan(book, members[1], returned_on,
                                                  branch_id=destination)
                self.assertEqual(second_loan.copy_id, loan.copy_id)
                self.assertEqual(reservation.status, "collected")
                self.assertTrue(returns.return_loan(second_loan.id, returned_on))
                self.assertEqual(members[1].emprunts_en_cours, 0)
                self.assertEqual(book.exemplaires_total, 1)
                self.assertEqual(book.exemplaires_dispo, 1)
                self.assertEqual(len(inventory.copies), 1)
