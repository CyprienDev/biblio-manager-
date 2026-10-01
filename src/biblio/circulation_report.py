from collections import Counter


def active_loans(loans):
    return [loan for loan in loans if loan.date_retour_reelle is None]


def overdue_report(loans, on):
    return [loan for loan in active_loans(loans) if loan.is_overdue(on)]


def most_popular_books(loans, limit=10):
    if limit < 0:
        raise ValueError("Limite négative")
    counts = Counter(loan.livre.id for loan in loans)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
