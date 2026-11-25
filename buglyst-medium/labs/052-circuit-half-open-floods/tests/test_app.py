from circuit_helper import PROBE_LIMIT


def test_half_open_allows_only_one_probe(client):
    client.post("/admin/half-open")
    first = client.post("/proxy")
    second = client.post("/proxy")
    assert first.status_code == 200
    assert second.status_code == 503


def test_half_open_probe_count_capped(client):
    client.post("/admin/half-open")
    client.post("/proxy")
    probes = client.get("/circuit").json()["half_open_probes"]
    assert probes <= PROBE_LIMIT


def test_downstream_called_once_in_half_open(client):
    client.post("/admin/half-open")
    client.post("/proxy")
    client.post("/proxy")
    calls = client.get("/_debug/downstream-calls").json()["calls"]
    assert calls == 1
