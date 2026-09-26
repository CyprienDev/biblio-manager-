from .exceptions import LoanNotFoundError


class ReturnService:
    def __init__(self, manager):
        self.manager = manager

    def return_loan(self, loan_id, on):
        if loan_id not in self.manager.loans:
            raise LoanNotFoundError(loan_id)
        loan = self.manager.loans[loan_id]
        if loan.date_retour_reelle is not None:
            return False
        if on < loan.date_emprunt:
            raise ValueError("Retour antérieur à l'emprunt")
        copy = self.manager.inventory.get(loan.copy_id)
        copy.status = "available"
        loan.date_retour_reelle = on
        loan.membre.remove_loan()
        return True
