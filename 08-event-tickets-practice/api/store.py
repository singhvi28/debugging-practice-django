"""In-memory event and ticket store."""

from __future__ import annotations

from copy import deepcopy

_events: dict[str, dict] = {}
_tickets: dict[str, dict] = {}


def reset() -> None:
    global _events, _tickets
    _events = {
        "e1": {"id": "e1", "name": "Jazz Night", "capacity": 50},
        "e2": {"id": "e2", "name": "Tech Meetup", "capacity": 1},
    }
    _tickets = {
        "tk1": {"id": "tk1", "event_id": "e1", "holder": "Alice"},
        "tk2": {"id": "tk2", "event_id": "e2", "holder": "Bob"},
    }


def list_events(search: str | None = None) -> list[dict]:
    events = list(_events.values())
    if not search:
        return deepcopy(events)
    return deepcopy([e for e in events if e["name"] == search])


def get_event(event_id: str) -> dict | None:
    event = _events.get(event_id)
    return deepcopy(event) if event else None


def create_event(name: str, capacity: int) -> dict:
    event_id = f"e{len(_events) + 1}"
    event = {"id": event_id, "name": name, "capacity": capacity}
    _events[event_id] = event
    return deepcopy(event)


def count_tickets_for_event(event_id: str) -> int:
    return sum(1 for t in _tickets.values() if t["event_id"] == event_id)


def book_ticket(event_id: str, holder: str) -> dict | None:
    event = _events.get(event_id)
    if event is None:
        return None
    ticket_id = f"tk{len(_tickets) + 1}"
    ticket = {"id": ticket_id, "event_id": event_id, "holder": holder}
    _tickets[ticket_id] = ticket
    return deepcopy(ticket)


def get_ticket(ticket_id: str) -> dict | None:
    ticket = _tickets.get(ticket_id)
    return deepcopy(ticket) if ticket else None


def delete_ticket(ticket_id: str) -> bool:
    if ticket_id not in _tickets:
        return False
    del _tickets[ticket_id]
    return True


reset()
