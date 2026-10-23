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

    def test_exact_message_contents_and_recipient(self):
        from biblio.models.reservation import Reservation
        day, book, member, manager = fixture()
        loan = manager.create_loan(book, member, day)
        service = NotificationService()
        self.assertEqual(service.send_due_reminder(loan),
                         (member.email, f"Retour de Dune prévu le {loan.date_retour_prevue.isoformat()}"))
        self.assertEqual(service.send_overdue_notice(loan, loan.date_retour_prevue + timedelta(days=3)),
                         (member.email, "Dune : 3 jour(s) de retard"))
        reservation = Reservation("r", book.id, member.id, day)
        reservation.pickup_deadline = day + timedelta(days=2)
        self.assertEqual(service.send_reservation_notice(reservation, member),
                         (member.email, f"Réservation r disponible jusqu'au {reservation.pickup_deadline}"))
        reservation.member_id = 999
        with self.assertRaises(ValueError):
            service.send_reservation_notice(reservation, member)
        self.assertEqual(len(service.messages), 3)
