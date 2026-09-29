class RenewalPolicy:
    def __init__(self, subscriptions, reservations):
        self.subscriptions = subscriptions
        self.reservations = reservations

    def can_extend(self, loan, on):
        return (loan.date_retour_reelle is None
                and on >= loan.date_emprunt
                and not loan.is_overdue(on)
                and self.subscriptions.active_for(loan.membre.id, on) is not None
                and not self.reservations.has_active(loan.livre.id))
