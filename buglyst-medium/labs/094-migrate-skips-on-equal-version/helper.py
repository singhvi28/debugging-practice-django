"""Schema migration runner with version tracking."""

MIGRATIONS: list[dict[str, str]] = [
    {"version": "1", "column": "id"},
    {"version": "2", "column": "email"},
    {"version": "3", "column": "preferences"},
]

_schema_columns: set[str] = set()


def reset() -> None:
    global _schema_columns
    _schema_columns = set()


def current_schema() -> set[str]:
    return set(_schema_columns)


def run_migrations(current_version: str) -> dict:
    """Apply pending migrations and return the resulting schema version."""
    version = current_version
    applied: list[str] = []

    for migration in MIGRATIONS:
        if version >= migration["version"]:
            continue
        _schema_columns.add(migration["column"])
        applied.append(migration["version"])
        version = migration["version"]

    return {"version": version, "applied": applied, "columns": sorted(_schema_columns)}
