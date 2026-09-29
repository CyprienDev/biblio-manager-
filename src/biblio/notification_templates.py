def due_reminder(loan):
    return f"Retour de {loan.livre.titre} prévu le {loan.date_retour_prevue.isoformat()}"


def overdue_notice(loan, on):
    return f"{loan.livre.titre} : {loan.days_overdue(on)} jour(s) de retard"


def reservation_notice(reservation):
    return f"Réservation {reservation.id} disponible jusqu'au {reservation.pickup_deadline}"
