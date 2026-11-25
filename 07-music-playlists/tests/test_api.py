import json

from tests.conftest import AUTH


def test_search_is_case_insensitive(client):
    res = client.get("/tracks", {"search": "bohemian"})
    assert res.status_code == 200
    titles = [t["title"] for t in res.json()]
    assert "Bohemian Rhapsody" in titles


def test_search_partial_match(client):
    res = client.get("/tracks", {"search": "hotel"})
    assert res.status_code == 200
    titles = [t["title"] for t in res.json()]
    assert "Hotel California" in titles


def test_browse_tracks_without_auth(client):
    res = client.get("/tracks")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_missing_track_returns_404(client):
    res = client.get("/tracks/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_playlist_rejects_duplicate_track(client):
    res = client.post(
        "/playlists/pl1/tracks",
        data=json.dumps({"track_id": "t1"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_add_track_to_playlist(client):
    res = client.post(
        "/playlists/pl1/tracks",
        data=json.dumps({"track_id": "t2"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    track_ids = res.json()["track_ids"]
    assert "t2" in track_ids


def test_remove_track_keeps_others(client):
    res = client.delete("/playlists/pl1/tracks/t1", headers=AUTH)
    assert res.status_code == 204
    playlist = client.get("/playlists/pl1").json()
    assert playlist["track_ids"] == []


def test_create_track_with_auth(client):
    res = client.post(
        "/tracks",
        data=json.dumps({"title": "Imagine", "artist": "Lennon"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
