from .models.inventory_session import InventorySession


class InventoryService:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sessions = {}

    def start(self, session_id, branch_id):
        if session_id in self.sessions:
            raise ValueError("Session déjà enregistrée")
        expected = {copy.id for copy in self.inventory.copies.values()
                    if copy.branch_id == branch_id and copy.status == "available"}
        session = InventorySession(session_id, branch_id, expected)
        self.sessions[session_id] = session
        return session

    def scan(self, session_id, copy_id):
        session = self.sessions[session_id]
        if session.closed or copy_id not in session.expected:
            raise ValueError("Scan invalide")
        session.seen.add(copy_id)

    def close(self, session_id):
        session = self.sessions[session_id]
        if session.closed:
            return set()
        missing = session.expected - session.seen
        for copy_id in missing:
            copy = self.inventory.get(copy_id)
            if copy.branch_id == session.branch_id and copy.status == "available":
                copy.status = "lost"
        session.closed = True
        return missing
