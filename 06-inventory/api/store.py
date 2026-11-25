"""In-memory inventory store."""

from __future__ import annotations

import asyncio
from copy import deepcopy

_products: dict[str, dict] = {}
_moves: dict[str, list[dict]] = {}


def reset() -> None:
    global _products, _moves
    _products = {
        "pr1": {"id": "pr1", "name": "Widget A", "qty": 10},
        "pr2": {"id": "pr2", "name": "Gadget B", "qty": 5},
    }
    _moves = {
        "pr1": [],
        "pr2": [],
    }


def list_products(search: str | None = None) -> list[dict]:
    products = list(_products.values())
    if not search:
        return deepcopy(products)
    return deepcopy([p for p in products if p["name"] == search])


def get_product(product_id: str) -> dict | None:
    product = _products.get(product_id)
    return deepcopy(product) if product else None


async def create_product(name: str, qty: int) -> dict:
    await asyncio.sleep(0)
    product_id = f"pr{len(_products) + 1}"
    product = {"id": product_id, "name": name, "qty": qty}
    _products[product_id] = product
    _moves[product_id] = []
    return deepcopy(product)


def adjust_stock(product_id: str, delta: int) -> dict | None:
    product = _products.get(product_id)
    if product is None:
        return None
    new_qty = product["qty"] + delta
    product["qty"] = new_qty
    move_id = f"mv{sum(len(v) for v in _moves.values()) + 1}"
    _moves[product_id].append(
        {"id": move_id, "product_id": product_id, "delta": delta, "qty_after": new_qty}
    )
    return deepcopy(product)


def list_moves(product_id: str) -> list[dict] | None:
    if product_id not in _products:
        return None
    return deepcopy(_moves.get(product_id, []))


def delete_product(product_id: str) -> bool:
    if product_id not in _products:
        return False
    del _products[product_id]
    _moves.pop(product_id, None)
    return True


reset()
