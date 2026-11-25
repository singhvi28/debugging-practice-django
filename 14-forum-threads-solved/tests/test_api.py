import json

from api import store
from tests.conftest import AUTH


def test_list_threads_excludes_deleted(client):
    res = client.get("/threads")
    assert res.status_code == 200
    ids = [thread["id"] for thread in res.json()]
    assert "t1" in ids
    assert "t2" not in ids


def test_get_deleted_thread_returns_404(client):
    res = client.get("/threads/t2")
    assert res.status_code == 404


def test_list_deleted_threads(client):
    res = client.get("/threads/deleted")
    assert res.status_code == 200
    ids = [thread["id"] for thread in res.json()]
    assert "t2" in ids


def test_create_reply_is_public(client):
    res = client.post(
        "/threads/t1/replies",
        data=json.dumps({"author": "carol", "body": "Great thread!"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert res.json()["author"] == "carol"


def test_delete_reply_keeps_others(client):
    second = client.post(
        "/threads/t1/replies",
        data=json.dumps({"author": "dave", "body": "Second reply"}),
        content_type="application/json",
    )
    assert second.status_code == 201
    res = client.delete("/threads/t1/replies/rp1", headers=AUTH)
    assert res.status_code == 204
    remaining = [r["id"] for r in store.list_replies("t1")]
    assert "rp1" not in remaining
    assert len(remaining) >= 1


def test_create_reply_missing_thread_does_not_increment_count(client):
    before = store.get_thread("t1")["reply_count"]
    res = client.post(
        "/threads/missing/replies",
        data=json.dumps({"author": "eve", "body": "Orphan reply"}),
        content_type="application/json",
    )
    assert res.status_code == 404
    after = store.get_thread("t1")["reply_count"]
    assert after == before


def test_create_thread_requires_auth(client):
    res = client.post(
        "/threads",
        data=json.dumps({"title": "New", "author": "frank"}),
        content_type="application/json",
    )
    assert res.status_code == 401
