import unittest
from datetime import date
from biblio.business_calendar import BusinessCalendar
from biblio.utils import add_business_days, format_date, validate_isbn


class Tests(unittest.TestCase):
    def test_weekend_closure_and_zero(self):
        friday = date(2026, 9, 11)
        self.assertEqual(add_business_days(friday, 1), date(2026, 9, 14))
        calendar = BusinessCalendar(closures={date(2026, 9, 14)})
        self.assertEqual(calendar.add_days(friday, 1), date(2026, 9, 15))
        self.assertEqual(calendar.add_days(friday, 0), friday)
        with self.assertRaises(ValueError):
            calendar.add_days(friday, -1)

    def test_isbn_and_format(self):
        self.assertTrue(validate_isbn("978-0-441-17271-9"))
        self.assertTrue(validate_isbn("0-8044-2957-X"))
        self.assertFalse(validate_isbn("9780441172718"))
        self.assertFalse(validate_isbn("abcdefghij"))
        self.assertEqual(format_date(date(2026, 9, 11)), "11/09/2026")

    def test_consecutive_exceptional_closures(self):
        calendar = BusinessCalendar(closures={date(2026, 9, 14), date(2026, 9, 15)})
        self.assertFalse(calendar.is_open(date(2026, 9, 14)))
        self.assertEqual(calendar.add_days(date(2026, 9, 11), 1), date(2026, 9, 16))
        self.assertEqual(calendar.add_days(date(2026, 9, 11), 2), date(2026, 9, 17))
