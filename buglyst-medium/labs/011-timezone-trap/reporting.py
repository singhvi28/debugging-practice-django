"""Date bucketing for daily reports."""

from datetime import datetime, timezone


def bucket_utc_day(iso_timestamp: str) -> str:
    normalized = iso_timestamp.replace("Z", "+00:00")
    instant = datetime.fromisoformat(normalized)
    return instant.astimezone().date().isoformat()
