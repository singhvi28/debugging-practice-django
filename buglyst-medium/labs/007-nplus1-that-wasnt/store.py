"""In-memory order store with work-unit accounting."""

ORDERS = [
    {"id": "o1", "customer": "alice"},
    {"id": "o2", "customer": "bob"},
    {"id": "o3", "customer": "carol"},
]

ITEMS_BY_ORDER = {
    "o1": [{"sku": "a"}, {"sku": "b"}, {"sku": "c"}],
    "o2": [{"sku": "d"}, {"sku": "e"}],
    "o3": [{"sku": "f"}, {"sku": "g"}, {"sku": "h"}, {"sku": "i"}],
}

_work_units = 0
_query_count = 0


def reset() -> None:
    global _work_units, _query_count
    _work_units = 0
    _query_count = 0


def list_orders() -> list[dict]:
    global _query_count
    _query_count += 1
    return [order.copy() for order in ORDERS]


def load_items_for_order(order_id: str) -> list[dict]:
    global _work_units
    items = ITEMS_BY_ORDER.get(order_id, [])
    # Simulates per-item graph expansion work in Python
    for item in items:
        _work_units += len(ITEMS_BY_ORDER)
    return [item.copy() for item in items]


def get_work_units() -> int:
    return _work_units


def get_query_count() -> int:
    return _query_count
