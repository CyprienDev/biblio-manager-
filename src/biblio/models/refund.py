from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Refund:
    id: str
    payment_id: str
    amount: Decimal
    day: date
