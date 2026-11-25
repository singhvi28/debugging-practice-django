def test_single_successful_job_restores_one_permit(client):
    client.post("/work")
    assert client.get("/_debug/permits").json()["available"] == 1


def test_two_sequential_jobs_do_not_over_credit_pool(client):
    client.post("/work")
    client.post("/work")
    assert client.get("/_debug/permits").json()["available"] == 1
