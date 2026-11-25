import json

import pytest

from api import store
from tests.conftest import AUTH


def test_list_rooms(client):
    res = client.get("/rooms")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_missing_room_returns_404(client):
    res = client.get("/rooms/missing")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_booking_returns_201(client):
    res = client.post(
        "/bookings",
        data=json.dumps(
            {
                "room_id": "r2",
                "guest_name": "Bob",
                "checkin": "2026-08-15",
                "checkout": "2026-08-18",
            }
        ),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["guest_name"] == "Bob"


def test_authenticated_create_booking_works(client):
    res = client.post(
        "/bookings",
        data=json.dumps(
            {
                "room_id": "r2",
                "guest_name": "Carol",
                "checkin": "2026-09-01",
                "checkout": "2026-09-05",
            }
        ),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201


def test_overlapping_booking_returns_409(client):
    res = client.post(
        "/bookings",
        data=json.dumps(
            {
                "room_id": "r1",
                "guest_name": "Dave",
                "checkin": "2026-08-11",
                "checkout": "2026-08-13",
            }
        ),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_adjacent_booking_allowed(client):
    if store.has_date_conflict("r1", "2026-08-12", "2026-08-14"):
        pytest.fail("adjacent nights should not conflict with half-open intervals")
    res = client.post(
        "/bookings",
        data=json.dumps(
            {
                "room_id": "r1",
                "guest_name": "Eve",
                "checkin": "2026-08-12",
                "checkout": "2026-08-14",
            }
        ),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201


def test_delete_booking_with_auth(client):
    res = client.delete("/bookings/b1", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/bookings").json() == []


def test_create_booking_without_auth_is_401(client):
    res = client.post(
        "/bookings",
        data=json.dumps(
            {
                "room_id": "r2",
                "guest_name": "Frank",
                "checkin": "2026-10-01",
                "checkout": "2026-10-03",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 401
