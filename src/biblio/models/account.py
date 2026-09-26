from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    member_id: int
