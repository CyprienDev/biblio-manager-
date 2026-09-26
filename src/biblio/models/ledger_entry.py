from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class LedgerEntry:
    id: str
    account_id: int
    amount: Decimal
    day: date
