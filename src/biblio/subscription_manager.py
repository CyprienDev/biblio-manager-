from .models.subscription import Subscription


class SubscriptionManager:
    def __init__(self):
        self.subscriptions = {}

    def register(self, subscription: Subscription):
        self.subscriptions[subscription.member_id] = subscription

    def active_for(self, member_id, on):
        subscription = self.subscriptions.get(member_id)
        if subscription is not None and subscription.is_active(on):
            return subscription
        return None
