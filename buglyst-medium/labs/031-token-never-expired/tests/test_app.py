import json


def test_valid_session_is_accepted(client):
    issued = client.post(
        "/sessions",
        data=json.dumps({"subject": "alice", "ttl_seconds": 3600}),
        content_type="application/json",
    )
    token = issued.json()["token"]

    response = client.get("/me", HTTP_AUTHORIZATION=f"Bearer {token}")

    assert response.status_code == 200
    assert response.json()["subject"] == "alice"


def test_expired_session_is_rejected(client):
    issued = client.post(
        "/sessions",
        data=json.dumps({"subject": "bob", "ttl_seconds": -30}),
        content_type="application/json",
    )
    token = issued.json()["token"]

    response = client.get("/me", HTTP_AUTHORIZATION=f"Bearer {token}")

    assert response.status_code == 401
