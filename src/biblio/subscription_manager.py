from .models.subscription import Subscription


class SubscriptionManager:
    def __init__(self):
        self.subscriptions = {}

    def register(self, subscription: Subscription):
        self.subscriptions[subscription.member_id] = subscription

    def quota_for(self, member_id, on):
        subscription = self.active_for(member_id, on)
        return subscription.quota if subscription is not None else 0

    def active_for(self, member_id, on):
        subscription = self.subscriptions.get(member_id)
        if subscription is not None and subscription.is_active(on):
            return subscription
        return None
