from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class FinePolicy:
    daily_rate: Decimal = Decimal("0.50")
    maximum: Decimal = Decimal("20.00")

    def __post_init__(self):
        if self.daily_rate < 0 or self.maximum < 0:
            raise ValueError("Tarif négatif")
