from .models.transfer import Transfer


class TransferService:
    def __init__(self, inventory):
        self.inventory = inventory
        self.transfers = {}

    def start(self, transfer_id, copy_id, destination):
        if transfer_id in self.transfers:
            raise ValueError("Transfert déjà enregistré")
        copy = self.inventory.get(copy_id)
        if copy.status != "available" or copy.branch_id == destination:
            raise ValueError("Transfert impossible")
        transfer = Transfer(transfer_id, copy_id, copy.branch_id, destination)
        self.transfers[transfer_id] = transfer
        copy.status = "transit"
        return transfer

    def receive(self, transfer_id):
        transfer = self.transfers[transfer_id]
        if transfer.received:
            return False
        copy = self.inventory.get(transfer.copy_id)
        copy.branch_id = transfer.destination
        copy.status = "available"
        transfer.received = True
        return True
