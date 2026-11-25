def test_submit_works_after_rotation(client):
    client.post("/submit")  # prime credential cache with pre-rotation secret

    rotate = client.post("/rotate")
    assert rotate.status_code == 200

    submit = client.post("/submit")
    assert submit.status_code == 200
    assert submit.json()["status"] == "accepted"


def test_submit_uses_fresh_secret_not_stale_cache(client):
    client.post("/submit")  # prime cache
    client.post("/rotate")
    assert client.post("/submit").status_code == 200
