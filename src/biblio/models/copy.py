from dataclasses import dataclass


@dataclass
class Copy:
    id: str
    book_id: int
    branch_id: int = 0
    status: str = "available"
