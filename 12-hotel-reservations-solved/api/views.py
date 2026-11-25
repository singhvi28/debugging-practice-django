from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_rooms(request):
    return JsonResponse(store.list_rooms(), safe=False)


@require_http_methods(["GET"])
def get_room(request, room_id: str):
    room = store.get_room(room_id)
    if room is None:
        return JsonResponse({"detail": "Room not found"}, status=404)
    return JsonResponse(room, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def bookings_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_bookings(), safe=False)

    body = parse_json(request)
    room_id = body.get("room_id", "")
    guest_name = body.get("guest_name", "")
    checkin = body.get("checkin", "")
    checkout = body.get("checkout", "")
    if not room_id or not guest_name or not checkin or not checkout:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    room = store.get_room(room_id)
    if room is None:
        return JsonResponse({"detail": "Room not found"}, status=404)

    try:
        booking = store.create_booking(room_id, guest_name, checkin, checkout)
    except ValueError as e:
        return JsonResponse({"detail": str(e)}, status=409)
    return JsonResponse(booking, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_booking(request, booking_id: str):
    deleted = store.delete_booking(booking_id)
    if not deleted:
        return JsonResponse({"detail": "Booking not found"}, status=404)
    return HttpResponse(status=204)

