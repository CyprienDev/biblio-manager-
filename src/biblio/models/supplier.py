from dataclasses import dataclass


@dataclass(frozen=True)
class Supplier:
    id: str
    name: str
