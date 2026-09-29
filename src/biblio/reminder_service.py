class ReminderService:
    def __init__(self, notifications):
        self.notifications = notifications
        self.sent = set()

    def run(self, loans, on, days_before=2):
        count = 0
        for loan in loans:
            if loan.date_retour_reelle is not None:
                continue
            kind = None
            if loan.is_overdue(on):
                kind = "overdue"
            elif (loan.date_retour_prevue - on).days == days_before:
                kind = "due"
            key = (loan.id, on, kind)
            if kind is None or key in self.sent:
                continue
            if kind == "overdue":
                self.notifications.send_overdue_notice(loan, on)
            else:
                self.notifications.send_due_reminder(loan)
            self.sent.add(key)
            count += 1
        return count
