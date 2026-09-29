from . import notification_templates as templates


class NotificationService:
    def __init__(self):
        self.messages = []

    def send_due_reminder(self, loan):
        message = (loan.membre.email, templates.due_reminder(loan))
        self.messages.append(message)
        return message

    def send_overdue_notice(self, loan, on):
        message = (loan.membre.email, templates.overdue_notice(loan, on))
        self.messages.append(message)
        return message

    def send_reservation_notice(self, reservation, member):
        if member.id != reservation.member_id:
            raise ValueError("Destinataire incorrect")
        message = (member.email, templates.reservation_notice(reservation))
        self.messages.append(message)
        return message
