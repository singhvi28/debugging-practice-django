"""Cursor pagination over activity records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Activity:
    id: int
    updated_at: str


_ACTIVITIES: list[Activity] = [
    Activity(id=1, updated_at="2024-01-01T10:00:00Z"),
    Activity(id=2, updated_at="2024-01-01T10:00:00Z"),
    Activity(id=3, updated_at="2024-01-01T10:00:00Z"),
    Activity(id=4, updated_at="2024-01-01T09:00:00Z"),
    Activity(id=5, updated_at="2024-01-01T08:00:00Z"),
]


def reset() -> None:
    pass


def all_activities() -> list[Activity]:
    return sorted(_ACTIVITIES, key=lambda item: (item.updated_at, item.id), reverse=True)


def page_after(cursor_updated_at: str | None, limit: int) -> list[Activity]:
    items = all_activities()
    if cursor_updated_at is None:
        return items[:limit]

    filtered = [item for item in items if item.updated_at < cursor_updated_at]
    return filtered[:limit]
