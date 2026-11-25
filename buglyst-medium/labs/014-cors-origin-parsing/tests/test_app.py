def test_trusted_origin_is_allowed(client):
    response = client.get("/public", headers={"Origin": "https://app.trusted.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://app.trusted.com"


def test_lookalike_origin_is_rejected(client):
    response = client.get("/public", headers={"Origin": "https://evil.trusted.com.evil.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_unrelated_origin_is_rejected(client):
    response = client.get("/public", headers={"Origin": "https://evil.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
