import threading
from copy import deepcopy
from datetime import datetime, timezone

_providers = {
    "prov_1": {"id": "prov_1", "name": "Dr. Smith", "specialty": "General"},
    "prov_2": {"id": "prov_2", "name": "Dr. Lee", "specialty": "Dermatology"},
}

_appointments: dict[str, dict] = {}
_booked_slots: set[tuple[str, str]] = set()


def reset() -> None:
    global _providers, _appointments, _booked_slots
    _providers = {
        "prov_1": {"id": "prov_1", "name": "Dr. Smith", "specialty": "General"},
        "prov_2": {"id": "prov_2", "name": "Dr. Lee", "specialty": "Dermatology"},
    }
    _appointments = {}
    _booked_slots = set()


def list_providers() -> list[dict]:
    return deepcopy(list(_providers.values()))


def get_provider(provider_id: str) -> dict | None:
    provider = _providers.get(provider_id)
    return deepcopy(provider) if provider else None


def has_booking(provider_id: str, start_at: str) -> bool:
    return (provider_id, start_at) in _booked_slots


def create_appointment_async(provider_id: str, patient_name: str, start_at: str) -> threading.Thread:
    def _work() -> None:
        appointment_id = f"appt_{len(_appointments) + 1}"
        appointment = {
            "id": appointment_id,
            "provider_id": provider_id,
            "patient_name": patient_name,
            "start_at": start_at,
            "status": "scheduled",
            "notes": "",
            "slot_booked": True,
        }
        _appointments[appointment_id] = appointment
        _booked_slots.add((provider_id, start_at))

    return threading.Thread(target=_work)


def get_appointment(appointment_id: str) -> dict | None:
    appointment = _appointments.get(appointment_id)
    return deepcopy(appointment) if appointment else None


def list_appointments_for_utc_date(date_str: str) -> list[dict]:
    results = []
    for appointment in _appointments.values():
        start = datetime.fromisoformat(appointment["start_at"].replace("Z", "+00:00"))
        if start.astimezone(timezone.utc).date().isoformat() == date_str:
            results.append(deepcopy(appointment))
    return results


def update_appointment_notes(appointment_id: str, notes: str) -> dict | None:
    appointment = _appointments.get(appointment_id)
    if appointment is None:
        return None
    appointment["notes"] = notes
    return deepcopy(appointment)


def cancel_appointment(appointment_id: str) -> dict | None:
    appointment = _appointments.get(appointment_id)
    if appointment is None:
        return None
    appointment["status"] = "canceled"
    return deepcopy(appointment)


reset()
