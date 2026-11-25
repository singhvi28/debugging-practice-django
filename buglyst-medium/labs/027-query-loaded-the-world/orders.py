"""In-memory multi-tenant order store."""

_orders: list[dict] = []


def reset() -> None:
    _orders.clear()
    _orders.extend(
        [
            {"id": "o-1", "tenant_id": "tenant-a", "sku": "widget"},
            {"id": "o-2", "tenant_id": "tenant-a", "sku": "bolt"},
            {"id": "o-3", "tenant_id": "tenant-b", "sku": "gear"},
            {"id": "o-4", "tenant_id": "tenant-b", "sku": "spring"},
            {"id": "o-5", "tenant_id": "tenant-c", "sku": "valve"},
        ]
    )


def list_orders(tenant_id: str) -> list[dict]:
    return list(_orders)
