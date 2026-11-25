import json


def test_entry_expires_without_reads(client):
    client.post(
        "/cache",
        data=json.dumps({"key": "session", "value": "abc", "ttl_seconds": 10}),
        content_type="application/json",
    )
    client.post(
        "/_test/clock",
        data=json.dumps({"now": 11}),
        content_type="application/json",
    )

    response = client.get("/cache/session")
    assert response.status_code == 404


def test_read_traffic_does_not_extend_ttl_past_write_deadline(client):
    client.post(
        "/cache",
        data=json.dumps({"key": "hot", "value": "v1", "ttl_seconds": 10}),
        content_type="application/json",
    )
    client.post(
        "/_test/clock",
        data=json.dumps({"now": 5}),
        content_type="application/json",
    )
    client.get("/cache/hot")
    client.post(
        "/_test/clock",
        data=json.dumps({"now": 11}),
        content_type="application/json",
    )

    response = client.get("/cache/hot")
    assert response.status_code == 404
