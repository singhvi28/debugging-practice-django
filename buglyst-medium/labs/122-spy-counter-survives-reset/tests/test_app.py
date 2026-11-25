def test_reset_clears_count_and_log(client):
    client.post("/notify/email")
    client.post("/notify/sms")
    client.post("/_test/reset")
    client.post("/notify/push")

    debug = client.get("/_debug/spy").json()
    assert debug["log"] == ["push"]
    assert debug["count"] == 1


def test_fresh_reset_starts_from_zero(client):
    client.post("/_test/reset")
    debug = client.get("/_debug/spy").json()
    assert debug["log"] == []
    assert debug["count"] == 0
