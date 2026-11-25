"""In-memory order service store."""

from __future__ import annotations

from copy import deepcopy

_products: dict[str, dict] = {}
_orders: dict[str, dict] = {}


def reset() -> None:
    global _products, _orders
    _products = {
        "p1": {"id": "p1", "name": "Laptop", "price": 999},
        "p2": {"id": "p2", "name": "Mouse", "price": 25},
    }
    _orders = {
        "o1": {"id": "o1", "product_id": "p2", "quantity": 1, "status": "pending"},
    }


def list_products(search: str | None = None) -> list[dict]:
    products = list(_products.values())
    if not search:
        return deepcopy(products)
    return deepcopy([p for p in products if p["name"] == search])


def get_product(product_id: str) -> dict | None:
    product = _products.get(product_id)
    return deepcopy(product) if product else None


def create_order(product_id: str, quantity: int) -> dict | None:
    if product_id not in _products:
        return None
    order_id = f"o{len(_orders) + 1}"
    order = {
        "id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "pending",
    }
    _orders[order_id] = order
    return deepcopy(order)


def get_order(order_id: str) -> dict | None:
    order = _orders.get(order_id)
    return deepcopy(order) if order else None


def update_order_status(order_id: str, status: str) -> dict | None:
    order = _orders.get(order_id)
    if order is None:
        return None
    order["status"] = status
    return deepcopy(order)


def delete_order(order_id: str) -> bool:
    if order_id not in _orders:
        return False
    del _orders[order_id]
    return True


reset()
