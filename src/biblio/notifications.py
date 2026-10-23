from . import notification_templates as templates


class NotificationService:
    def __init__(self):
        self.messages = []

    def send_due_reminder(self, loan):
        message = templates.addressed_to(loan.membre, templates.due_reminder(loan))
        self.messages.append(message)
        return message

    def send_overdue_notice(self, loan, on):
        message = templates.addressed_to(loan.membre, templates.overdue_notice(loan, on))
        self.messages.append(message)
        return message

    def send_reservation_notice(self, reservation, member):
        if member.id != reservation.member_id:
            raise ValueError("Destinataire incorrect")
        message = templates.addressed_to(member, templates.reservation_notice(reservation))
        self.messages.append(message)
        return message
