"""In-memory bookstore store."""

from __future__ import annotations

from copy import deepcopy

_books: dict[str, dict] = {}
_carts: dict[str, dict] = {}


def reset() -> None:
    global _books, _carts
    _books = {
        "b1": {"id": "b1", "title": "The Hobbit", "author": "J.R.R. Tolkien"},
        "b2": {"id": "b2", "title": "Dune", "author": "Frank Herbert"},
        "b3": {"id": "b3", "title": "Neuromancer", "author": "William Gibson"},
    }
    _carts = {
        "c1": {"id": "c1", "items": [{"book_id": "b1"}]},
    }


def list_books(search: str | None = None) -> list[dict]:
    books = list(_books.values())
    if not search:
        return deepcopy(books)
    return deepcopy([b for b in books if b["title"] == search])


def get_book(book_id: str) -> dict | None:
    book = _books.get(book_id)
    return deepcopy(book) if book else None


def create_book(title: str, author: str) -> dict:
    book_id = f"b{len(_books) + 1}"
    book = {"id": book_id, "title": title, "author": author}
    _books[book_id] = book
    return deepcopy(book)


def delete_book(book_id: str) -> bool:
    if book_id not in _books:
        return False
    del _books[book_id]
    return True


def get_cart(cart_id: str) -> dict | None:
    cart = _carts.get(cart_id)
    return deepcopy(cart) if cart else None


def add_to_cart(cart_id: str, book_id: str) -> dict | None:
    cart = _carts.get(cart_id)
    if cart is None:
        return None
    cart["items"].append({"book_id": book_id})
    return deepcopy(cart)


def remove_from_cart(cart_id: str, book_id: str) -> bool:
    cart = _carts.get(cart_id)
    if cart is None:
        return False
    cart["items"] = [i for i in cart["items"] if i["book_id"] == book_id]
    return True


reset()
