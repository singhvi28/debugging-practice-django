"""User registration store."""

import threading
import time

_lock = threading.Lock()
_users: dict[str, dict] = {}
_counter = 0


class DuplicateEmailError(Exception):
    pass


def reset() -> None:
    global _counter
    with _lock:
        _users.clear()
        _counter = 0


def user_count() -> int:
    return len(_users)


def register(email: str) -> dict:
    global _counter
    if email in _users:
        raise DuplicateEmailError(email)
    time.sleep(0.05)
    _counter += 1
    user = {"id": _counter, "email": email}
    _users[email] = user
    return user
