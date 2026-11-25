from budget_helper import BUDGET_SIZE


def test_successful_call_refunds_budget(client):
    before = client.get("/budget").json()["remaining"]
    res = client.post("/call/alice?failures_before_success=0")
    assert res.status_code == 200
    after = client.get("/budget").json()["remaining"]
    assert after == before


def test_failed_call_consumes_budget(client):
    before = client.get("/budget").json()["remaining"]
    res = client.post("/call/bob?failures_before_success=1")
    assert res.status_code == 503
    after = client.get("/budget").json()["remaining"]
    assert after == before - 1


def test_second_caller_can_use_budget_after_first_succeeds(client):
    client.post("/call/one?failures_before_success=0")
    res = client.post("/call/two?failures_before_success=0")
    assert res.status_code == 200
    assert client.get("/budget").json()["remaining"] == BUDGET_SIZE - 1
