"""In-memory forum threads store."""

from __future__ import annotations

from copy import deepcopy

_threads: dict[str, dict] = {}
_replies: dict[str, list[dict]] = {}


def reset() -> None:
    global _threads, _replies
    _threads = {
        "t1": {
            "id": "t1",
            "title": "Welcome",
            "author": "mod",
            "deleted": False,
            "reply_count": 1,
        },
        "t2": {
            "id": "t2",
            "title": "Archived topic",
            "author": "alice",
            "deleted": True,
            "reply_count": 0,
        },
    }
    _replies = {
        "t1": [
            {"id": "rp1", "thread_id": "t1", "author": "bob", "body": "Hello everyone!"},
        ],
        "t2": [],
    }


def list_threads() -> list[dict]:
    return list(deepcopy(t) for t in _threads.values() if not t["deleted"])


def get_thread(thread_id: str) -> dict | None:
    thread = _threads.get(thread_id)
    return deepcopy(thread) if thread and not thread["deleted"] else None


def list_deleted_threads() -> list[dict]:
    return deepcopy([t for t in _threads.values() if t["deleted"]])


def create_thread(title: str, author: str) -> dict:
    thread_id = f"t{len(_threads) + 1}"
    thread = {
        "id": thread_id,
        "title": title,
        "author": author,
        "deleted": False,
        "reply_count": 0,
    }
    _threads[thread_id] = thread
    _replies[thread_id] = []
    return deepcopy(thread)


def create_reply(thread_id: str, author: str, body: str) -> dict | None:
    thread = _threads.get(thread_id)
    if thread is None or thread.get("deleted", False):
        return None
    thread["reply_count"] += 1
    reply_id = f"rp{sum(len(v) for v in _replies.values()) + 1}"
    reply = {"id": reply_id, "thread_id": thread_id, "author": author, "body": body}
    _replies.setdefault(thread_id, []).append(reply)
    return deepcopy(reply)


def list_replies(thread_id: str) -> list[dict]:
    return deepcopy(_replies.get(thread_id, []))


def delete_reply(thread_id: str, reply_id: str) -> bool:
    replies = _replies.get(thread_id)
    if replies is None:
        return False
    _replies[thread_id] = [r for r in replies if r["id"] != reply_id]
    return True


reset()
