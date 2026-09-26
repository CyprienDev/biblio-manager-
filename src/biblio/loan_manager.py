from .exceptions import BookNotAvailableError, MemberNotEligibleError
from .models.loan import Loan


class LoanManager:
    def __init__(self, inventory, policy, calendar):
        self.inventory = inventory
        self.policy = policy
        self.calendar = calendar
        self.loans = {}
        self.next_id = 1

    def create_loan(self, book, member, on, branch_id=None, duration=10):
        if not self.policy.can_borrow(member, on):
            raise MemberNotEligibleError(member.id)
        due = self.calendar.add_days(on, duration)
        copies = self.inventory.available(book.id, branch_id)
        if not copies:
            raise BookNotAvailableError(book.id)
        copy = copies[0]
        subscription = self.policy.subscriptions.active_for(member.id, on)
        if not member.add_loan(subscription.quota):
            raise MemberNotEligibleError(member.id)
        copy.status = "loaned"
        loan = Loan(self.next_id, book, member, on, due, copy_id=copy.id)
        self.loans[loan.id] = loan
        self.next_id += 1
        return loan
