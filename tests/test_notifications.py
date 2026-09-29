import unittest
from datetime import timedelta
from support import fixture
from biblio.notifications import NotificationService
from biblio.reminder_service import ReminderService


class Tests(unittest.TestCase):
    def test_due_overdue_and_duplicate(self):
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        notifications = NotificationService()
        service = ReminderService(notifications)
        before = loan.date_retour_prevue - timedelta(days=2)
        self.assertEqual(service.run([loan], before), 1)
        self.assertEqual(service.run([loan], before), 0)
        self.assertEqual(service.run([loan], loan.date_retour_prevue + timedelta(days=1)), 1)
        self.assertEqual(len(notifications.messages), 2)
        self.assertEqual(notifications.messages[0][0], member.email)
        loan.date_retour_reelle = loan.date_retour_prevue
        self.assertEqual(service.run([loan], loan.date_retour_prevue + timedelta(days=2)), 0)
