from datetime import timedelta

from .reservation_queue import ReservationQueue


class ReservationManager:
    def __init__(self, queue=None):
        self.queue = queue if queue is not None else ReservationQueue()

    def reserve(self, book, reservation):
        if reservation.book_id != book.id:
            raise ValueError("Livre incohérent")
        if book.is_available():
            return False
        return self.queue.add(reservation)

    def notify_next(self, book_id, on, pickup_days=3):
        if pickup_days < 0:
            raise ValueError("Délai négatif")
        item = self.queue.next(book_id)
        if item is not None:
            item.status = "ready"
            item.pickup_deadline = on + timedelta(days=pickup_days)
        return item
