from .exceptions import MemberNotEligibleError
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
        copy = copies[0] if copies else None
        subscription = self.policy.subscriptions.active_for(member.id, on)
        if not member.add_loan(subscription.quota):
            raise MemberNotEligibleError(member.id)
        if copy is not None:
            copy.status = "loaned"
        loan = Loan(self.next_id, book, member, on, due, copy_id=copy.id if copy is not None else None)
        self.loans[loan.id] = loan
        self.next_id += 1
        return loan

    def extend_loan(self, loan_id, on, renewal_policy, days=5):
        if days <= 0:
            raise ValueError("Prolongation positive requise")
        loan = self.loans[loan_id]
        if not renewal_policy.can_extend(loan, on):
            return False
        loan.date_retour_prevue = self.calendar.add_days(loan.date_retour_prevue, days)
        return True
