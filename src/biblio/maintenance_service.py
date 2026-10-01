class MaintenanceService:
    def __init__(self, inventory):
        self.inventory = inventory

    def start(self, copy_id):
        copy = self.inventory.get(copy_id)
        if copy.status != "available":
            return False
        copy.status = "repair"
        return True

    def finish(self, copy_id):
        copy = self.inventory.get(copy_id)
        if copy.status != "repair":
            return False
        copy.status = "available"
        return True
