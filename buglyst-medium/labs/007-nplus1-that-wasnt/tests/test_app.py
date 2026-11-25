def test_orders_returns_all_rows(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()["orders"]) == 3


def test_query_count_stays_low(client):
    client.get("/orders")
    assert client.get("/_debug/query-count").json()["queries"] == 1


def test_work_units_stay_bounded(client):
    client.get("/orders")
    work_units = client.get("/_debug/work-units").json()["work_units"]
    assert work_units <= 12
