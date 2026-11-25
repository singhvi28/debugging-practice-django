"""In-memory hotel reservations store."""

from __future__ import annotations

from copy import deepcopy

_rooms: dict[str, dict] = {}
_bookings: dict[str, dict] = {}


def reset() -> None:
    global _rooms, _bookings
    _rooms = {
        "r1": {"id": "r1", "number": "101", "type": "standard"},
        "r2": {"id": "r2", "number": "202", "type": "suite"},
    }
    _bookings = {
        "b1": {
            "id": "b1",
            "room_id": "r1",
            "guest_name": "Alice",
            "checkin": "2026-08-10",
            "checkout": "2026-08-12",
        },
    }


def list_rooms() -> list[dict]:
    return deepcopy(list(_rooms.values()))


def get_room(room_id: str) -> dict | None:
    room = _rooms.get(room_id)
    return deepcopy(room) if room else None


def list_bookings() -> list[dict]:
    return deepcopy(list(_bookings.values()))


def get_booking(booking_id: str) -> dict | None:
    booking = _bookings.get(booking_id)
    return deepcopy(booking) if booking else None


def has_date_conflict(room_id: str, checkin: str, checkout: str) -> bool:
    for booking in _bookings.values():
        if booking["room_id"] != room_id:
            continue
        if checkin < booking["checkout"] and checkout > booking["checkin"]:
            return True
    return False


def create_booking(room_id: str, guest_name: str, checkin: str, checkout: str) -> dict:
    if has_date_conflict(room_id, checkin, checkout):
        raise ValueError("Date conflict")
    booking_id = f"b{len(_bookings) + 1}"
    booking = {
        "id": booking_id,
        "room_id": room_id,
        "guest_name": guest_name,
        "checkin": checkin,
        "checkout": checkout,
    }
    _bookings[booking_id] = booking
    return deepcopy(booking)


def delete_booking(booking_id: str) -> bool:
    if booking_id not in _bookings:
        return False
    del _bookings[booking_id]
    return True


reset()
