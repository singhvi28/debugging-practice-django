import json

from tests.conftest import AUTH


def test_list_files(client):
    res = client.get("/api/files")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_missing_file_returns_404(client):
    res = client.get("/api/files/missing")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_file_with_auth(client):
    res = client.post(
        "/api/files",
        data=json.dumps({"title": "Notes", "mime_type": "text/plain"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["title"] == "Notes"


def test_update_file_title(client):
    res = client.patch(
        "/api/files/f1",
        data=json.dumps({"title": "Updated Report"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Report"


def test_add_duplicate_tag_returns_409(client):
    res = client.post(
        "/api/files/f1/tags",
        data=json.dumps({"name": "finance"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_search_by_tag_case_insensitive(client):
    res = client.get("/api/files", {"tag": "Finance"})
    assert res.status_code == 200
    ids = [f["id"] for f in res.json()]
    assert "f1" in ids


def test_create_file_without_auth_is_401(client):
    res = client.post(
        "/api/files",
        data=json.dumps({"title": "Secret", "mime_type": "text/plain"}),
        content_type="application/json",
    )
    assert res.status_code == 401
