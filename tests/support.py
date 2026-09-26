from datetime import date

from biblio.models.book import Book
from biblio.models.member import Member
from biblio.models.subscription import Subscription
from biblio.copy_inventory import CopyInventory
from biblio.subscription_manager import SubscriptionManager
from biblio.borrowing_policy import BorrowingPolicy
from biblio.business_calendar import BusinessCalendar
from biblio.loan_manager import LoanManager


def fixture(quota=5):
    today = date(2026, 9, 15)
    book = Book(1, "Dune", "Herbert", "9780441172719", 1, 1)
    member = Member(1, "Camille", "c@example.com", today)
    inventory = CopyInventory()
    inventory.register_book(book)
    subscriptions = SubscriptionManager()
    subscriptions.register(Subscription(1, today, date(2026, 12, 31), quota))
    manager = LoanManager(inventory, BorrowingPolicy(subscriptions), BusinessCalendar())
    return today, book, member, manager
