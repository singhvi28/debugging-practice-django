from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def events_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_events(search), safe=False)

    body = parse_json(request)
    name = body.get("name", "")
    capacity = body.get("capacity")
    if not name or capacity is None:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    event = store.create_event(name, int(capacity))
    return JsonResponse(event)


@require_http_methods(["GET"])
def get_event(request, event_id: str):
    event = store.get_event(event_id)
    return JsonResponse(event, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def book_ticket(request, event_id: str):
    event = store.get_event(event_id)
    if event is None:
        return JsonResponse({"detail": "Event not found"}, status=404)

    body = parse_json(request)
    holder = body.get("holder", "")
    if not holder:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    ticket = store.book_ticket(event_id, holder)
    if ticket is None:
        return JsonResponse({"detail": "Event not found"}, status=404)
    return JsonResponse(ticket, status=201)


@require_http_methods(["GET"])
def get_ticket(request, ticket_id: str):
    ticket = store.get_ticket(ticket_id)
    if ticket is None:
        return JsonResponse({"detail": "Ticket not found"}, status=404)
    return JsonResponse(ticket)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_ticket(request, ticket_id: str):
    if not store.delete_ticket(ticket_id):
        return JsonResponse({"detail": "Ticket not found"}, status=404)
    return HttpResponse(status=204)
