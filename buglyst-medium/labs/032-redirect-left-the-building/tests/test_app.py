import json


def _login(client, next_path: str):
    return client.post(
        "/login",
        data=json.dumps(
            {"username": "alice", "password": "secret", "next": next_path}
        ),
        content_type="application/json",
    )


def test_relative_path_is_allowed(client):
    response = _login(client, "/settings/profile")
    assert response.status_code == 200
    assert response.json()["redirect"] == "/settings/profile"


def test_absolute_url_is_rejected(client):
    response = _login(client, "https://evil.example/phish")
    assert response.status_code == 400


def test_protocol_relative_url_is_rejected(client):
    response = _login(client, "//evil.example/phish")
    assert response.status_code == 400
