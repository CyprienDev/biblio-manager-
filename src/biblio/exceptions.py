class BookNotAvailableError(Exception):
    pass


class MemberNotEligibleError(Exception):
    pass


class LoanNotFoundError(Exception):
    pass


class BranchNotFoundError(KeyError):
    """Agence inconnue ; reste compatible avec les traitements de KeyError."""


class InventoryError(ValueError):
    """Opération invalide sur une session d'inventaire."""
