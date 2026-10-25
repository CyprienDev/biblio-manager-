class BorrowingPolicy:
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

    def can_borrow(self, member, on):
        quota = self.subscriptions.quota_for(member.id, on)
        return quota > 0 and member.can_borrow(quota)
