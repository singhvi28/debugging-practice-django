def test_authorization_forwarded_to_internal_echo(client):
    token = "Bearer service-token"
    res = client.post("/forward", HTTP_AUTHORIZATION=token)
    assert res.status_code == 200
    echoed = res.json()["received"]
    assert echoed.get("Authorization") == token

    last = client.get("/internal/echo/last")
    assert last.json()["headers"].get("Authorization") == token


def test_non_auth_headers_still_forwarded(client):
    res = client.post("/forward", HTTP_AUTHORIZATION="Bearer abc")
    echoed = res.json()["received"]
    assert echoed.get("X-Request-Id") == "req-1"
