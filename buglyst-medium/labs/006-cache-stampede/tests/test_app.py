import time
from concurrent.futures import ThreadPoolExecutor


def _warm_and_expire(client) -> int:
    client.get("/report")
    time.sleep(0.06)
    return client.get("/_debug/backend-fetches").json()["fetches"]


def test_concurrent_expiry_hits_backend_once(client):
    before = _warm_and_expire(client)

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(client.get, "/report") for _ in range(8)]
        for future in futures:
            assert future.result().status_code == 200

    after = client.get("/_debug/backend-fetches").json()["fetches"]
    assert after - before == 1


def test_stampede_does_not_multiply_backend_load(client):
    before = _warm_and_expire(client)

    with ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(lambda _: client.get("/report"), range(12)))

    after = client.get("/_debug/backend-fetches").json()["fetches"]
    assert after - before <= 1
