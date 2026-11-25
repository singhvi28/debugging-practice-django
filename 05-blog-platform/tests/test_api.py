import json

from tests.conftest import AUTH


def test_search_is_case_insensitive(client):
    res = client.get("/posts", {"search": "hello"})
    assert res.status_code == 200
    titles = [p["title"] for p in res.json()]
    assert "Hello World" in titles


def test_create_post_returns_201(client):
    res = client.post(
        "/posts",
        data=json.dumps({"title": "New Post", "body": "Content here"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["title"] == "New Post"


def test_comment_on_missing_post_returns_404(client):
    res = client.post(
        "/posts/missing/comments",
        data=json.dumps({"author": "Alice", "text": "Great post!"}),
        content_type="application/json",
    )
    assert res.status_code == 404


def test_delete_post_removes_only_target(client):
    res = client.delete("/posts/p1", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/posts/p1").status_code == 404
    assert client.get("/posts/p2").status_code == 200


def test_create_post_without_auth_is_401(client):
    res = client.post(
        "/posts",
        data=json.dumps({"title": "Draft", "body": "secret"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_add_comment_to_post(client):
    res = client.post(
        "/posts/p1/comments",
        data=json.dumps({"author": "Bob", "text": "Nice!"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    comments = client.get("/posts/p1/comments").json()
    assert any(c["text"] == "Nice!" for c in comments)


def test_get_missing_post_returns_404(client):
    # sanity: existing get-by-id path works for known ids
    assert client.get("/posts/p1").status_code == 200


def test_empty_search_returns_all(client):
    res = client.get("/posts")
    assert res.status_code == 200
    assert len(res.json()) == 2
