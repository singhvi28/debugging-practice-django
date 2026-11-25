import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/events", {"search": "jazz"})
    assert res.status_code == 200
    names = [e["name"] for e in res.json()]
    assert "Jazz Night" in names


def test_search_partial_match(client):
    res = client.get("/events", {"search": "tech"})
    assert res.status_code == 200
    names = [e["name"] for e in res.json()]
    assert "Tech Meetup" in names


def test_get_missing_event_returns_404(client):
    res = client.get("/events/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_event_returns_201(client):
    res = client.post(
        "/events",
        data=json.dumps({"name": "Rock Fest", "capacity": 100}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Rock Fest"


def test_book_ticket_when_sold_out_returns_409(client):
    res = client.post(
        "/events/e2/tickets",
        data=json.dumps({"holder": "Charlie"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_delete_ticket_with_auth(client):
    res = client.delete("/tickets/tk1", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/tickets/tk1").status_code == 404


def test_book_ticket_success(client):
    res = client.post(
        "/events/e1/tickets",
        data=json.dumps({"holder": "Diana"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["holder"] == "Diana"
