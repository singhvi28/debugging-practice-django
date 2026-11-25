import json

from tests.conftest import AUTH


def test_list_notifications_with_auth(client):
    res = client.get("/notifications", headers=AUTH)
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_missing_notification_returns_404(client):
    res = client.get("/notifications/does-not-exist", headers=AUTH)
    assert res.status_code == 404


def test_create_rejects_empty_title(client):
    res = client.post(
        "/notifications",
        data=json.dumps({"title": "", "body": "x"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400


def test_mark_one_read_updates_unread_count(client):
    before = client.get("/notifications/unread-count", headers=AUTH).json()["unread_count"]
    res = client.post("/notifications/n1/read", headers=AUTH)
    assert res.status_code == 200
    assert res.json()["unread_count"] == before - 1
    after = client.get("/notifications/unread-count", headers=AUTH).json()["unread_count"]
    assert after == before - 1


def test_mark_all_read_zeros_unread_count(client):
    res = client.post("/notifications/mark-all-read", headers=AUTH)
    assert res.status_code == 200
    assert res.json()["unread_count"] == 0
    count = client.get("/notifications/unread-count", headers=AUTH).json()["unread_count"]
    assert count == 0


def test_mark_all_read_route_not_captured_as_id(client):
    res = client.post("/notifications/mark-all-read", headers=AUTH)
    assert res.status_code == 200
    assert "marked_read" in res.json()
