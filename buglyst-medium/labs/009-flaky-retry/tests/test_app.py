def test_upstream_failure_returns_503(client):
    response = client.get("/status")
    assert response.status_code == 503


def test_retry_stops_after_max_attempts(client):
    client.get("/status")
    attempts = client.get("/_debug/upstream-attempts").json()["attempts"]
    assert attempts == 3


def test_retry_does_not_amplify_outage(client):
    client.get("/status")
    attempts = client.get("/_debug/upstream-attempts").json()["attempts"]
    assert attempts <= 3
