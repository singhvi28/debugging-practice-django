def test_user_can_make_requests_up_to_limit(client):
    headers = {"X-User-Id": "alice"}
    for _ in range(2):
        assert client.get("/search", headers=headers).status_code == 200


def test_same_user_blocked_after_limit(client):
    headers = {"X-User-Id": "alice"}
    for _ in range(2):
        client.get("/search", headers=headers)

    blocked = client.get("/search", headers=headers)
    assert blocked.status_code == 429


def test_different_users_have_independent_buckets(client):
    for _ in range(2):
        assert client.get("/search", headers={"X-User-Id": "alice"}).status_code == 200

    assert client.get("/search", headers={"X-User-Id": "alice"}).status_code == 429
    assert client.get("/search", headers={"X-User-Id": "bob"}).status_code == 200
