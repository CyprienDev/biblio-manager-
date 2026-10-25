from decimal import Decimal


def balances(ledger):
    return {account_id: ledger.balance(account_id) for account_id in ledger.accounts}


def total_debt(ledger):
    debts = (amount for amount in balances(ledger).values() if amount > 0)
    return sum(debts, Decimal("0"))
