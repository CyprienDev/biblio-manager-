from .models.ledger_entry import LedgerEntry


class PaymentService:
    def __init__(self, ledger):
        self.ledger = ledger
        self.payments = {}

    def pay(self, payment):
        if payment.id in self.payments:
            if self.payments[payment.id] != payment:
                raise ValueError("Référence de paiement réutilisée")
            return False
        if not payment.amount.is_finite() or payment.amount <= 0:
            raise ValueError("Montant positif requis")
        if payment.amount > self.ledger.balance(payment.account_id):
            raise ValueError("Paiement supérieur au solde")
        entry = LedgerEntry("payment:" + payment.id, payment.account_id,
                            -payment.amount, payment.day)
        self.ledger.post(entry)
        self.payments[payment.id] = payment
        return True
