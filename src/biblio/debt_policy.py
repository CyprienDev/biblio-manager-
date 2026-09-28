from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DebtPolicy:
    threshold: Decimal = Decimal("5")
    delay_days: int = 7

    def __post_init__(self):
        if self.threshold < 0 or self.delay_days < 0:
            raise ValueError("Règle de relance invalide")

    def should_remind(self, balance, due, on):
        return balance >= self.threshold and (on - due).days >= self.delay_days
