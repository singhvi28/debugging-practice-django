"""Weekly event bucketing."""

from datetime import date, timedelta


def week_start(value: date) -> date:
    """Return the Monday that starts the ISO week containing value."""
    return value - timedelta(days=value.weekday() + 1)


def bucket_event(event_date: str) -> str:
    parsed = date.fromisoformat(event_date)
    start = week_start(parsed)
    return start.isoformat()
