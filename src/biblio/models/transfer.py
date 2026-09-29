from dataclasses import dataclass


@dataclass
class Transfer:
    id: str
    copy_id: str
    source: int
    destination: int
    received: bool = False
