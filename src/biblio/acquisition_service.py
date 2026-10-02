from .models.purchase_order import PurchaseOrder


class AcquisitionService:
    def __init__(self, branches):
        self.branches = branches
        self.suppliers = {}
        self.orders = {}

    def register_supplier(self, supplier):
        if supplier.id in self.suppliers:
            if self.suppliers[supplier.id] != supplier:
                raise ValueError("Fournisseur déjà enregistré")
            return False
        self.suppliers[supplier.id] = supplier
        return True

    def place_order(self, order_id, supplier_id, book, quantity, branch_id):
        if order_id in self.orders:
            raise ValueError("Commande déjà enregistrée")
        if supplier_id not in self.suppliers:
            raise KeyError(supplier_id)
        self.branches.get(branch_id)
        order = PurchaseOrder(order_id, supplier_id, book, quantity, branch_id)
        self.orders[order_id] = order
        return order
