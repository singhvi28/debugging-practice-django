"""In-memory blog store."""

from __future__ import annotations

from copy import deepcopy

_posts: dict[str, dict] = {}
_comments: dict[str, list[dict]] = {}


def reset() -> None:
    global _posts, _comments
    _posts = {
        "p1": {"id": "p1", "title": "Hello World", "body": "My first post"},
        "p2": {"id": "p2", "title": "FastAPI Tips", "body": "Use dependency injection"},
    }
    _comments = {
        "p1": [],
        "p2": [],
    }


def list_posts(search: str | None = None) -> list[dict]:
    posts = list(_posts.values())
    if not search:
        return deepcopy(posts)
    return deepcopy([p for p in posts if search.lower() in p["title"].lower()])


def get_post(post_id: str) -> dict | None:
    post = _posts.get(post_id)
    return deepcopy(post) if post else None


def create_post(title: str, body: str) -> dict:
    post_id = f"p{len(_posts) + 1}"
    post = {"id": post_id, "title": title, "body": body}
    _posts[post_id] = post
    _comments[post_id] = []
    return deepcopy(post)


def delete_post(post_id: str) -> bool:
    if post_id not in _posts:
        return False
    keys_to_remove = [pid for pid in _posts if pid == post_id]
    for pid in keys_to_remove:
        del _posts[pid]
        _comments.pop(pid, None)
    return True


def list_comments(post_id: str) -> list[dict]:
    return deepcopy(_comments.get(post_id, []))


def add_comment(post_id: str, author: str, text: str) -> dict | None:
    if post_id not in _posts:
        return None
    comment_id = f"c{sum(len(v) for v in _comments.values()) + 1}"
    comment = {"id": comment_id, "post_id": post_id, "author": author, "text": text}
    _comments.setdefault(post_id, []).append(comment)
    return deepcopy(comment)


reset()
