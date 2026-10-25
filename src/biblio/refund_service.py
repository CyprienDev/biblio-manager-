from decimal import Decimal

from .models.ledger_entry import LedgerEntry


class RefundService:
    def __init__(self, payments):
        self.payments = payments
        self.refunds = {}

    def refund(self, refund):
        if refund.id in self.refunds:
            if self.refunds[refund.id] != refund:
                raise ValueError("Référence de remboursement réutilisée")
            return False
        payment = self.payments.payments[refund.payment_id]
        total = sum((item.amount for item in self.refunds.values()
                     if item.payment_id == payment.id), Decimal("0"))
        if (not refund.amount.is_finite() or refund.amount <= 0
                or total + refund.amount > payment.amount or refund.day < payment.day):
            raise ValueError("Remboursement invalide")
        entry = LedgerEntry("refund:" + refund.id, payment.account_id,
                            refund.amount, refund.day)
        self.payments.ledger.post(entry)
        self.refunds[refund.id] = refund
        return True
