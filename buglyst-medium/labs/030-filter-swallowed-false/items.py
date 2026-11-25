"""In-memory item catalog with soft-delete filtering."""

_items: list[dict] = []


def reset() -> None:
    _items.clear()
    _items.extend(
        [
            {"id": "item-1", "name": "Active widget", "deleted": False},
            {"id": "item-2", "name": "Retired widget", "deleted": True},
            {"id": "item-3", "name": "Active bolt", "deleted": False},
        ]
    )


def parse_include_deleted(raw: str | None) -> bool:
    if raw:
        return True
    return False


def list_items(include_deleted: bool) -> list[dict]:
    if include_deleted:
        return list(_items)
    return [item for item in _items if not item["deleted"]]
