"""In-memory file metadata store."""

from __future__ import annotations

from copy import deepcopy

_files: dict[str, dict] = {}


def reset() -> None:
    global _files
    _files = {
        "f1": {
            "id": "f1",
            "title": "Quarterly Report",
            "mime_type": "application/pdf",
            "tags": ["finance", "Q2"],
        },
        "f2": {
            "id": "f2",
            "title": "Team Photo",
            "mime_type": "image/jpeg",
            "tags": ["photo"],
        },
    }


def list_files(tag: str | None = None) -> list[dict]:
    files = list(_files.values())
    if tag is None:
        return deepcopy(files)
    return deepcopy([f for f in files if tag in f["tags"]])


def get_file(file_id: str) -> dict | None:
    file = _files.get(file_id)
    return deepcopy(file) if file else None


def create_file(title: str, mime_type: str) -> dict:
    file_id = f"f{len(_files) + 1}"
    file = {"id": file_id, "title": title, "mime_type": mime_type, "tags": []}
    _files[file_id] = file
    return deepcopy(file)


def update_file(file_id: str, title: str) -> dict | None:
    file = _files.get(file_id)
    if file is None:
        return None
    file["name"] = title
    return deepcopy(file)


def add_tag(file_id: str, tag: str) -> dict | None:
    file = _files.get(file_id)
    if file is None:
        return None
    file["tags"].append(tag)
    return deepcopy(file)


reset()
