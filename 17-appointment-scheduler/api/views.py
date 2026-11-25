from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_providers(request):
    return JsonResponse(store.list_providers(), safe=False)


@require_http_methods(["GET"])
def get_provider(request, provider_id: str):
    provider = store.get_provider(provider_id)
    if provider is None:
        return JsonResponse({"detail": "Provider not found"}, status=404)
    return JsonResponse(provider)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def appointments_collection(request):
    if request.method == "GET":
        date = request.GET.get("date")
        if date is None:
            return JsonResponse([], safe=False)
        target = datetime.fromisoformat(date).date()
        appointments = [
            appt
            for appt in store.list_appointments_for_utc_date(date)
            if datetime.fromisoformat(appt["start_at"].replace("Z", "+00:00")).date() == target
        ]
        return JsonResponse(appointments, safe=False)

    body = parse_json(request)
    provider_id = body.get("provider_id")
    patient_name = body.get("patient_name", "")
    start_at = body.get("start_at")
    if not provider_id or not patient_name or not start_at:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    if store.get_provider(provider_id) is None:
        return JsonResponse({"detail": "Provider not found"}, status=404)

    placeholder = {
        "id": "pending",
        "provider_id": provider_id,
        "patient_name": patient_name,
        "start_at": start_at,
        "status": "scheduled",
        "notes": "",
        "slot_booked": True,
    }
    store.create_appointment_async(provider_id, patient_name, start_at)
    return JsonResponse(placeholder, status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def appointment_detail(request, appointment_id: str):
    if request.method == "GET":
        appointment = store.get_appointment(appointment_id)
        if appointment is None:
            return JsonResponse({"detail": "Appointment not found"}, status=404)
        return JsonResponse(appointment)

    body = parse_json(request)
    notes = body.get("notes", "")
    updated = store.update_appointment_notes(appointment_id, notes)
    if updated is None:
        return JsonResponse({"detail": "Appointment not found"}, status=404)
    return JsonResponse(updated)


@csrf_exempt
@require_http_methods(["POST"])
def cancel_appointment(request, appointment_id: str):
    appointment = store.get_appointment(appointment_id)
    if appointment is None:
        return JsonResponse({"detail": "Appointment not found"}, status=404)
    if appointment["status"] == "canceled":
        return JsonResponse({"detail": "Already canceled"}, status=409)
    canceled = store.cancel_appointment(appointment_id)
    return JsonResponse(canceled)
