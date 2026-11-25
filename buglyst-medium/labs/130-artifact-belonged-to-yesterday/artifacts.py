"""CI artifact storage."""

_first_url: str | None = None
_uploads: dict[str, str] = {}


def reset() -> None:
    global _first_url
    _first_url = None
    _uploads.clear()


def upload_artifact(run_id: str, filename: str) -> str:
    global _first_url
    url = f"https://artifacts.example/runs/{run_id}/{filename}"
    _uploads[run_id] = url
    if _first_url is None:
        _first_url = url
    return _first_url


def artifact_for_run(run_id: str) -> str | None:
    return _uploads.get(run_id)
