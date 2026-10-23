class RenewalPolicy:
    def __init__(self, subscriptions, reservations):
        self.subscriptions = subscriptions
        self.reservations = reservations

    def can_extend(self, loan, on):
        if loan.date_retour_reelle is not None or on < loan.date_emprunt:
            return False
        if loan.is_overdue(on):
            return False
        if self.subscriptions.active_for(loan.membre.id, on) is None:
            return False
        return not self.reservations.has_active(loan.livre.id)
