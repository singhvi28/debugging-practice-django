def _collect_all_ids(client) -> list[int]:
    ids: list[int] = []
    cursor = None
    while True:
        params = {"limit": 2}
        if cursor:
            params["cursor"] = cursor
        response = client.get("/activities", params)
        payload = response.json()
        ids.extend(item["id"] for item in payload["items"])
        cursor = payload["next_cursor"]
        if len(payload["items"]) < 2:
            break
    return ids


def test_pagination_returns_every_activity_despite_timestamp_ties(client):
    ids = _collect_all_ids(client)

    assert ids == [1, 2, 3, 4, 5]


def test_first_page_includes_tied_timestamps(client):
    response = client.get("/activities", {"limit": 2})
    payload = response.json()

    assert [item["id"] for item in payload["items"]] == [3, 2]
    assert payload["next_cursor"] == "2024-01-01T10:00:00Z"
