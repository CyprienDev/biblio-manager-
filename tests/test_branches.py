import unittest
from datetime import date
from biblio.models.branch import Branch
from biblio.branches import BranchRegistry
from biblio.opening_hours import OpeningHours


class Tests(unittest.TestCase):
    def test_registry_and_hours(self):
        registry = BranchRegistry()
        branch = Branch(1, "Centre")
        self.assertTrue(registry.add(branch))
        self.assertFalse(registry.add(branch))
        self.assertIs(registry.get(1), branch)
        self.assertTrue(OpeningHours().is_open(date(2026, 9, 14)))
        self.assertFalse(OpeningHours().is_open(date(2026, 9, 13)))
        with self.assertRaises(ValueError):
            OpeningHours(frozenset())
