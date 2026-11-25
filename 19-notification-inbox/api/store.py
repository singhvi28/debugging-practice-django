from copy import deepcopy

_notifications = {
    "n1": {"id": "n1", "title": "Welcome", "body": "Thanks for joining", "read": False},
    "n2": {"id": "n2", "title": "Reminder", "body": "Check your profile", "read": False},
    "n3": {"id": "n3", "title": "Promo", "body": "20% off", "read": True},
}

_unread_count_cache = sum(1 for n in _notifications.values() if not n["read"])


def reset() -> None:
    global _notifications, _unread_count_cache
    _notifications = {
        "n1": {"id": "n1", "title": "Welcome", "body": "Thanks for joining", "read": False},
        "n2": {"id": "n2", "title": "Reminder", "body": "Check your profile", "read": False},
        "n3": {"id": "n3", "title": "Promo", "body": "20% off", "read": True},
    }
    _unread_count_cache = sum(1 for n in _notifications.values() if not n["read"])


def list_notifications() -> list[dict]:
    return deepcopy(list(_notifications.values()))


def get_notification(notification_id: str) -> dict | None:
    notification = _notifications.get(notification_id)
    return deepcopy(notification) if notification else None


def create_notification(title: str, body: str) -> dict:
    notification_id = f"n{len(_notifications) + 1}"
    notification = {
        "id": notification_id,
        "title": title,
        "body": body,
        "read": False,
    }
    _notifications[notification_id] = notification
    global _unread_count_cache
    _unread_count_cache += 1
    return deepcopy(notification)


def mark_read(notification_id: str) -> dict | None:
    notification = _notifications.get(notification_id)
    if notification is None:
        return None
    if not notification["read"]:
        notification["read"] = True
    return deepcopy(notification)


def mark_all_read() -> int:
    count = 0
    for notification in _notifications.values():
        if not notification["read"]:
            notification["read"] = True
            count += 1
    return count


def get_unread_count() -> int:
    return _unread_count_cache


reset()
