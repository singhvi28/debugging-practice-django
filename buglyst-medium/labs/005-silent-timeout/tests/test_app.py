import time


def test_slow_upstream_fails_fast(client):
    started = time.monotonic()
    response = client.get("/data")
    elapsed = time.monotonic() - started

    assert response.status_code == 504
    assert elapsed < 0.25


def test_timeout_response_is_explicit(client):
    response = client.get("/data")
    assert response.json()["detail"] == "upstream timeout"
