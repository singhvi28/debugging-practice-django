import math

from backoff_helper import MAX_DELAY_MS


def test_low_attempts_grow_exponentially(client):
    first = client.get("/backoff/1").json()["delay_ms"]
    second = client.get("/backoff/2").json()["delay_ms"]
    assert second > first


def test_delay_is_finite_at_high_attempt():
    from backoff_helper import compute_delay_ms

    delay = compute_delay_ms(1020)
    assert math.isfinite(delay)


def test_delay_never_exceeds_cap(client):
    for attempt in [10, 25, 50, 100]:
        delay = client.get(f"/backoff/{attempt}").json()["delay_ms"]
        assert delay <= MAX_DELAY_MS
