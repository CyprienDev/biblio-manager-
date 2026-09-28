from decimal import Decimal

from .fine_policy import FinePolicy


class FineCalculator:
    def __init__(self, policy=None):
        self.policy = policy or FinePolicy()

    def calculate_fine(self, loan, on=None):
        days = loan.days_overdue(on)
        return min(Decimal(days) * self.policy.daily_rate, self.policy.maximum)
