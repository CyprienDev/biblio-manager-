class BorrowingPolicy:
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

    def can_borrow(self, member, on):
        subscription = self.subscriptions.active_for(member.id, on)
        return (subscription is not None
                and member.can_borrow(subscription.quota))
