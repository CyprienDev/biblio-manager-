from dataclasses import dataclass, field


@dataclass
class InventorySession:
    id: str
    branch_id: int
    expected: set[str]
    seen: set[str] = field(default_factory=set)
    closed: bool = False
