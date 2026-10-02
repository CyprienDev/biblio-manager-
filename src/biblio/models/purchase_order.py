from dataclasses import dataclass

from .book import Book


@dataclass
class PurchaseOrder:
    id: str
    supplier_id: str
    book: Book
    quantity: int
    branch_id: int
    received: int = 0

    def __post_init__(self):
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ValueError("Quantité entière positive requise")
        if not 0 <= self.received <= self.quantity:
            raise ValueError("Quantité reçue invalide")

    @property
    def remaining(self):
        return self.quantity - self.received
