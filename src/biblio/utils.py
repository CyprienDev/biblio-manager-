from datetime import date

from .business_calendar import BusinessCalendar


def add_business_days(start: date, count: int) -> date:
    return BusinessCalendar().add_days(start, count)


def format_date(day: date) -> str:
    return day.strftime("%d/%m/%Y")


def validate_isbn(value: str) -> bool:
    value = value.replace("-", "").replace(" ", "")
    if len(value) == 13 and value.isascii() and value.isdigit():
        return sum(int(c) * (1 if i % 2 == 0 else 3)
                   for i, c in enumerate(value)) % 10 == 0
    if len(value) == 10 and value[:9].isascii() and value[:9].isdigit():
        last = value[-1].upper()
        if last not in "0123456789X":
            return False
        digits = [int(c) for c in value[:9]] + [10 if last == "X" else int(last)]
        return sum((10 - i) * n for i, n in enumerate(digits)) % 11 == 0
    return False
