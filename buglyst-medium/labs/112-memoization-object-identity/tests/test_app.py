import json

PAYLOAD = {"term": "keyboard", "category": "electronics"}


def test_identical_queries_reuse_memoized_results(client):
    first = client.post(
        "/search",
        data=json.dumps(PAYLOAD),
        content_type="application/json",
    )
    second = client.post(
        "/search",
        data=json.dumps(PAYLOAD),
        content_type="application/json",
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["cache_hit"] is False
    assert second.json()["cache_hit"] is True
    assert second.json()["calls"] == 1
    assert first.json()["results"] == second.json()["results"]


def test_different_queries_miss_cache(client):
    other = client.post(
        "/search",
        data=json.dumps({"term": "mouse", "category": "electronics"}),
        content_type="application/json",
    )
    assert other.json()["cache_hit"] is False
