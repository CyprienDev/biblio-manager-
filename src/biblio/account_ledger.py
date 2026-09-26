from decimal import Decimal


class AccountLedger:
    def __init__(self):
        self.accounts = {}
        self.entries = {}

    def register(self, account):
        self.accounts.setdefault(account.member_id, account)

    def post(self, entry):
        if entry.account_id not in self.accounts:
            raise KeyError(entry.account_id)
        if not isinstance(entry.amount, Decimal) or not entry.amount.is_finite():
            raise ValueError("Montant décimal fini requis")
        if entry.amount != entry.amount.quantize(Decimal("0.01")):
            raise ValueError("Précision supérieure au centime")
        if entry.id in self.entries:
            if self.entries[entry.id] != entry:
                raise ValueError("Référence réutilisée")
            return False
        self.entries[entry.id] = entry
        return True

    def balance(self, account_id):
        if account_id not in self.accounts:
            raise KeyError(account_id)
        return sum((entry.amount for entry in self.entries.values()
                    if entry.account_id == account_id), Decimal("0"))
