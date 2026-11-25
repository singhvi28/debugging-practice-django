"""In-memory user permissions with a read-through cache."""

_users: dict[str, dict] = {}
_resources: dict[str, dict] = {}
_permission_cache: dict[str, set[str]] = {}


def reset() -> None:
    _users.clear()
    _resources.clear()
    _permission_cache.clear()
    _users["contractor-7"] = {
        "id": "contractor-7",
        "active": True,
        "permissions": {"delete"},
    }
    _resources["doc-42"] = {"id": "doc-42", "title": "Quarterly report"}


def revoke_user(user_id: str) -> bool:
    user = _users.get(user_id)
    if user is None:
        return False
    user["active"] = False
    return True


def get_permissions(user_id: str) -> set[str]:
    if user_id in _permission_cache:
        return _permission_cache[user_id]
    user = _users.get(user_id)
    if user is None or not user["active"]:
        return set()
    perms = set(user["permissions"])
    _permission_cache[user_id] = perms
    return perms


def can_delete(user_id: str) -> bool:
    return "delete" in get_permissions(user_id)
