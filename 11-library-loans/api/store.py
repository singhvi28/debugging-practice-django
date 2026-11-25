"""In-memory library loans store."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta

MAX_ACTIVE_LOANS = 2

_books: dict[str, dict] = {}
_loans: dict[str, dict] = {}
_pending_loans: dict[str, dict] = {}

_REFERENCE_DATE = date(2026, 8, 10)


def reset() -> None:
    global _books, _loans, _pending_loans
    _books = {
        "bk1": {"id": "bk1", "title": "Dune", "author": "Frank Herbert"},
        "bk2": {"id": "bk2", "title": "1984", "author": "George Orwell"},
    }
    _loans = {
        "ln1": {
            "id": "ln1",
            "book_id": "bk2",
            "user_id": "user1",
            "status": "active",
            "due_date": "2026-08-09",
            "returned_at": None,
        },
        "ln2": {
            "id": "ln2",
            "book_id": "bk1",
            "user_id": "user2",
            "status": "active",
            "due_date": "2026-08-20",
            "returned_at": None,
        },
        "ln3": {
            "id": "ln3",
            "book_id": "bk2",
            "user_id": "user2",
            "status": "active",
            "due_date": "2026-08-22",
            "returned_at": None,
        },
    }
    _pending_loans = {}


def list_books() -> list[dict]:
    return deepcopy(list(_books.values()))


def get_book(book_id: str) -> dict | None:
    book = _books.get(book_id)
    return deepcopy(book) if book else None


def list_loans() -> list[dict]:
    return deepcopy(list(_loans.values()))


def list_overdue_loans() -> list[dict]:
    overdue = []
    for loan in _loans.values():
        if loan["status"] == "active" and loan["due_date"] < _REFERENCE_DATE.isoformat():
            overdue.append(loan)
    return deepcopy(overdue)


def count_active_loans(user_id: str) -> int:
    return sum(
        1 for loan in _loans.values() if loan["user_id"] == user_id and loan["status"] == "active"
    )


def schedule_create_loan(book_id: str, user_id: str) -> dict:
    loan_id = f"ln{len(_loans) + len(_pending_loans) + 1}"
    due_date = (_REFERENCE_DATE + timedelta(days=14)).isoformat()
    loan = {
        "id": loan_id,
        "book_id": book_id,
        "user_id": user_id,
        "status": "active",
        "due_date": due_date,
        "returned_at": None,
    }
    _pending_loans[loan_id] = loan
    return deepcopy(loan)


def create_loan(book_id: str, user_id: str) -> dict:
    return schedule_create_loan(book_id, user_id)


def return_loan(loan_id: str) -> dict | None:
    loan = _loans.get(loan_id)
    if loan is None:
        return None
    loan["returned_at"] = _REFERENCE_DATE.isoformat()
    return deepcopy(loan)


reset()
