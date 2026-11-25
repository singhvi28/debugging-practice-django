def test_jittered_delay_is_non_negative(client):
    res = client.post("/jitter", data={"base_ms": 50, "jitter_ms": 200, "seed": 7}, content_type="application/json")
    assert res.status_code == 200
    assert res.json()["delay_ms"] >= 0


def test_small_base_with_large_jitter_stays_non_negative(client):
    for seed in range(20):
        res = client.post(
            "/jitter",
            data={"base_ms": 10, "jitter_ms": 500, "seed": seed},
            content_type="application/json",
        )
        assert res.json()["delay_ms"] >= 0


def test_zero_jitter_returns_base(client):
    res = client.post("/jitter", data={"base_ms": 250, "jitter_ms": 0, "seed": 1}, content_type="application/json")
    assert res.json()["delay_ms"] == 250
