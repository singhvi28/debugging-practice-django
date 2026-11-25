from metrics import _percentile, get_service_samples


def test_p95_reflects_slow_tail_not_average_of_averages(client):
    res = client.get("/metrics/latency")
    assert res.status_code == 200
    samples = get_service_samples()
    all_samples = [v for values in samples.values() for v in values]
    expected = round(_percentile(all_samples, 95), 2)
    assert res.json()["p95_ms"] == expected
    assert res.json()["p95_ms"] >= 180.0


def test_endpoint_lists_services(client):
    res = client.get("/metrics/latency")
    assert set(res.json()["services"]) == {"checkout", "search"}
