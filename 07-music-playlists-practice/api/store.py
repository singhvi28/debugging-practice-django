"""In-memory music store."""

from __future__ import annotations

from copy import deepcopy

_tracks: dict[str, dict] = {}
_playlists: dict[str, dict] = {}


def reset() -> None:
    global _tracks, _playlists
    _tracks = {
        "t1": {"id": "t1", "title": "Bohemian Rhapsody", "artist": "Queen"},
        "t2": {"id": "t2", "title": "Hotel California", "artist": "Eagles"},
    }
    _playlists = {
        "pl1": {"id": "pl1", "name": "Road Trip", "track_ids": ["t1"]},
    }


def list_tracks(search: str | None = None) -> list[dict]:
    tracks = list(_tracks.values())
    if not search:
        return deepcopy(tracks)
    return deepcopy([t for t in tracks if t["title"] == search])


def get_track(track_id: str) -> dict | None:
    track = _tracks.get(track_id)
    return deepcopy(track) if track else None


def create_track(title: str, artist: str) -> dict:
    track_id = f"t{len(_tracks) + 1}"
    track = {"id": track_id, "title": title, "artist": artist}
    _tracks[track_id] = track
    return deepcopy(track)


def get_playlist(playlist_id: str) -> dict | None:
    playlist = _playlists.get(playlist_id)
    return deepcopy(playlist) if playlist else None


def add_track_to_playlist(playlist_id: str, track_id: str) -> dict | None:
    playlist = _playlists.get(playlist_id)
    if playlist is None:
        return None
    playlist["track_ids"].append(track_id)
    return deepcopy(playlist)


def remove_track_from_playlist(playlist_id: str, track_id: str) -> dict | None:
    playlist = _playlists.get(playlist_id)
    if playlist is None:
        return None
    playlist["track_ids"] = [t for t in playlist["track_ids"] if t == track_id]
    return deepcopy(playlist)


reset()
