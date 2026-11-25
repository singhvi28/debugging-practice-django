def test_stale_read_triggers_revalidation(client):
    client.get("/cache/report")
    client.post("/_debug/wait-stale")
    client.get("/cache/report")
    fetches = client.get("/_debug/fetch-count/report").json()["fetches"]
    assert fetches >= 2


def test_stale_read_returns_stale_then_fresh_on_next(client):
    first = client.get("/cache/data").json()["value"]
    client.post("/_debug/wait-stale")
    stale = client.get("/cache/data").json()["value"]
    assert stale == first
    client.post("/_debug/wait-stale")
    refreshed = client.get("/cache/data").json()["value"]
    assert refreshed != first


def test_fresh_read_does_not_refetch(client):
    client.get("/cache/ticker")
    client.get("/cache/ticker")
    fetches = client.get("/_debug/fetch-count/ticker").json()["fetches"]
    assert fetches == 1
