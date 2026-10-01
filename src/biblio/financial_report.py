from decimal import Decimal


def balances(ledger):
    return {account_id: ledger.balance(account_id) for account_id in ledger.accounts}


def total_debt(ledger):
    return sum((max(Decimal("0"), amount) for amount in balances(ledger).values()),
               Decimal("0"))
