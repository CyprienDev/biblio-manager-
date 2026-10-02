from .models.copy import Copy


class ReceivingService:
    def __init__(self, acquisitions, inventory):
        self.acquisitions = acquisitions
        self.inventory = inventory
        self.receipts = {}

    def receive(self, receipt_id, order_id, quantity):
        if not isinstance(receipt_id, str) or not receipt_id:
            raise ValueError("Référence de réception requise")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantité entière positive requise")
        request = (order_id, quantity)
        if receipt_id in self.receipts:
            if self.receipts[receipt_id] != request:
                raise ValueError("Référence de réception réutilisée")
            return False
        order = self.acquisitions.orders[order_id]
        if quantity > order.remaining:
            raise ValueError("Réception supérieure à la commande")
        copies = [Copy(f"receipt:{receipt_id}:{i + 1}", order.book.id, order.branch_id)
                  for i in range(quantity)]
        self.inventory.add_copies(order.book, copies)
        order.received += quantity
        self.receipts[receipt_id] = request
        return True
