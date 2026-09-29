class PickupService:
    def expire(self, reservation, on):
        if (reservation.status == "ready"
                and reservation.pickup_deadline is not None
                and on > reservation.pickup_deadline):
            reservation.status = "expired"
            return True
        return False

    def collect(self, reservation, on):
        self.expire(reservation, on)
        if reservation.status != "ready":
            return False
        reservation.status = "collected"
        return True
