from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    id: int
    nom: str
