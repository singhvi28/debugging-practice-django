from django.test import Client

client = Client()


def collect_all_task_ids() -> list[str]:
    ids: list[str] = []
    cursor = None

    while True:
        params = {"limit": 2}
        if cursor:
            params["cursor"] = cursor
        response = client.get("/tasks", data=params)
        assert response.status_code == 200
        body = response.json()
        ids.extend(item["id"] for item in body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break

    return ids


def test_cursor_pagination_returns_every_task_once():
    ids = collect_all_task_ids()
    assert ids == ["t1", "t2", "t3", "t4", "t5", "t6"]
    assert len(ids) == len(set(ids))


def test_first_page_respects_limit():
    response = client.get("/tasks", data={"limit": 2})
    body = response.json()
    assert [item["id"] for item in body["items"]] == ["t1", "t2"]
    assert body["next_cursor"] is not None
