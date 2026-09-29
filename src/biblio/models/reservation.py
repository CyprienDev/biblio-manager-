from dataclasses import dataclass
from datetime import date


@dataclass
class Reservation:
    id: str
    book_id: int
    member_id: int
    created: date
    status: str = "waiting"
    pickup_deadline: date | None = None
