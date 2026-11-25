"""In-memory order and inventory store."""

_orders: list[dict] = []
_inventory: dict[str, int] = {"widget": 5, "gadget": 3}


def reset() -> None:
    _orders.clear()
    _inventory["widget"] = 5
    _inventory["gadget"] = 3


def deduct(sku: str, quantity: int) -> None:
    available = _inventory.get(sku, 0)
    if available < quantity:
        raise ValueError(f"insufficient stock for {sku}")
    _inventory[sku] = available - quantity


def save_order(order_id: str, items: list[dict]) -> None:
    _orders.append({"order_id": order_id, "items": items})


def list_orders() -> list[dict]:
    return list(_orders)


def inventory_snapshot() -> dict[str, int]:
    return dict(_inventory)
