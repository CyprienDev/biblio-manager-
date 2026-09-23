from .models.branch import Branch


class BranchRegistry:
    def __init__(self):
        self.branches = {}

    def add(self, branch: Branch) -> bool:
        if branch.id in self.branches:
            return False
        self.branches[branch.id] = branch
        return True

    def get(self, branch_id: int) -> Branch:
        return self.branches[branch_id]
