class ReservationQueue:
    def __init__(self):
        self.items = []

    def add(self, reservation):
        if any(item.id == reservation.id for item in self.items):
            raise ValueError("Identifiant déjà utilisé")
        if any(item.book_id == reservation.book_id
               and item.member_id == reservation.member_id
               and item.status in {"waiting", "ready"} for item in self.items):
            return False
        self.items.append(reservation)
        return True

    def cancel(self, reservation_id):
        for item in self.items:
            if item.id == reservation_id and item.status in {"waiting", "ready"}:
                item.status = "cancelled"
                return True
        return False

    def next(self, book_id):
        return next((item for item in self.items
                     if item.book_id == book_id and item.status == "waiting"), None)

    def has_active(self, book_id):
        return any(item.book_id == book_id and item.status in {"waiting", "ready"}
                   for item in self.items)
