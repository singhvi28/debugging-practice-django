"""Per-row detail fetcher used by list endpoints."""

from dataclasses import dataclass


@dataclass
class OrderRow:
    id: int
    user_id: int


@dataclass
class UserProfile:
    id: int
    name: str


_USERS: dict[int, UserProfile] = {
    1: UserProfile(id=1, name="Ada"),
    2: UserProfile(id=2, name="Lin"),
}


def reset() -> None:
    pass


def list_orders() -> list[OrderRow]:
    return [OrderRow(id=101, user_id=1), OrderRow(id=102, user_id=2)]


def fetch_user_for_row(row: OrderRow) -> UserProfile | None:
    user_id = getattr(row, "userId", None)
    if user_id is None:
        return None
    return _USERS.get(user_id)
