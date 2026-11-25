def test_cache_expires_after_ttl_and_picks_up_rotation(client):
    first = client.post("/resolve?hostname=api.internal&now=100.0")
    assert first.json()["address"] == "10.0.0.1"
    assert first.json()["resolver_calls"] == 1

    client.post("/rotate")

    second = client.post("/resolve?hostname=api.internal&now=101.5")
    payload = second.json()

    assert payload["address"] == "10.0.0.2"
    assert payload["resolver_calls"] == 2


def test_cache_hit_within_ttl_avoids_extra_lookup(client):
    client.post("/resolve?hostname=edge.internal&now=50.0")
    cached = client.post("/resolve?hostname=edge.internal&now=50.5")

    assert cached.json()["resolver_calls"] == 1
