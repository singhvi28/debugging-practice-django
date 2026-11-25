def test_allows_requests_up_to_capacity(client):
    headers = {"X-Client-Id": "mobile"}
    for _ in range(3):
        response = client.get("/api/resource", headers=headers)
        assert response.status_code == 200


def test_blocks_after_capacity_exhausted(client):
    headers = {"X-Client-Id": "mobile"}
    for _ in range(3):
        assert client.get("/api/resource", headers=headers).status_code == 200

    blocked = client.get("/api/resource", headers=headers)
    assert blocked.status_code == 429


def test_clients_are_isolated(client):
    for _ in range(3):
        assert client.get("/api/resource", headers={"X-Client-Id": "alpha"}).status_code == 200

    assert client.get("/api/resource", headers={"X-Client-Id": "alpha"}).status_code == 429
    assert client.get("/api/resource", headers={"X-Client-Id": "beta"}).status_code == 200
