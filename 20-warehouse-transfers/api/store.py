import threading
from copy import deepcopy

_locations = {
    "wh_east": {"id": "wh_east", "name": "East Warehouse"},
    "wh_west": {"id": "wh_west", "name": "West Warehouse"},
}

_stock = {
    "wh_east": {"SKU-100": 50, "SKU-200": 10},
    "wh_west": {"SKU-100": 5, "SKU-200": 0},
}

_transfers: dict[str, dict] = {}


def reset() -> None:
    global _locations, _stock, _transfers
    _locations = {
        "wh_east": {"id": "wh_east", "name": "East Warehouse"},
        "wh_west": {"id": "wh_west", "name": "West Warehouse"},
    }
    _stock = {
        "wh_east": {"SKU-100": 50, "SKU-200": 10},
        "wh_west": {"SKU-100": 5, "SKU-200": 0},
    }
    _transfers = {}


def list_locations() -> list[dict]:
    return deepcopy(list(_locations.values()))


def get_location(location_id: str) -> dict | None:
    location = _locations.get(location_id)
    return deepcopy(location) if location else None


def get_stock(location_id: str) -> dict | None:
    if location_id not in _locations:
        return None
    return deepcopy(_stock.get(location_id, {}))


def get_sku_quantity(location_id: str, sku: str) -> int | None:
    if location_id not in _locations:
        return None
    return _stock.get(location_id, {}).get(sku, 0)


def add_dest_stock(to_location_id: str, sku: str, quantity: int) -> None:
    dest = _stock.setdefault(to_location_id, {})
    dest[sku] = dest.get(sku, 0) + quantity


def apply_transfer(from_location_id: str, to_location_id: str, sku: str, quantity: int) -> bool:
    source = _stock.setdefault(from_location_id, {})
    if source.get(sku, 0) < quantity:
        return False
    source[sku] = source.get(sku, 0) - quantity
    return True


def count_transfers() -> int:
    return len(_transfers)


def commit_transfer_async(transfer: dict) -> threading.Thread:
    def _work() -> None:
        _transfers[transfer["id"]] = transfer

    return threading.Thread(target=_work)


def get_transfer(transfer_id: str) -> dict | None:
    transfer = _transfers.get(transfer_id)
    return deepcopy(transfer) if transfer else None


reset()
